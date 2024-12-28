from Score import Score
import csv
from typing import List

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
            "scores": [score.to_dict() for score in self.scores]
        }

    @staticmethod
    def from_dict(data):
        """Create a User instance from a dictionary."""
        scores = [Score(score_data['subject'], score_data['points']) for score_data in
                  data['scores']]
        return User(data['fullName'], data['email'], data['username'], data['password'], scores)
    

    @staticmethod
    def export_users_to_csv(users: List['User'], filename: str) -> None:
        """
        Export a list of User objects to a CSV file with separate columns for each score.
        
        Args:
            users: List of User objects to export
            filename: Name of the CSV file to create
        """
        
        subjects = set()
        for user in users:
            for score in user.scores:
                subjects.add(score.subject)
        subjects = sorted(list(subjects))
        
        
        headers = ['Full Name', 'Email', 'Username'] + subjects
        
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            
            writer.writerow(headers)
            
            
            for user in users:
                
                score_dict = {score.subject: score.points for score in user.scores}
                
            
                row = [
                    user.fullname,
                    user.email,
                    user.username
                ]
                
                
                for subject in subjects:
                    row.append(score_dict.get(subject, ''))
                
                writer.writerow(row)




    def add_scores(self, subject,points):
        return #todo


    def viwe_scores(self):
        return self.scores
    #todo chakib





