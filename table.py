from typing import Any


class Table:
    def __init__(self, name: str, columns: dict) -> None:
        """Initializes a new instance of the class.

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

    def insert_record(self, record: dict[str, Any]) -> None:
        """Inserts a record into the instance.

        Args:
        ----
        self: The current object.
        record (dict): A dictionary representing the record to insert.

        Returns:
        -------
        None
        """
        if not record:
            msg = "Record must have a value."
            raise ValueError(msg)
        if not isinstance(record, dict):
            msg = "Record must be a dictionary."
            raise ValueError(msg)

        for column_name, column_type in self.columns.items():
            if column_name not in record:
                msg = f"Record must have a value for {column_name}."
                raise ValueError(msg)
            if not isinstance(record[column_name], column_type):
                msg = f"Record value for {column_name} must be {column_type}."
                raise ValueError(msg)

        self.count += 1
        self.records[self.count] = record
