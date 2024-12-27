from data_handler import read_users,write_users
import hashlib
from User import User


def hash_password(password):
    return #todo

def is_valid_email(email):
    return True #todo

def verify_password_length(password):
    return #todo


def register(name,last_name,email,username,password):
    return #todo

def login(username,password):
    users = read_users()

    for user in users:
        if user['username'] == username and user['password'] == password:
            logged_in_user = User.from_dict(user)
            return logged_in_user

    return "Invalid email or password. Please try again."


