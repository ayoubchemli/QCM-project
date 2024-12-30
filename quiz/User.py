from Score import Score
from subject import Subject


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





