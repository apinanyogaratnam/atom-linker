from errors import InvalidQueryException

from database import Database


class ExecuteQuery:
    def __init__(self, query: str) -> None:
        self.query = query
        self.databases = {}

    def execute_query(self) -> None:
        query = self.query

        if query.startswith("CREATE DATABASE"):
            database_name = query.split(" ")[2]

            db = Database(database_name)
            self.databases[database_name] = db
        else:
            raise InvalidQueryException("failed to execute query")
