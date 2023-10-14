import logging
from datetime import datetime
from typing import Union

import pytz

from database import Database
import os

logging.basicConfig(level=logging.DEBUG)
file_name = os.path.basename(__file__)
logger = logging.getLogger(file_name)
# setup logger to write to file
fh = logging.FileHandler(f"{file_name}.log")
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)


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

    john_record_id = db.insert_record_into_table(
        table_name,
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
    users.create_index("first_name")

    jane_record_id = db.insert_record_into_table(
        table_name,
        {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "janedoe@email.com",
            "created_at": datetime.now(tz=pytz.UTC),
            "updated_at": datetime.now(tz=pytz.UTC),
            "deleted_at": None,
        },
    )

    users.get_record_by_id(john_record_id)
    users.get_record_by_id(jane_record_id)

    users.get_records_by_column("email", "johndoe@email.com")
    users.get_records_by_column("first_name", "John")
    users.get_records_by_column("last_name", "Doe")

    users_records = users.get_records()
    logger.debug(f'all users_records: {users_records}')
    sorted_user_records = db.sort_records(users_records, "created_at")
    logger.debug(f'sorted_user_records: {sorted_user_records}')

    second_table_name = "posts"
    db.create_table(
        second_table_name,
        {
            "user_id": int,
            "title": str,
            "body": str,
            "created_at": datetime,
            "updated_at": datetime,
            "deleted_at": Union[datetime, None],
        },
    )

    logger.debug(db.tables[second_table_name].columns)

    db.create_foreign_key(second_table_name, "user_id", table_name)

    db.insert_record_into_table(
        second_table_name,
        {
            "user_id": john_record_id,
            "title": "My first post",
            "body": "This is my first post.",
            "created_at": datetime.now(tz=pytz.UTC),
            "updated_at": datetime.now(tz=pytz.UTC),
            "deleted_at": None,
        },
    )

    # logger.debug(john_record)
    # logger.debug(jane_record)
    # logger.debug(users.indexes)
    # logger.debug(users.unique_indexes)
    # logger.debug(records)
    logger.debug(db.tables[second_table_name].foreign_keys)

    db.update_record_by_id_into_table(
        second_table_name,
        1,
        {
            "user_id": john_record_id,
            "title": "My first post",
            "body": "This is my first post UPDATED!.",
            "created_at": datetime.now(tz=pytz.UTC),
            "updated_at": datetime.now(tz=pytz.UTC),
            "deleted_at": None,
        },
    )

    posts = db.get_table(second_table_name)

    posts.create_index("title")
    posts.create_index("body")

    updated_record = posts.get_record_by_id(1)
    logger.debug(updated_record)
    logger.debug(f"fk: {posts.foreign_keys}")
    logger.debug(f"indexes: {posts.indexes}")
    logger.debug(f"unique_indexes: {posts.unique_indexes}")

    posts.delete_record_by_id(1)

    posts = db.get_table(second_table_name)
    logger.debug(f"fk: {posts.foreign_keys}")
    logger.debug(f"indexes: {posts.indexes}")
    logger.debug(f"unique_indexes: {posts.unique_indexes}")

    db.drop_table(table_name)

if __name__ == "__main__":
    main()
