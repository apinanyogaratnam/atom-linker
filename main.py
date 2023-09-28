import logging
from datetime import datetime

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
    db = Database("test")

    db.create_table(
        "users",
        {
            "first_name": str,
            "last_name": str,
            "email": str,
            "created_at": datetime,
            "updated_at": datetime,
            # "deleted_at": datetime, # NOTE: need to figure out how to make this optional
        },
    )

    users = db.get_table("users")

    record_id = users.insert_record(
        {
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@email.com",
            "created_at": datetime.now(tz=pytz.UTC),
            "updated_at": datetime.now(tz=pytz.UTC),
        },
    )

    record = users.get_record_by_id(record_id)
    logger.debug(record)

if __name__ == "__main__":
    main()
