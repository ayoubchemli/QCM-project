import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from quiz.views.loginRegister import MCQApp
# from quiz.views.Homepage import MCQHomePage
from quiz.views.quizesLevel import quizesLevel
from quiz.views.MCQPage import MCQPage
from quiz.AppState import AppState
from quiz.login_register import login, register
from quiz.subject import Subject
from quiz.User import User
from quiz.take_test import takeTest


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # self.setWindowTitle("QCM Application")
        # self.setGeometry(100, 100, 800, 600)


        
        

        appstate = AppState()

        user = login("dzdm", "adam2005")
        appstate.setUser(user)

        chapters = Subject.get_all_chapters_of_course("Cyber Security") # tsra fl home page
        appstate.setCourse("Cyber Security") # tsra fl home page
        chapters = Subject.get_all_chapters_of_course(appstate.getCourse())
        appstate.setChapterID(0)

        # chapter_id = appstate.getChapterID()
        # course = appstate.getCourse()
        # chapter_name = Subject.get_all_chapters_of_course(course)[chapter_id]['title']

        # subject = Subject(course, chapter_id, chapter_name)

        # test_instance = takeTest(user, subject)

        # questions = test_instance.get_questions()

        # appstate.setQuestions(questions)
        
        # Initialize all pages
        self.login_page = MCQApp(appstate)
        # self.homepage = Homepage()
        # self.quizesLevel = quizesLevel(appstate, chapters)
        # self.MCQPage = MCQPage(questions)

        # Add pages to the stacked widget
        # self.stacked_widget.addWidget(self.login_page)
        # self.stacked_widget.addWidget(self.homepage)
        self.stacked_widget = QStackedWidget()
        appstate.setStacked_widget(self.stacked_widget)
        self.stacked_widget.addWidget(self.login_page)
        # self.stacked_widget.addWidget(self.MCQPage)

        # Set initial page
        self.setCentralWidget(self.stacked_widget)
        self.stacked_widget.setCurrentIndex(0)  # Start at the login page

    def closeEvent(self, event):
        print("Application closed.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    font_db = app.font()
    font_db.setFamily("Segoe UI")
    app.setFont(font_db)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())