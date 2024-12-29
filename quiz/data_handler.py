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

def read_questions(course, category):
    # if not os.path.exists(os.path.join(os.path.dirname(__file__), "../data/"+subject+"Qs.json")):
    #     return []
    # with open(os.path.join(os.path.dirname(__file__), "../data/"+subject+"Qs.json"), "r") as file:
    #     return json.load(file)

    ''' returns the data file '''
    base_dir = "./../data/Courses"  # Root folder for all courses
    course_dir = os.path.join(base_dir, course.replace(" ", "_"))
    category_filename = os.path.join(course_dir, f"{category.replace(' ', '_')}.json")

    if not os.path.exists(category_filename):
        print(f"Error: File '{category_filename}' not found.")
        return None

    try:
        with open(category_filename, "r") as category_file:
            return json.load(category_file)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in file '{category_filename}': {e}")
        return None
