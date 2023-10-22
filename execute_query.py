from database import Database
from errors import InvalidQueryError


# TODO: rename this class to something more descriptive
# some ideas: QueryExecutor, QueryHandler, QueryProcessor
# but this also stores the databases, so maybe something like
# DatabaseManager or DatabaseHandler
class ExecuteQuery:
    """Execute a query.

    Executes the given query based on its type.
    If the query is a "CREATE DATABASE" query, it creates a new database with the specified name.
    If the query is a "DELETE DATABASE" query, it deletes the specified database.
    If the query is a "SHUTDOWN TABLE" query, it shuts down the specified table in the specified database.
    Otherwise, it raises an InvalidQueryError.

    Args:
    ----
    self: The instance of the class.
    query (str): The query to execute.

    Returns:
    -------
    None

    Raises:
    ------
    InvalidQueryError: If the query is invalid or the specified database or table does not exist.
    """

    def __init__(self) -> None:
        """Initialize the ExecuteQuery object.

        Creates an empty dictionary to store databases.

        Args:
        ----
        self: The instance of the class.

        Returns:
        -------
        None
        """
        self.databases = {}

    def execute_query(self, query: str) -> None:
        """Execute a query.

        Executes the given query based on its type.
        If the query is a "CREATE DATABASE" query, it creates a new database with the specified name.
        If the query is a "DELETE DATABASE" query, it deletes the specified database.
        If the query is a "SHUTDOWN TABLE" query, it shuts down the specified table in the specified database.
        Otherwise, it raises an InvalidQueryError.

        Args:
        ----
        self: The instance of the class.
        query (str): The query to execute.

        Returns:
        -------
        None

        Raises:
        ------
        InvalidQueryError: If the query is invalid or the specified database or table does not exist.
        """
        # TODO: make this a map maybe?
        if query.startswith("CREATE DATABASE"):
            database_name = query.split(" ")[2]

            if database_name in self.databases:
                msg = f"database {database_name} already exists"
                raise InvalidQueryError(msg)

            db = Database(database_name)
            self.databases[database_name] = db
        elif query.startswith("DELETE DATABASE"):
            database_name = query.split(" ")[2]

            db = self.databases.pop(database_name, None)
            if not db:
                msg = f"database {database_name} does not exist"
                raise InvalidQueryError(msg)

            db.shutdown()
            # TODO: db.delete(): implement this
            del db
        elif query.startswith("SHUTDOWN TABLE"):
            database_name = query.split(" ")[2]
            table_name = query.split(" ")[4]

            db = self.databases.get(database_name)
            if not db:
                msg = f"database {database_name} does not exist"
                raise InvalidQueryError(msg)

            db.shutdown_table(table_name)
        else:
            msg = "failed to execute query"
            raise InvalidQueryError(msg)
