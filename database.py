from typing import Union

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
        self.tables = {}

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
