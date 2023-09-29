import logging
from datetime import datetime
from typing import Union

import pytz

from database import Database

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def main() -> None:
    """Execute the main function.

    Creates a database instance with the name "test".
    Creates a table named "users" with columns for first name, last name, email, created at, updated at, and deleted at.
    Inserts a record into the "users" table.
    Retrieves the inserted record by its ID and prints it.

    Args:
    ----
        None

    Returns:
    -------
        None
    """
    database_name = "test"
    table_name = "users"

    db = Database(database_name)

    db.create_table(
        table_name,
        {
            "first_name": str,
            "last_name": str,
            "email": str,
            "created_at": datetime,
            "updated_at": datetime,
            "deleted_at": Union[datetime, None], # NOTE: nullable field
        },
    )

    users = db.get_table(table_name)

    record_id = users.insert_record(
        {
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@email.com",
            "created_at": datetime.now(tz=pytz.UTC),
            "updated_at": datetime.now(tz=pytz.UTC),
            "deleted_at": None,
        },
    )

    users.create_unique_index("email")
    record = users.get_record_by_id(record_id)
    logger.debug(record)

    db.drop_table(table_name)

if __name__ == "__main__":
    main()
