from datetime import datetime

class Score:
    def __init__(self, subject, score,date=None):
        self.date =date
        self.subject = subject
        self.score = round(score, 2)
        if self.date is None:
            self.date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        return f"Score(subject={self.subject}, score={self.score}, date={self.date})"

    def to_dict(self):
        """Convert the Score instance to a dictionary."""
        return {
            "subject":self.subject.to_dict(),
            "points": self.score,
            "date": self.date
        }


    # def get_score_percentage(self):
    #     return self.num_of_correct_answers/self.total_questions*100

