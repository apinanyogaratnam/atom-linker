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
        # TODO: make this a map maybe?
        if query.startswith("CREATE DATABASE"):
            database_name = query.split(" ")[2]

            if database_name in self.databases:
                msg = f"database {database_name} already exists"
                raise InvalidQueryException(msg)

            db = Database(database_name)
            self.databases[database_name] = db
        elif query.startswith("DELETE DATABASE"):
            database_name = query.split(" ")[2]

            db = self.databases.pop(database_name, None)
            if not db:
                msg = f"database {database_name} does not exist"
                raise InvalidQueryException(msg)

            db.shutdown()
            # TODO: db.delete(): implement this
            del db
        elif query.startswith("SHUTDOWN TABLE"):
            database_name = query.split(" ")[2]
            table_name = query.split(" ")[4]

            db = self.databases.get(database_name)
            if not db:
                msg = f"database {database_name} does not exist"
                raise InvalidQueryException(msg)

            db.shutdown_table(table_name)
        else:
            msg = "failed to execute query"
            raise InvalidQueryException(msg)
