from datetime import datetime

class Score:
    def __init__(self, course, category, score):
        self.course = course
        self.category = category
        self.score = score
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        """Convert the Score instance to a dictionary."""
        return {
            "course": self.course,
            "category": self.category,
            "points": self.score,
            "date": self.date
        }

    # def get_score_percentage(self):
    #     return self.num_of_correct_answers/self.total_questions*100

