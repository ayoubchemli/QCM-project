from data_handler import *
from Score import Score

class takeTest:
    def __init__(self, user, course, category):
        self.user = user
        self.course = course
        self.category = category
        self.list_of_answers=[]
        self.list_of_correct_answers=self.get_correct_answers()
        self.current_test_score=0

    def get_questions(self):
        return read_questions(self.course, self.category)

    def get_number_of_questions(self):
        return len(self.get_questions())

    def get_correct_answers(self):
        """Return a list of correct answers."""
        questions = self.get_questions()
        return [question['correctAnswer'] for question in questions]

    def set_list_of_answers(self, list_of_answers):
        self.list_of_answers=list_of_answers.copy()
        self.current_test_score=self.calculate_score_in_percentage()
        self.save_score()

    def calculate_score_in_percentage(self):
        """Calculate the score % based on the user's answers."""
        correct_answers = self.list_of_correct_answers
        points = 0
        for i in range(len(self.list_of_answers)):
            if self.list_of_answers[i] == correct_answers[i]:
                points += 1
        return points/self.get_number_of_questions()*100

    def get_results_of_test(self):
        """Return the test results including score, user's answers, and correct answers. as Dics"""
        return {
            "finalScore": f'{self.current_test_score:.2f}%',
            "listOfAnswers": self.list_of_answers,
            "correctAnswers": self.list_of_correct_answers
        }

    def save_score(self):
        """Save the score to the user's profile."""
        score = Score(self.course, self.category, self.current_test_score)
        self.user.scores.append(score)
        users = read_users()

        for user in users:
            if user['username'] == self.user.username:
                user['scores'].append(score.to_dict())
                write_users(users)
                return

