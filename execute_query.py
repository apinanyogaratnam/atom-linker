from database import Database
from errors import InvalidQueryException


# TODO: rename this class to something more descriptive
# some ideas: QueryExecutor, QueryHandler, QueryProcessor
# but this also stores the databases, so maybe something like
# DatabaseManager or DatabaseHandler
class ExecuteQuery:
    def __init__(self) -> None:
        self.databases = {}

    def execute_query(self, query) -> None:
        if query.startswith("CREATE DATABASE"):
            database_name = query.split(" ")[2]

            db = Database(database_name)
            self.databases[database_name] = db
        else:
            msg = "failed to execute query"
            raise InvalidQueryException(msg)
