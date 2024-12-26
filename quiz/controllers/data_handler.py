import json
import os

USER_DATA_FILE = os.path.join(os.path.dirname(__file__), "../data/users.json")

def read_users():
    if not os.path.exists(USER_DATA_FILE):
        return []
    with open(USER_DATA_FILE, "r") as file:
        return json.load(file)

def write_users(users):
    with open(USER_DATA_FILE, "w") as file:
        json.dump(users, file, indent=4)

