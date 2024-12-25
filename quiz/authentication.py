from .data_handler import read_users, write_users

def authenticate_user(user_id, password):
    users = read_users()
    for user in users:
        if user['id'] == user_id and user['password'] == password:
            return True
    return False

def add_user(user_id, name, password):
    users = read_users()
    if any(user['id'] == user_id for user in users):
        return False
    users.append({"id": user_id, "name": name, "password": password})
    write_users(users)
    return True