from data_handler import *
from Score import Score
from subject import Subject

class takeTest:
    def __init__(self, user, subject):
        self.user = user
        self.subject = subject
        self.list_of_answers=[]
        self.list_of_correct_answers=self.get_correct_answers()
        self.current_test_score=0

    def get_questions(self):
        """Retuns list of questions (questions+options+answer)"""
        all_chapters = Subject.get_all_chapters_of_course(self.subject.course)
        chapter = all_chapters[self.subject.chapter_id]

        questions = chapter['questions']
        return questions

    def get_number_of_questions(self):
        """Returns the number of questions in the current test"""
        all_chapters = Subject.get_all_chapters_of_course(self.subject.course)
        chapter = all_chapters[self.subject.chapter_id]
        return chapter['questions_count']

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
        score = Score(self.subject, self.current_test_score)
        self.user.scores.append(score)
        users = read_users()

        for user in users:
            if user['username'] == self.user.username:
                user['scores'].append(score.to_dict())
                write_users(users)
                return
