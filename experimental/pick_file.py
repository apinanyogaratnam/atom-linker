import pickle
import os


def save_database_object_to_pickle_file(db: object, name: str) -> None:
    if not os.path.exists("data"):
        os.mkdir("data")

    if not os.path.exists("data/databases"):
        os.mkdir("data/databases")

    pickle_file_name = f"data/databases/{name}.pickle"
    pickle_file = open(pickle_file_name, "wb")
    pickle.dump(db, pickle_file)
