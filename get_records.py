
from internal_types import ColumnName, Record
from stop_words import STOP_WORDS


class GetRecords:
    """Represents a read operation."""

    def __init__(self) -> None:
        """Initialize a new instance of Get."""

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

    def get_records_by_broad_search(self, column_name: ColumnName, search_text: str) -> list[Record]:
        """Get records from the instance by column_name and search_text.

        Args:
        ----
        self: The current object.
        column_name (ColumnName): The name of the column to get records by.
        search_text (str): The text to search for.

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

        if self.columns[column_name] != str:
            msg = f"Column {column_name} is not a string."
            raise ValueError(msg)

        record_ids = set()
        for word in set(search_text.split()).difference(STOP_WORDS):
            with self.inverted_index_lock:  # Lock when accessing the inverted index
                in_inverted_index = column_name in self.inverted_indexes and word in self.inverted_indexes[column_name]
                if in_inverted_index:
                    _record_ids = self.inverted_indexes[column_name][word]

            # Continue using the acquired _record_ids, if available, outside of the lock
            if in_inverted_index:
                record_ids.update(_record_ids)
            else:
                # manual search
                for record_id, record in self.records.items():
                    full_column_text = record[column_name]
                    full_column_text_words = full_column_text.split()
                    if word in full_column_text_words:
                        record_ids.add(record_id)

        return [self.records[record_id] for record_id in record_ids]
