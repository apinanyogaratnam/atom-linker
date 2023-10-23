import time
from datetime import datetime
from typing import Union

import pytz

from database import Database
from log import get_logger
from stats_enums import StatsType

logger = get_logger(__file__)


def main() -> None:  # sourcery skip: extract-duplicate-method
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
            "created_at": datetime, # TODO: @apinanyogaratnam: need to make a new datetime when this is not provided
            "updated_at": datetime, # TODO: @apinanyogaratnam: need to update this field when a record is updated
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

    logger.debug(f"users.indexes: {users.indexes}")
    logger.debug(f"users.unique_indexes: {users.unique_indexes}")

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
    logger.debug(f"all users_records: {users_records}")
    db.sort_records(users_records, "created_at", reverse=True)
    logger.debug(f"sorted_user_records: {users_records}")

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

    # TODO: @apinanyogaratnam: test inverted index broad search
    # TODO: @apinanyogaratnam: test out the threading of create inverted index and get records by broad search method

    posts.create_inverted_index("body")
    logger.debug(f"indexes: {posts.inverted_indexes}")

    db.shutdown()


def _create_database() -> Database:
    """Create a database instance with the name "test".

    Args:
    ----
        None

    Returns:
    -------
        Database: The database instance.
    """
    database_name = "test"

    db = Database(database_name)

    logger.debug(db)

    return db


def _create_users_table(db: Database) -> None:
    """Create a table named "users".

    This function creates a table named "users" with columns for first name, last name,
    email, created at, updated at, and deleted at. It then inserts two records into the table.

    Args:
    ----
        db (Database): The database instance.

    Returns:
    -------
        None
    """
    table_name = "users"

    db.create_table(
        table_name,
        {
            "first_name": str,
            "last_name": str,
            "email": str,
            "created_at": datetime,
            "updated_at": datetime,
            "deleted_at": Union[datetime, None],
        },
    )

    db.insert_record_into_table(
        table_name,
        {
            "first_name": "John",
            "last_name": "Doe",
            "email": "@gmail.com",
            "created_at": datetime.now(tz=pytz.UTC),
            "updated_at": datetime.now(tz=pytz.UTC),
            "deleted_at": None,
        },
    )

    db.insert_record_into_table(
        table_name,
        {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "@gmail.com",
            "created_at": datetime.now(tz=pytz.UTC),
            "updated_at": datetime.now(tz=pytz.UTC),
            "deleted_at": None,
        },
    )


def _create_post(db: Database) -> int:
    second_table_name = "posts"
    john_record_id = 1

    return db.insert_record_into_table(
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



def _create_posts_table(db: Database) -> None:
    """Create a table named "posts" with columns for user id, title, body, created at, updated at, and deleted at.

    Args:
    ----
        db (Database): The database instance.

    Returns:
    -------
        None
    """
    table_name = "users"

    db.get_table(table_name)
    john_record_id = 1

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

    db.create_foreign_key(second_table_name, "user_id", table_name)

    _create_post(db)

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


def test_inverted_index() -> None:
    """Creates an inverted index on the 'body' field of the posts table.

    The function first creates a database and tables for users and posts.
    It then gets the posts table and calls create_inverted_index() on it to build an inverted index on the 'body' field.

    The index creation is logged before and after a delay to observe any changes.

    Args:
    ----
    None

    Returns:
    -------
    None
    """
    db = _create_database()

    _create_users_table(db)

    _create_posts_table(db)

    posts = db.get_table("posts")

    posts.create_inverted_index("body")

    logger.debug(f"inverted_indexes: {posts.inverted_indexes}")

    time.sleep(5)

    logger.debug(f"inverted_indexes: {posts.inverted_indexes}")

    db.shutdown()


def test_index() -> None:
    """Creates an index on the 'body' field of the posts table.

    The function first creates a database and tables for users and posts.
    It then gets the posts table and calls create_index() on it to build an index on the 'body' field.

    The index creation is logged before and after a delay to observe any changes.

    Args:
    ----
    None

    Returns:
    -------
    None
    """
    db = _create_database()

    _create_users_table(db)

    _create_posts_table(db)

    posts = db.get_table("posts")

    for _ in range(1000):
        _create_post(db)

    posts.create_index("body")

    logger.debug(f"indexes: {posts.indexes}")

    time.sleep(5)

    logger.debug(f"indexes: {posts.indexes}")

    for i in range(1000000):
        record_id = _create_post(db)
        # if len(posts.records_to_index['body']) > 0:
        #     logger.debug(f"records to index: {posts.records_to_index}")

        if i % 100 == 0:
            posts.get_records_by_column("body", "This is my first post.")
            # logger.debug(f"records: {len(records)}")

            start_time = time.perf_counter()
            posts.update_record_by_id(
                record_id,
                {
                    "user_id": 1,
                    "title": "My first post",
                    "body": "This is my first post. UPDATED!!!!!!!!!",
                    "created_at": datetime.now(tz=pytz.UTC),
                    "updated_at": datetime.now(tz=pytz.UTC),
                    "deleted_at": None,
                },
            )
            end_time = time.perf_counter()
            time_taken = end_time - start_time
            if time_taken > 1:
                logger.debug(f"update_record_by_id took: {end_time - start_time}")
                logger.debug(f"indexes: {posts.indexes}")

            start_time = time.perf_counter()
            posts.delete_record_by_id(record_id)
            end_time = time.perf_counter()
            time_taken = end_time - start_time
            if time_taken > 1:
                logger.debug(f"delete_record_by_id took: {end_time - start_time}")

    time.sleep(5)

    logger.debug(f"indexes: {posts.indexes}")

    logger.debug(f"threads stats: {posts.stats.get(StatsType.THREADS)}")

    db.shutdown()


if __name__ == "__main__":
    # main()
    # test_inverted_index()
    test_index()
