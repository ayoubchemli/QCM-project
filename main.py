import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QTimer

from quiz.views.loginRegister import MCQApp

from quiz.login_register import login, register
from quiz.subject import Subject
from quiz.User import User
from quiz.take_test import takeTest
from quiz.AppState import AppState

def main():
    app = QApplication(sys.argv)
    appstate = AppState()
    
    # Enable high DPI scaling
    # app.setAttribute(Qt.AA_EnableHighDpiScaling)
    # app.setAttribute(Qt.AA_UseHighDpiPixmaps)
    
    # Enable smooth animations
    app.setAttribute(Qt.AA_UseStyleSheetPropagationInWidgetStyles)
    
    font_db = app.font()
    font_db.setFamily("Segoe UI")
    app.setFont(font_db)
    
    window = MCQApp(appstate)
    window.show()
    sys.exit(app.exec_())
    

    

if __name__ == "__main__":
    main()