from .Score import Score
from .subject import Subject
from .data_handler import read_users, write_users
import json
import csv
from datetime import datetime
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


class User:
    def __init__(self, fullname, email, username, password, scores=None):
        if scores is None:
            scores = []
        self.fullname = fullname
        self.email = email
        self.username = username
        self.password = password
        self.scores = scores

    def __str__(self):
        return f"User(full_name={self.fullname}, email={self.email}, username={self.username},scores={self.scores})"

    def to_dict(self):
        """Convert the User instance to a dictionary."""
        return {
            "fullname": self.fullname,
            "email": self.email,
            "username": self.username,
            "password": self.password,
            "scores": [Score(score.course, score.category, score.score).to_dict() for score in self.scores]
        }

    @staticmethod
    def from_dict(data):
        """Create a User instance from a dictionary."""
        scores = []
        for score_data in data.get('scores', []):
            subject_data = score_data.get('subject', {})
            course = subject_data.get('course')
            chapter_id = subject_data.get('chapter_id')
            chapter = subject_data.get('chapter')

            subject = Subject(course, chapter_id, chapter)

            score = Score(subject, score_data['points'], score_data.get('date'))
            scores.append(score.to_dict())

        return User(
            fullname=data.get('fullname', ''),
            email=data.get('email', ''),
            username=data.get('username', ''),
            password=data.get('password', ''),
            scores=scores
        )

    def get_scores(self):
        users = read_users()
        for user in users:
            if user['username'] == self.username:
                return user['scores']

    def count_tests_taken(self):
        scores = self.get_scores()
        return len(scores)

    def calculate_average_score(self):
        scores = self.get_scores()
        if not scores:
            return 0
        total_points = sum(score['points'] for score in scores)
        return round(total_points / len(scores), 2)
    
    def get_best_score(self):
        scores = self.get_scores()
        if not scores:
            return None
        max1 = max(scores, key=lambda x: x['points'])
        return max1['points']

    def count_tests_this_month(self):
        scores = self.get_scores()
        current_month = datetime.now().month
        current_year = datetime.now().year
        return sum(1 for score in scores if datetime.strptime(score['date'], "%Y-%m-%d %H:%M:%S").month == current_month and datetime.strptime(score['date'], "%Y-%m-%d %H:%M:%S").year == current_year)
        
    def mcq_history(self):
        scores = self.get_scores()
        formatted_scores = []
        for score in scores:
            date = str(score['date'])
            course = str(score['subject']['course'])
            chapter = str(score['subject']['chapter'])
            points = str(score['points'])
            status = "Passed" if score['points'] >= 50 else "Failed"
            formatted_scores.append((date, course, chapter, points, status))
        return formatted_scores

    def change_password(self, old_password, new_password):
        old_hashed_password = hash_password(old_password)
        new_hashed_password = hash_password(new_password)
        users = read_users()
        for user in users:
            if user['username'] == self.username:
                if user['password'] == old_hashed_password:
                    user['password'] = new_hashed_password
                else:
                    return False
                break
        write_users(users)
        return True

    def change_email(self, new_email):
        users = read_users()
        for user in users:
            if user['username'] == self.username:
                user['email'] = new_email
                break
        write_users(users)
        return True
    

   

def export_user_scores(username):
    """
    Extract scores data for a specific username and save to CSV.
    
    Args:
        username (str): Username to search for
    
    Returns:
        bool: True if successful, False if user not found
    """
    try:
        # Read JSON file
        with open('users.json', 'r') as file:
            data = json.load(file)
        
        # Find user
        user_data = None
        for user in data:
            if user['username'] == username:
                user_data = user
                break
        
        if user_data is None:
            print(f"User '{username}' not found.")
            return False
        
        # Extract scores
        scores = user_data['scores']
        if not scores:
            print(f"No scores found for user '{username}'.")
            return False
            
        # Write to CSV
        output_csv_file = f"{username}_scores.csv"
        with open(output_csv_file, 'w', newline='') as file:
            writer = csv.writer(file)
            # Write header
            writer.writerow(['Course', 'Chapter', 'Points', 'Date'])
            
            # Write scores
            for score in scores:
                writer.writerow([
                    score['subject']['course'],
                    score['subject']['chapter'],
                    score['points'],
                    score['date']
                ])
        
        print(f"Scores exported successfully to {username}_scores.csv")
        return True
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False    
   
         # to emplement : export_user_scores("op")
    