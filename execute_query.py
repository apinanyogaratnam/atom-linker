from database import Database
from errors import InvalidQueryException


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
            msg = "failed to execute query"
            raise InvalidQueryException(msg)
