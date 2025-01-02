from .Score import Score
from .subject import Subject
import json
import csv
from datetime import datetime


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

    def view_scores(self):
        return self.scores
    

   

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
    