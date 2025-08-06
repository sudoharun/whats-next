import os
import json

def get_or_create_db():
    db_file = os.path.join(os.getcwd(), "db", "data.json")

    # Create DB
    if not os.path.exists(db_file):
        db_contents = {
            "to-do": [],
            "in-progress": [],
            "done": [],
            "cancelled": []
        }

        with open(db_file, 'w') as file:
            json.dump(db_contents, file)

    # Get DB
    with open(db_file, 'r') as file:
        tasks = json.load(file)

    return tasks

# Function used to syncronize all modifications to tasks into the database, needs to be called separately
def sync_tasks(new_db_inst: dict):
    db_file = os.path.join(os.getcwd(), "db", "data.json")

    with open(db_file, "w") as file:
        json.dump(new_db_inst, file) # should probably get DB manually after this

def create_task(destination: str, content: str) -> dict:
    db = get_or_create_db()
    db[destination].append(content) # Call sync manually!
    return db

def move_task(source_addr, source_id, dest_addr):
    pass

if __name__ == "__main__":
    raise NotImplementedError("This module is not meant to be run directly.")
