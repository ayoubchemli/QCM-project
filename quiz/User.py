from Score import Score
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
        scores = [Score(score_data['course'], score_data['category'], score_data['points']) for score_data in
                  data['scores']]
        return User(data['fullname'], data['email'], data['username'], data['password'], scores)


    def add_scores(self, course, category, points):
        """Add a new score to the user's score list."""
        # If the course with same category doesn't exist, add a new Score object
        self.scores.append(Score(course, category, points))


    def view_scores(self):
        return self.scores





