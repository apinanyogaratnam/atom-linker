from datetime import datetime

from database import Database


def main():
    db = Database('test')

    db.create_table(
        "users",
        {
            "first_name": str,
            "last_name": str,
            "email": str,
            "created_at": datetime,
            "updated_at": datetime,
            "deleted_at": datetime,
        },
    )

    users = db.get_table("users")

    id = users.insert_record(
        {
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@email.com",
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }
    )

    users.get_record_by_id(1)

if __name__ == "__main__":
    main()
