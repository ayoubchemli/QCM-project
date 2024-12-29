import os
import json

# Load JSON data from a separate file
def load_json_data(file_path):
    try:
        with open(file_path, "r") as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        exit(1)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        exit(1)

# Create folders and files
def create_course_files(data):
    base_dir = "./Courses"  # Root folder for all courses

    # Ensure base directory exists
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    for course in data["courses"]:
        # Create course directory
        course_dir = os.path.join(base_dir, course["title"].replace(" ", "_"))
        os.makedirs(course_dir, exist_ok=True)

        for category in course.get("categories", []):
            # Create category file
            category_filename = os.path.join(course_dir, f"{category['title'].replace(' ', '_')}.json")
            with open(category_filename, "w") as category_file:
                json.dump(category, category_file, indent=4)

json_file_path = "./data.json"  # Path to the JSON file
data = load_json_data(json_file_path)
create_course_files(data)