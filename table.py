from typing import Any


class Table:
    def __init__(self, name: str, columns: dict) -> None:
        """
            Initializes a new instance of the class.

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

    def insert_record(self, record: dict[str, Any]) -> int:
        """
            Inserts a record into the instance.

            Args:
            ----
            self: The current object.
            record (dict): A dictionary representing the record to insert.

            Raises:
            ------
            ValueError: If the record is empty or not a dictionary.
            ValueError: If a column name is missing from the record.
            ValueError: If a column value is missing from the record.
            ValueError: If a column value is not the correct type.

            Returns:
            -------
            int: The id of the record.
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

        return self.count

    def get_record_by_id(self, id: int) -> Any:
        """
            Gets a record from the instance by id.

            Args:
            ----
            self: The current object.
            id (int): The id of the record to get.

            Raises:
            ------
            ValueError: If the id is empty or not an integer.
            ValueError: If the record does not exist.

            Returns:
            -------
            Any: The record.
        """
        if not id:
            msg = "Id must have a value."
            raise ValueError(msg)
        if not isinstance(id, int):
            msg = "Id must be an integer."
            raise ValueError(msg)

        record = self.records.get(id)
        if not record:
            msg = f"Record with id {id} does not exist."
            raise ValueError(msg)
