from datetime import datetime

from database import Database


def main():
    db = Database()

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


if __name__ == "__main__":
    main()
