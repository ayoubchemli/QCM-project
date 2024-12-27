from data_handler import read_users,write_users
import hashlib
from User import User


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def is_valid_email(email):
    return True #todo

def verify_password_length(password):
    return bool(len(password)>8)


def register(name,last_name,email,username,password):
    users = read_users()

    if not is_valid_email(email): return "Invalid email! Please try again."

    for user in users:
        if user['email'] == email:
            return "Email already exists! Please try a different one."
        if user['username'] == username:
            return "Username already exists! Please try a different one."

    if not verify_password_length(password):
        return "Password must be at least 8 characters long! Please try again."

    new_user = User (name,last_name,email,username,hash_password(password))

    users.append(new_user.to_dict())
    write_users(users)
    return new_user

def login(username,password):
    users = read_users()

    for user in users:
        if user['username'] == username and user['password'] == password:
            logged_in_user = User.from_dict(user)
            return logged_in_user

    return "Invalid email or password. Please try again."


