from typing import Any, Union

from table import Table


class Database:
    """Represents a database.

    Args:
    ----
        name (str): The name of the database.

    Raises:
    ------
        ValueError: If the name is empty or not a string.

    Returns:
    -------
        None
    """

    def __init__(self, name: str) -> None:
        """Initialize a new instance of the class.

        Args:
        ----
        self: The current object.
        name (str): The name of the database.

        Raises:
        ------
        ValueError: If the name is empty or not a string.

        Returns:
        -------
        None
        """
        if not name:
            msg = "Database must have a name."
            raise ValueError(msg)
        if not isinstance(name, str):
            msg = "Name must be a string."
            raise TypeError(msg)

        self.name = name
        self.tables: dict[str, Table] = {}

    def is_type_or_union_of_types(self, x: object) -> bool:
        """Check if the given object is a type or a union of types.

        Args:
        ----
        self: The current object.
        x: The object to check.

        Returns:
        -------
        bool: True if the object is a type or a union of types, False otherwise.
        """
        if isinstance(x, type):
            return True

        if getattr(x, "__origin__", None) is Union:
            return all(isinstance(t, type) for t in x.__args__)

        return False

    def __validate_create_table_columns(self, columns: dict) -> None:
        """Validate the arguments for the create_table method.

        Args:
        ----
        self: The current object.
        columns (dict): A dictionary representing the columns of the table.

        Raises:
        ------
        ValueError: If a column does not have a name.
        ValueError: If a column does not have a type.
        TypeError: If a column name is not a string.
        TypeError: If a column type is not a type.

        Returns:
        -------
        None
        """
        for column_name, column_type in columns.items():
            if not column_name:
                msg = "Column must have a name."
                raise ValueError(msg)
            if not column_type:
                msg = "Column must have a type."
                raise ValueError(msg)
            if not isinstance(column_name, str):
                msg = "Column name must be a string."
                raise TypeError(msg)
            if not self.is_type_or_union_of_types(column_type):
                msg = "Column type must be a type or union of types."
                raise TypeError(msg)

    def __validate_create_table(self, name: str, columns: dict) -> None:
        """Validate the arguments for the create_table method.

        Args:
        ----
        self: The current object.
        name (str): The name of the table.
        columns (dict): A dictionary representing the columns of the table.

        Raises:
        ------
        ValueError: If the name is empty.
        ValueError: If the table already exists.
        ValueError: If the columns are empty.
        TypeError: If the name is not a string.
        TypeError: If the columns are not a dictionary.
        ValueError: If a column does not have a name.
        ValueError: If a column does not have a type.
        TypeError: If a column name is not a string.
        TypeError: If a column type is not a type.

        Returns:
        -------
        None
        """
        if not name:
            msg = "Table must have a name."
            raise ValueError(msg)
        if name in self.tables:
            msg = f"Table {name} already exists."
            raise ValueError(msg)
        if not columns:
            msg = "Table must have columns."
            raise ValueError(msg)
        if not isinstance(name, str):
            msg = "Name must be a string."
            raise TypeError(msg)
        if not isinstance(columns, dict):
            msg = "Columns must be a dictionary."
            raise TypeError(msg)

        self.__validate_create_table_columns(columns)

    def create_table(self, name: str, columns: dict) -> None:
        """Create a new table in the database.

        Args:
        ----
        self: The current object.
        name (str): The name of the table.
        columns (dict): A dictionary representing the columns of the table.

        Raises:
        ------
        ValueError: If the name is empty.
        ValueError: If the table already exists.
        ValueError: If the columns are empty.
        TypeError: If the name is not a string.
        TypeError: If the columns are not a dictionary.
        ValueError: If a column does not have a name.
        ValueError: If a column does not have a type.
        TypeError: If a column name is not a string.
        TypeError: If a column type is not a type.

        Returns:
        -------
        None
        """
        self.__validate_create_table(name, columns)

        self.tables[name] = Table(name, columns)

    def get_table(self, name: str) -> Table:
        """Retrieve a table from the database.

        Args:
        ----
        self: The current object.
        name (str): The name of the table to retrieve.

        Raises:
        ------
        ValueError: If the table does not exist.

        Returns:
        -------
        Table: The requested table.
        """
        if name not in self.tables:
            msg = f"Table {name} does not exist."
            raise ValueError(msg)

        return self.tables[name]

    def drop_table(self, name: str) -> None:
        """Drop a table from the database.

        Args:
        ----
        self: The current object.
        name (str): The name of the table to drop.

        Raises:
        ------
        ValueError: If the table does not exist.

        Returns:
        -------
        None
        """
        if name not in self.tables:
            msg = f"Table {name} does not exist."
            raise ValueError(msg)

        del self.tables[name]

    def create_foreign_key(
        self, table_name: str, column_name: str, foreign_table_name: str,
    ) -> None:
        """Create a foreign key on a column.

        Args:
        ----
        self: The current object.
        table_name (str): The name of the table.
        column_name (str): The name of the column.
        foreign_table_name (str): The name of the foreign table.

        Raises:
        ------
        ValueError: If the table does not exist.
        ValueError: If the column does not exist.
        ValueError: If the foreign table does not exist.

        Returns:
        -------
        None
        """
        if table_name not in self.tables:
            msg = f"Table {table_name} does not exist."
            raise ValueError(msg)

        table = self.tables[table_name]

        if column_name not in table.columns:
            msg = f"Column {column_name} does not exist."
            raise ValueError(msg)

        if foreign_table_name not in self.tables:
            msg = f"Foreign table {foreign_table_name} does not exist."
            raise ValueError(msg)

        foreign_table = self.tables[foreign_table_name]

        if table.columns[column_name] != int:
            msg = f"Column {column_name} is not an integer."
            raise ValueError(msg)

        table.create_foreign_key_column(column_name, foreign_table)

    def insert_record_into_table(self, table_name: str, record: dict[str, Any]) -> int:
        """_summary_.

        Args:
        ----
            table_name (str): _description_
            record (dict[str, Any]): _description_
        """
        if table_name not in self.tables:
            msg = f"Table {table_name} does not exist."
            raise ValueError(msg)

        table = self.tables[table_name]

        table._validate_record(record)

        for column_name, column_value in record.items():
            if column_name in table.foreign_keys:
                foreign_table_name = table.foreign_keys[column_name]
                foreign_table = self.tables[foreign_table_name]
                if column_value not in foreign_table.records:
                    msg = f"Value {column_value} does not exist in foreign table {foreign_table_name}."
                    raise ValueError(msg)

        return table.insert_record(record)

    def update_record_by_id_into_table(self, table_name: str, record_id: int, record: dict[str, Any]) -> None:
        """_summary_.

        Args:
        ----
            table_name (str): _description_
            record_id (int): _description_
            record (dict[str, Any]): _description_
        """
        if table_name not in self.tables:
            msg = f"Table {table_name} does not exist."
            raise ValueError(msg)

        table = self.tables[table_name]

        table._validate_update_record_by_id(record_id, record)

        for column_name, column_value in record.items():
            if column_name in table.foreign_keys:
                foreign_table_name = table.foreign_keys[column_name]
                foreign_table = self.tables[foreign_table_name]
                if column_value not in foreign_table.records:
                    msg = f"Value {column_value} does not exist in foreign table {foreign_table_name}."
                    raise ValueError(msg)

        table.update_record_by_id(record_id, record)
