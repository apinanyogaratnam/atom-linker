import os
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from typing import Any

from get_records import GetRecords
from indexes import Indexes
from internal_types import ColumnName, Columns, Index, InvertedIndex, RowId
from log import get_logger
from stop_words import STOP_WORDS

logger = get_logger(__file__)

num_cores = os.cpu_count()


# NOTE: might not need to inherit from Indexes since we are already inheriting from GetRecords
class Table(GetRecords, Indexes):
    """Represents a table.

    Args:
    ----
        name (str): The name of the table.
        columns (dict): A dictionary representing the columns of the table.

    Returns:
    -------
        None
    """

    def __init__(self, name: str, columns: Columns) -> None:
        """Initialize a new instance of the class.

        Args:
        ----
        self: The current object.
        name (str): The name of the instance.
        columns (dict): A dictionary representing the columns of the instance.

        Returns:
        -------
        None
        """
        self.name: str = name
        self.columns: Columns = columns
        self.count = 0
        self.records = {}

        # TODO: @apinanyogaratnam: need to remove all if conditions that checks wether
        # TODO: the item exists or not to create a new set
        self.indexes: Index = defaultdict(lambda: defaultdict(set))
        # can get the column value from the record
        self.records_to_index: dict[ColumnName, set[RowId]] = defaultdict(set)
        self.records_to_index_lock = Lock()
        # need to make sure when columns are being CRUD, the lock is also being CRUD
        self.column_locks: dict[ColumnName, Lock] = {}
        self.undergoing_column_indexing: dict[ColumnName, int] = defaultdict(int)
        self.undergoing_column_indexing_lock = Lock()
        # NOTE: need to make this configurable or figure out how to dynamically set it based on resources
        # this is the pool of threads that will be used to create indexes
        # adjust max workers when dealing with io bound tasks
        # adjust max workers after testing speeds in real world situations and profiling
        # num cores is not a good number, need to find a better number
        self.index_executor = ThreadPoolExecutor(max_workers=num_cores)

        self.unique_indexes = {}
        self.unique_index_lock = Lock()

        # text search
        self.inverted_indexes: InvertedIndex = {}
        self.inverted_index_lock = Lock()

        self.foreign_keys = {}

        self._create_column_locks()
        self._create_records_to_index_keys()

    def _create_column_locks(self) -> None:
        for column_name in self.columns:
            self.column_locks[column_name] = Lock()

    def _create_records_to_index_keys(self) -> None:
        for column_name in self.columns:
            self.records_to_index[column_name] = set()

    def _create_records_to_index_thread(self) -> None:
        columns = self.records_to_index.keys()
        with self.undergoing_column_indexing_lock:
            for column_name in columns:
                self.undergoing_column_indexing[column_name] += 1

        for column_name, record_ids in self.records_to_index.items():
            column_lock = self.column_locks[column_name]

            with self.records_to_index_lock:
                for record_id in record_ids:
                    column_value = self.records[record_id][column_name]

                    with column_lock:
                        self.indexes[column_name][column_value].add(record_id)

                self.records_to_index[column_name].clear()

        with self.undergoing_column_indexing_lock:
            for column_name in columns:
                self.undergoing_column_indexing[column_name] -= 1

    def is_column_indexed(self, column_name: str) -> bool:
        """Check if a column is indexed.

        Args:
        ----
        self: The current object.
        column_name (str): The name of the column to check.

        Returns:
        -------
        bool: True if the column is indexed, False otherwise.
        """
        if not self.is_column_locked(column_name):
            return False
        if column_name not in self.indexes:
            return False

        with self.undergoing_column_indexing_lock:
            return self.undergoing_column_indexing[column_name] == 0

    def is_column_locked(self, column_name: str) -> bool:
        """Check if a column is locked.

        Args:
        ----
        self: The current object.
        column_name (str): The name of the column to check.

        Returns:
        -------
        bool: True if the column is locked, False otherwise.
        """
        return self.column_locks[column_name].locked()

    # TODO: @apinanyogaratnam: need to be aware of the lock for self.indexes
    def insert_record(self, record: dict[str, Any]) -> int:
        """Insert a record into the instance.

        Args:
        ----
        self: The current object.
        record (dict): A dictionary representing the record to insert.

        Raises:
        ------
        ValueError: If the record is empty.
        TypeError: If the record is not a dictionary.
        ValueError: If the record does not have a value for a column.
        TypeError: If the record value for a column is not the correct type.

        Returns:
        -------
        int: The id of the record.
        """
        self.count += 1
        self.records[self.count] = record

        for column_name, column_value in record.items():
            if column_name in self.indexes:
                with self.records_to_index_lock:
                    self.records_to_index[column_name].add(self.count)

            if column_name in self.unique_indexes:
                if column_value in self.unique_indexes[column_name]:
                    msg = f"Value {column_value} for column {column_name} is not unique."
                    raise ValueError(msg)

                self.unique_indexes[column_name][column_value] = self.count

            if column_name in self.inverted_indexes:
                for word in set(column_value.split()).difference(STOP_WORDS):
                    if word not in self.inverted_indexes[column_name]:
                        self.inverted_indexes[column_name][word] = set()

                    self.inverted_indexes[column_name][word].add(self.count)

        self.index_executor.submit(self._create_records_to_index_thread)

        return self.count

    def validate_update_record_by_id(self, record_id: int, record: dict[str, Any]) -> None:
        """Validate the arguments for the update_record_by_id method.

        Args:
        ----
        self: The current object.
        record_id (int): The id of the record to update.
        record (dict): A dictionary representing the record to update.

        Raises:
        ------
        ValueError: If the id is empty.
        TypeError: If the id is not an integer.
        ValueError: If the record is empty.
        TypeError: If the record is not a dictionary.
        ValueError: If the record does not have a value for a column.
        TypeError: If the record value for a column is not the correct type.
        ValueError: If the record does not exist.

        Returns:
        -------
        None
        """
        if not record_id:
            msg = "Id must have a value."
            raise ValueError(msg)
        if not isinstance(record_id, int):
            msg = "Id must be an integer."
            raise TypeError(msg)
        self.validate_record(record)
        if record_id not in self.records:
            msg = f"Record with id {record_id} does not exist."
            raise ValueError(msg)

    def validate_record(self, record: dict[str, Any]) -> None:
        """Validate the arguments for the insert_record and update_record_by_id methods.

        Args:
        ----
        self: The current object.
        record (dict): A dictionary representing the record to insert or update.

        Raises:
        ------
        ValueError: If the record is empty.
        TypeError: If the record is not a dictionary.
        ValueError: If the record does not have a value for a column.
        TypeError: If the record value for a column is not the correct type.

        Returns:
        -------
        None
        """
        if not record:
            msg = "Record must have a value."
            raise ValueError(msg)
        if not isinstance(record, dict):
            msg = "Record must be a dictionary."
            raise TypeError(msg)
        for column_name, column_type in self.columns.items():
            if column_name not in record:
                msg = f"Record must have a value for {column_name}."
                raise ValueError(msg)
            if not isinstance(record[column_name], column_type):
                msg = f"Record value for {column_name} must be {column_type}."
                raise TypeError(msg)

    # TODO: @apinanyogaratnam: need to be aware of the lock for self.indexes
    # TODO: @apinanyogaratnam: need to fix this since it won't reindex the record
    def update_record_by_id(self, record_id: int, record: dict[str, Any]) -> object:
        """Update a record in the instance by record_id.

        Args:
        ----
        self: The current object.
        record_id (int): The id of the record to update.
        record (dict): A dictionary representing the record to update.

        Raises:
        ------
        ValueError: If the id is empty.
        TypeError: If the id is not an integer.
        ValueError: If the record is empty.
        TypeError: If the record is not a dictionary.
        ValueError: If the record does not have a value for a column.
        TypeError: If the record value for a column is not the correct type.
        ValueError: If the record does not exist.

        Returns:
        -------
        object: The record.
        """
        self.validate_update_record_by_id(record_id, record)
        old_record = self.records[record_id]

        for column_name, old_column_value in old_record.items():
            # Handle normal indexes
            if column_name in self.indexes:
                new_column_value = record[column_name]

                with self.column_locks[column_name]:
                    if old_column_value in self.indexes[column_name]:
                        self.indexes[column_name][old_column_value].discard(record_id)
                    self.indexes[column_name][new_column_value].add(record_id)

            # Handle unique indexes
            if column_name in self.unique_indexes:
                self.unique_indexes[column_name].pop(old_column_value, None)

        self.records[record_id] = record
        return self.records[record_id]


    def _validate_delete_record_by_id(self, record_id: int) -> None:
        """Validate the arguments for the delete_record_by_id method.

        Args:
        ----
        self: The current object.
        record_id (int): The id of the record to delete.

        Raises:
        ------
        ValueError: If the id is empty.
        TypeError: If the id is not an integer.
        ValueError: If the record does not exist.

        Returns:
        -------
        None
        """
        if not record_id:
            msg = "Id must have a value."
            raise ValueError(msg)
        if not isinstance(record_id, int):
            msg = "Id must be an integer."
            raise TypeError(msg)

        if record_id not in self.records:
            msg = f"Record with id {record_id} does not exist."
            raise ValueError(msg)

    # TODO: @apinanyogaratnam: need to be aware of the lock for self.indexes
    def delete_record_by_id(self, record_id: int) -> None:
        """Delete a record from the instance by record_id.

        Args:
        ----
        self: The current object.
        record_id (int): The id of the record to delete.

        Raises:
        ------
        ValueError: If the id is empty.
        TypeError: If the id is not an integer.
        ValueError: If the record does not exist.

        Returns:
        -------
        None
        """
        self._validate_delete_record_by_id(record_id)
        record = self.records.pop(record_id)

        for column_name, column_value in record.items():
            if column_name in self.indexes:
                column_index = self.indexes.get(column_name, {})
                if record_ids := column_index.get(column_value, set()):
                    column_lock = self.column_locks[column_name]
                    with column_lock:
                        record_ids.discard(record_id)

            if column_name in self.unique_indexes:
                unique_index = self.unique_indexes.get(column_name, {})
                unique_index.pop(column_value, None)


    def create_unique_index(self, column_name: str) -> None:
        """Create a unique index on a column.

        Args:
        ----
        self: The current object.
        column_name (str): The name of the column to create a unique index on.

        Raises:
        ------
        ValueError: If the column does not exist.

        Returns:
        -------
        None
        """
        if column_name not in self.columns:
            msg = f"Column {column_name} does not exist."
            raise ValueError(msg)

        self.unique_indexes[column_name] = {}

        for record_id, record in self.records.items():
            value = record[column_name]
            if value in self.unique_indexes[column_name]:
                msg = f"Value {value} for column {column_name} is not unique."
                raise ValueError(msg)

            self.unique_indexes[column_name][value] = record_id

    def _create_index_thread(self, column_name: str) -> None:
        with self.undergoing_column_indexing_lock:
            self.undergoing_column_indexing[column_name] += 1

        for record_id, record in self.records.items():
            column_lock = self.column_locks[column_name]
            column_value = record[column_name]
            with column_lock:
                self.indexes[column_name][column_value].add(record_id)

        with self.undergoing_column_indexing_lock:
            self.undergoing_column_indexing[column_name] -= 1

    def create_index(self, column_name: str) -> None:
        """Create an index on a column.

        Args:
        ----
        self: The current object.
        column_name (str): The name of the column to create an index on.

        Raises:
        ------
        ValueError: If the column does not exist.

        Returns:
        -------
        None
        """
        if column_name not in self.columns:
            msg = f"Column {column_name} does not exist."
            raise ValueError(msg)

        if column_name in self.indexes:
            msg = f"Index for column {column_name} already exists."
            raise ValueError(msg)

        self.index_executor.submit(self._create_index_thread, column_name)

    def create_foreign_key_column(self, column_name: str, foreign_table: "Table") -> None:
        """Create a foreign key column.

        Args:
        ----
        self: The current object.
        column_name (str): The name of the column to create a foreign key on.
        foreign_table (Table): The foreign table.

        Raises:
        ------
        ValueError: If the column already exists.
        ValueError: If the foreign table does not exist.

        Returns:
        -------
        None
        """
        foreign_table_ids = set(foreign_table.records.keys())
        table_column_values = {record[column_name] for record in self.records.values()}

        if not table_column_values.issubset(foreign_table_ids):
            msg = f"Cannot create foreign key on {column_name} because not all values exist in foreign table."
            raise ValueError(msg)

        self.foreign_keys[column_name] = foreign_table.name

    def _create_inverted_index_thread(self, column_name: str) -> None:
        # NOTE: need to rewrite this method
        local_index = defaultdict(set)
        for record_id, record in self.records.items():
            for word in self.get_sanitized_words(record[column_name]):
                local_index[word].add(record_id)

        with self.inverted_index_lock:
            self.inverted_indexes[column_name] = local_index

    def create_inverted_index(self, column_name: str) -> None:
        """Create an inverted index on a column.

        Args:
        ----
        self: The current object.
        column_name (str): The name of the column to create an inverted index on.

        Raises:
        ------
        ValueError: If the column does not exist.

        Returns:
        -------
        None
        """
        if column_name not in self.columns:
            msg = f"Column {column_name} does not exist."
            raise ValueError(msg)

        if column_name in self.inverted_indexes:
            msg = f"Inverted index for column {column_name} already exists."
            raise ValueError(msg)

        if self.columns[column_name] != str:
            msg = f"Cannot create inverted index for column {column_name} because it is not a string."
            raise ValueError(msg)

        # thread = Thread(target=self._create_inverted_index_thread, args=(column_name,))
        # thread.start()

        for record_id, record in self.records.items():
            if column_name not in self.inverted_indexes:
                self.inverted_indexes[column_name] = {}

            for word in self.get_sanitized_words(record[column_name]):
                if word not in self.inverted_indexes[column_name]:
                    self.inverted_indexes[column_name][word] = set()

                self.inverted_indexes[column_name][word].add(record_id)

    def close_index_executor(self) -> None:
        """Close the index executor.

        Shuts down the index executor.

        Args:
        ----
        self: The instance of the class.

        Returns:
        -------
        None
        """
        self.index_executor.shutdown()

    def shutdown_executors(self) -> None:
        """Shutdown the executors.

        Calls the `close_index_executor` method to shut down the index executor.

        Args:
        ----
        self: The instance of the class.

        Returns:
        -------
        None
        """
        self.close_index_executor()

    def shutdown(self) -> None:
        """Shutdown the object.

        Calls the `shutdown_executors` method to shut down the executors.

        Args:
        ----
        self: The instance of the class.

        Returns:
        -------
        None
        """
        self.shutdown_executors()
