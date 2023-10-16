from typing import Any, Dict, Set
from stop_words import STOP_WORDS
from internal_types import Record, RowId, ColumnName, Word


class Table:
    """Represents a table.

    Args:
    ----
        name (str): The name of the table.
        columns (dict): A dictionary representing the columns of the table.

    Returns:
    -------
        None
    """

    def __init__(self, name: str, columns: dict) -> None:
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
        self.name = name
        self.columns = columns
        self.count = 0
        self.records = {}

        self.indexes = {}
        self.unique_indexes = {}
        self.inverted_indexes: Dict[ColumnName, Dict[Word, Set[RowId]]] = {} # text search

        self.foreign_keys = {}

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
        # self.__validate_record(record)
        self.count += 1
        self.records[self.count] = record

        for column_name, column_value in record.items():
            if column_name in self.indexes:
                if column_value not in self.indexes[column_name]:
                    self.indexes[column_name][column_value] = []

                self.indexes[column_name][column_value].append(self.count)

            if column_name in self.unique_indexes:
                if column_value in self.unique_indexes[column_name]:
                    msg = f"Value {column_value} for column {column_name} is not unique."
                    raise ValueError(msg)

                self.unique_indexes[column_name][column_value] = self.count

        return self.count

    def get_record_by_id(self, record_id: int) -> object:
        """Get a record from the instance by record_id.

        Args:
        ----
        self: The current object.
        record_id (int): The id of the record to get.

        Raises:
        ------
        ValueError: If the id is empty.
        TypeError: If the id is not an integer.
        ValueError: If the record does not exist.

        Returns:
        -------
        object: The record.
        """
        if not record_id:
            msg = "Id must have a value."
            raise ValueError(msg)
        if not isinstance(record_id, int):
            msg = "Id must be an integer."
            raise TypeError(msg)

        record = self.records.get(record_id)
        if not record:
            msg = f"Record with id {record_id} does not exist."
            raise ValueError(msg)

        return record

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
        for column_name, column_value in old_record.items():
            if column_name in self.indexes:
                self.indexes[column_name][column_value].remove(record_id)

            if column_name in self.unique_indexes:
                self.unique_indexes[column_name].pop(column_value)

        self.records[record_id] = record

        return self.records[record_id]

    def __validate_delete_record_by_id(self, record_id: int) -> None:
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
        self.__validate_delete_record_by_id(record_id)
        record = self.records.pop(record_id)

        for column_name, column_value in record.items():
            if column_name in self.indexes:
                self.indexes[column_name][column_value].remove(record_id)

            if column_name in self.unique_indexes:
                self.unique_indexes[column_name].pop(column_value)

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

        self.indexes[column_name] = {}

        for record_id, record in self.records.items():
            value = record[column_name]
            if value not in self.indexes[column_name]:
                self.indexes[column_name][value] = set()

            self.indexes[column_name][value].add(record_id)

    def get_records_by_column(self, column_name: str, column_value: object) -> list[object]:
        """Get records from the instance by column_name and column_value.

        Args:
        ----
        self: The current object.
        column_name (str): The name of the column to get records by.
        column_value (object): The value of the column to get records by.

        Raises:
        ------
        ValueError: If the column does not exist.

        Returns:
        -------
        list: A list of records.
        """
        if column_name not in self.columns:
            msg = f"Column {column_name} does not exist."
            raise ValueError(msg)

        is_indexed = False
        record_ids = set()
        if column_name in self.indexes and column_value in self.indexes[column_name]:
            is_indexed = True
            record_ids = set(self.indexes[column_name][column_value])

        if column_name in self.unique_indexes and column_value in self.unique_indexes[column_name]:
            is_indexed = True
            record_id = self.unique_indexes[column_name][column_value]
            record_ids.add(record_id)

        if not is_indexed:
            for record_id, record in self.records.items():
                if record[column_name] == column_value:
                    record_ids.add(record_id)

        return [self.records[record_id] for record_id in record_ids]

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

    def get_records(self) -> list[object]:
        """Get records from the instance.

        Args:
        ----
        self: The current object.

        Returns:
        -------
        list: A list of records.
        """
        return list(self.records.values())
