class Get:
    """Represents a read operation."""

    def __init__(self) -> None:
        """Initialize a new instance of Get."""
        pass

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

