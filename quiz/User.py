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
            "scores": []
        }

    @staticmethod
    def from_dict(data):
        return #todo


    def add_scores(self, subject,points):
        return #todo


    def viwe_scores(self):
        return self.scores
    #todo chakib





