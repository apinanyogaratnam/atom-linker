from table import Table


class Database:
    def __init__(self, name: str) -> None:
        """Initializes a new instance of the class.

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
            raise ValueError(msg)

        self.name = name
        self.tables = {}

    def create_table(self, name: str, columns: dict) -> None:
        """Creates a new table in the database.

        Args:
        ----
        self: The current object.
        name (str): The name of the table.
        columns (dict): A dictionary representing the columns of the table.

        Raises:
        ------
        ValueError: If the name is empty, already exists, or not a string.
        ValueError: If the columns are empty or not a dictionary.
        ValueError: If a column name is empty, a type is missing, or the name or type is not a string or type, respectively.

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
            raise ValueError(msg)
        if not isinstance(columns, dict):
            msg = "Columns must be a dictionary."
            raise ValueError(msg)

        for column_name, column_type in columns.items():
            if not column_name:
                msg = "Column must have a name."
                raise ValueError(msg)
            if not column_type:
                msg = "Column must have a type."
                raise ValueError(msg)
            if not isinstance(column_name, str):
                msg = "Column name must be a string."
                raise ValueError(msg)
            if not isinstance(column_type, type):
                msg = "Column type must be a type."
                raise ValueError(msg)

        self.tables[name] = Table(name, columns)

    def get_table(self, name: str) -> Table:
        """Retrieves a table from the database.

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
