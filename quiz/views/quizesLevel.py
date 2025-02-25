import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QLabel, QPushButton, QScrollArea,
                           QGraphicsDropShadowEffect, QFrame, QGridLayout,
                           QSizePolicy, QShortcut)
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve, QSize
from PyQt5.QtGui import QFont, QColor, QPainter, QPainterPath, QLinearGradient, QIcon, QKeySequence
from PyQt5.QtWidgets import QLineEdit, QMenu

import quiz.views.MCQPage
from quiz.AppState import AppState
from quiz.subject import Subject
from quiz.User import User
from quiz.take_test import takeTest





class ThemeToggleButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCheckable(True)
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedSize(60, 30)
        
        # Create icons for light/dark mode
        self.light_icon = "🌞"
        self.dark_icon = "🌙"
        self.setText(self.dark_icon)

        # Initial style
        self.update_style(False)

        
    def update_style(self, is_light_mode=False):
        self.setChecked(is_light_mode)  # Synchronize button state with theme
        self.setText(self.light_icon if is_light_mode else self.dark_icon)
        
        if is_light_mode:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #E2E8F0;
                    border: 2px solid #4F46E5;
                    border-radius: 15px;
                    color: black;
                    font-size: 16px;
                }
                QPushButton:checked {
                    background-color: #1E293B;
                    border: 2px solid #4F46E5;
                    color: white;
                }
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #1E293B;
                    border: 2px solid #4F46E5;
                    border-radius: 15px;
                    color: white;
                    font-size: 16px;
                }
                QPushButton:checked {
                    background-color: #E2E8F0;
                    border: 2px solid #4F46E5;
                    color: black;
                }
            """)
        

class HoverButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setFixedHeight(45)
        self.setCursor(Qt.PointingHandCursor)
        
        # Animation for hover effect
        self._animation = QPropertyAnimation(self, b"geometry")
        self._animation.setDuration(150)
        
        self.setStyleSheet("""
            HoverButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                          stop:0 #4F46E5, stop:1 #7C3AED);
                color: white;
                border: none;
                border-radius: 22px;
                font-weight: bold;
                font-size: 14px;
                padding: 10px 20px;
            }
            HoverButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                          stop:0 #4338CA, stop:1 #6D28D9);
            }
        """)

    def enterEvent(self, event):
        geo = self.geometry()
        self._animation.setStartValue(geo)
        self._animation.setEndValue(QRect(geo.x()-2, geo.y()-2, 
                                        geo.width()+4, geo.height()+4))
        self._animation.setEasingCurve(QEasingCurve.OutQuad)
        self._animation.start()

    def leaveEvent(self, event):
        geo = self.geometry()
        self._animation.setStartValue(geo)
        self._animation.setEndValue(QRect(geo.x()+2, geo.y()+2, 
                                        geo.width()-4, geo.height()-4))
        self._animation.setEasingCurve(QEasingCurve.OutQuad)
        self._animation.start()

class CategoryCard(QFrame):
    def __init__(self, title, description, chapters, questions_count, time_estimate, difficulty, is_new=False, on_start=None):
        super().__init__()
        self.setMinimumSize(600, 200)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        # Main layout
        layout = QHBoxLayout()
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)
        self.setLayout(layout)
        
        # Add shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 50))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)
        
        # Style
        self.setStyleSheet("""
            CategoryCard {
                background-color: #1E293B;
                border-radius: 15px;
            }
            QLabel {
                color: white;
            }
        """)
        
        # Left section with title and description
        left_section = QVBoxLayout()
        
        # Header with title and badge
        header_layout = QHBoxLayout()
        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 22, QFont.Bold))
        header_layout.addWidget(title_label)
        
        if is_new:
            new_badge = QLabel("NEW")
            new_badge.setStyleSheet("""
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                          stop:0 #10B981, stop:1 #059669);
                color: white;
                padding: 4px 12px;
                border-radius: 10px;
                font-size: 12px;
                font-weight: bold;
                margin-left: 15px;
            """)
            header_layout.addWidget(new_badge)
        header_layout.addStretch()
        left_section.addLayout(header_layout)
        
        # Description
        desc_label = QLabel(description)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("color: #94A3B8; font-size: 14px; margin-top: 5px;")
        left_section.addWidget(desc_label)
        
        # Quiz info
        info_layout = QHBoxLayout()
        
        # Questions count
        questions_label = QLabel(f"🎯 {questions_count} Questions")
        questions_label.setStyleSheet("color: #94A3B8; font-size: 13px;")
        info_layout.addWidget(questions_label)
        
        # Time estimate
        time_label = QLabel(f"⏱️ {time_estimate}")
        time_label.setStyleSheet("color: #94A3B8; font-size: 13px;")
        info_layout.addWidget(time_label)
        
        # Difficulty
        difficulty_label = QLabel(f"📊 {difficulty}")
        difficulty_label.setStyleSheet("color: #94A3B8; font-size: 13px;")
        info_layout.addWidget(difficulty_label)
        
        info_layout.addStretch()
        left_section.addLayout(info_layout)
        
        layout.addLayout(left_section, stretch=2)
        
        # Right section with button
        right_section = QVBoxLayout()
        right_section.setAlignment(Qt.AlignCenter)
        
        start_button = HoverButton("Start Quiz")
        if on_start:
            start_button.clicked.connect(on_start)
        right_section.addWidget(start_button)
        
        layout.addLayout(right_section, stretch=1)

class quizesLevel(QMainWindow):
    
    def setup_themes(self):
        self.dark_theme = {
            "main_bg": "background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #0F172A, stop:1 #1E293B)",
            "card_bg": "#1E293B",
            "text_primary": "white",
            "text_secondary": "#94A3B8",
            "button_gradient": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4F46E5, stop:1 #7C3AED)",
            "button_hover": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4338CA, stop:1 #6D28D9)",
            "new_badge": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #10B981, stop:1 #059669)"
        }
        
        self.light_theme = {
            "main_bg": "background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #F8FAFC, stop:1 #E2E8F0)",
            "card_bg": "white",
            "text_primary": "#1E293B",
            "text_secondary": "#475569",
            "button_gradient": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4F46E5, stop:1 #7C3AED)",
            "button_hover": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4338CA, stop:1 #6D28D9)",
            "new_badge": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #10B981, stop:1 #059669)"
        }

    def theme_toggle_clicked(self):
        is_light_mode = self.appstate.getThemeToggle().isChecked()
        self.apply_theme(is_light_mode)
            
    def __init__(self, appstate, is_light_mode=False):
        super().__init__()
        self.appstate = appstate
        
        
        # Show fullscreen after creating UI elements
        self.showFullScreen()
        
        # Setup themes first
        self.setup_themes()
        
        self.theme_toggle = self.appstate.getThemeToggle()
        self.theme_toggle.clicked.connect(self.theme_toggle_clicked)

        
        # Central widget setup
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(30)
        
        # Header section with back button
        header_layout = QHBoxLayout()
        back_button = HoverButton("← Return to Home")
        back_button.setFixedWidth(200)
        back_button.clicked.connect(self.return_to_home)
        header_layout.addWidget(back_button)
        header_layout.addStretch()
        main_layout.addLayout(header_layout)
        
        # Welcome section - Create labels before applying theme
        welcome_layout = QVBoxLayout()
        
        self.greeting_label = QLabel(appstate.getCourse())
        self.greeting_label.setFont(QFont("Segoe UI", 40, QFont.Bold))
        welcome_layout.addWidget(self.greeting_label, alignment=Qt.AlignCenter)
        
        self.subtitle_label = QLabel("Choose a level to test your knowledge")
        self.subtitle_label.setFont(QFont("Segoe UI", 16))
        welcome_layout.addWidget(self.subtitle_label, alignment=Qt.AlignCenter)
        
        main_layout.addLayout(welcome_layout)
        
        # Scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Container for cards
        cards_widget = QWidget()
        cards_layout = QVBoxLayout(cards_widget)
        cards_layout.setContentsMargins(20, 20, 20, 20)
        cards_layout.setSpacing(20)
        cards_layout.setAlignment(Qt.AlignHCenter)

        categories = Subject.get_all_chapters_of_course(appstate.getCourse())
        
        for category in categories:
            chapter_id = int(category["chapter_id"]) 
            card = CategoryCard(
                category["title"],
                category["description"],
                [],  # chapters not shown in this design
                category["questions_count"],
                category["time_estimate"],
                category["difficulty"],
                category["is_new"],
                on_start=self.create_on_start_handler(chapter_id),
            )
            cards_layout.addWidget(card)
        
        cards_layout.addStretch()
        scroll_area.setWidget(cards_widget)
        main_layout.addWidget(scroll_area)
        
        # Add escape shortcut
        self.shortcut = QShortcut(QKeySequence('Esc'), self)
        self.shortcut.activated.connect(self.close)
        
        # Apply theme after all widgets are created
        self.apply_theme(is_light_mode)
        
        
    def return_to_home(self):
        # Get the parent QStackedWidget
        stacked_widget = self.parent()
        # Return to the home screen (index 0)
        stacked_widget.setCurrentIndex(0)
        

    def apply_theme(self, is_light_mode=False):
        theme = self.light_theme if is_light_mode else self.dark_theme
        
        # Update main window style
        self.setStyleSheet(f"""
            QMainWindow {{
                {theme["main_bg"]};
            }}
            QScrollArea {{
                border: none;
                background-color: transparent;
            }}
            QScrollBar:vertical {{
                width: 8px;
                background: rgba(0, 0, 0, 0.1);
                border-radius: 4px;
                margin: 0px;
            }}
            QScrollBar::handle:vertical {{
                background: #4F46E5;
                border-radius: 4px;
                min-height: 40px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: #6D28D9;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
            HoverButton {{
                background: {theme["button_gradient"]};
                color: white;
                border: none;
                border-radius: 22px;
                font-weight: bold;
                font-size: 14px;
                padding: 10px 20px;
            }}
            HoverButton:hover {{
                background: {theme["button_hover"]};
            }}
        """)
        
        # Update category cards
        for card in self.findChildren(CategoryCard):
            card.setStyleSheet(f"""
                CategoryCard {{
                    background-color: {theme["card_bg"]};
                    border-radius: 15px;
                }}
                QLabel {{
                    color: {theme["text_primary"]};
                }}
            """)
            
            # Update description and info labels
            for label in card.findChildren(QLabel):
                if "margin-top: 5px;" in label.styleSheet() or "font-size: 13px;" in label.styleSheet():
                    label.setStyleSheet(f"color: {theme['text_secondary']}; {label.styleSheet()}")
        
        # Update welcome section labels
        if self.greeting_label and self.subtitle_label:
            self.greeting_label.setStyleSheet(f"""
                color: {theme["text_primary"]};
                margin-bottom: 10px;
            """)
            self.subtitle_label.setStyleSheet(f"color: {theme['text_secondary']};")

    def create_on_start_handler(self, chapter_id):
        def on_start():
            self.start_quiz(chapter_id)
        return on_start

    def start_quiz(self, chapter_id):
        self.appstate.setChapterID(chapter_id)
        user = self.appstate.getUser()
        course = self.appstate.getCourse()
        chapter_name = Subject.get_all_chapters_of_course(course)[chapter_id]['title']
        subject = Subject(course, chapter_id, chapter_name)
        test_instance = takeTest(user, subject)
        self.appstate.setTestInstance(test_instance)
        questions = test_instance.get_questions()
        self.appstate.setQuestions(questions)
        
        # Pass the current theme state and appstate to MCQPage
        is_light_mode = self.theme_toggle.isChecked()      
        self.MCQPage = quiz.views.MCQPage.MCQPage(self.appstate, is_light_mode)
        # Add a reference to the theme toggle
        # self.MCQPage.theme_toggle = self.theme_toggle
        # self.MCQPage.theme_toggle.clicked.connect(lambda: (self.MCQPage.apply_theme(self.theme_toggle.isChecked())))
        
        parent = self.parent()
        parent.addWidget(self.MCQPage)
        parent.setCurrentIndex(2)

        

    def resizeEvent(self, event):
        super().resizeEvent(event)
        central_widget = self.centralWidget()
        if central_widget and self.centralWidget().layout():
            width = self.width()
            height = self.height()
            margin = min(width, height) * 0.1
            central_widget.layout().setContentsMargins(margin, margin, margin, margin)
        # Update positions
        #self.theme_toggle.move(self.width() - 120, 20)

    


    # self.close()
        
        
