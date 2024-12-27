from Score import Score
class User:
    def __init__(self, name, last_name, email, username, password, scores=None):
        if scores is None:
            scores = []
        self.name = name
        self.last_name = last_name
        self.email = email
        self.username = username
        self.password = password
        self.scores = scores

    def __str__(self):
        return f"User(name={self.name}, last_name={self.last_name}, email={self.email}, username={self.username},scores={self.scores})"

    def to_dict(self):
        """Convert the User instance to a dictionary."""
        return {
            "name": self.name,
            "lastName": self.last_name,
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
        return User(data['name'], data['lastName'], data['email'], data['username'], data['password'], scores)


    def add_scores(self, subject,points):
        return #todo


    def viwe_scores(self):
        return self.scores
    #todo chakib





