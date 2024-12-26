import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve, QSize
from PyQt5.QtGui import QFont, QColor, QPainter, QPainterPath, QLinearGradient, QIcon, QKeySequence


class ScrollButton(QPushButton):
    def __init__(self, direction, parent=None):
        super().__init__(parent)
        self.direction = direction
        self.setFixedSize(50, 50)
        self.setCursor(Qt.PointingHandCursor)
        
        # Set arrow symbols based on direction
        self.setText('←' if direction == 'left' else '→')
        
        self.setStyleSheet("""
            QPushButton {
                background-color: rgba(79, 70, 229, 0.9);
                border-radius: 25px;
                color: white;
                font-size: 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(109, 40, 217, 0.9);
            }
            QPushButton:pressed {
                background-color: rgba(79, 70, 229, 0.7);
            }
        """)

class HorizontalScrollArea(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        
        # Create scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # Create container for content
        self.container = QWidget()
        self.container_layout = QHBoxLayout(self.container)
        self.container_layout.setSpacing(30)
        self.scroll_area.setWidget(self.container)
        
        # Create scroll buttons
        self.left_button = ScrollButton('left')
        self.right_button = ScrollButton('right')
        
        # Add widgets to layout
        self.layout.addWidget(self.left_button)
        self.layout.addWidget(self.scroll_area)
        self.layout.addWidget(self.right_button)
        
        # Connect buttons to scroll functions
        self.left_button.clicked.connect(self.scroll_left)
        self.right_button.clicked.connect(self.scroll_right)
        
        # Animation
        self.scroll_animation = QPropertyAnimation(self.scroll_area.horizontalScrollBar(), b"value")
        self.scroll_animation.setDuration(300)
        self.scroll_animation.setEasingCurve(QEasingCurve.OutCubic)

    def scroll_left(self):
        new_value = max(0, self.scroll_area.horizontalScrollBar().value() - 400)
        self.animate_scroll(new_value)

    def scroll_right(self):
        new_value = min(
            self.scroll_area.horizontalScrollBar().maximum(),
            self.scroll_area.horizontalScrollBar().value() + 400
        )
        self.animate_scroll(new_value)

    def animate_scroll(self, new_value):
        self.scroll_animation.setStartValue(self.scroll_area.horizontalScrollBar().value())
        self.scroll_animation.setEndValue(new_value)
        self.scroll_animation.start()

    def add_widget(self, widget):
        self.container_layout.addWidget(widget)

class ThemeToggleButton(QPushButton):
   def __init__(self, parent=None):
       super().__init__(parent)
       self.setCheckable(True)
       self.setCursor(Qt.PointingHandCursor)
       self.setFixedSize(60, 30)
       self.light_icon = "🌞"
       self.dark_icon = "🌙"
       self.setText(self.dark_icon)
       self.update_style(False)
       
   def update_style(self, is_light_mode=False):
       self.setChecked(is_light_mode)
       self.setText(self.light_icon if is_light_mode else self.dark_icon)
       style = """
           QPushButton {
               background-color: %s;
               border: 2px solid #4F46E5;
               border-radius: 15px;
               color: %s;
               font-size: 16px;
           }
           QPushButton:checked {
               background-color: %s;
               border: 2px solid #4F46E5;
               color: %s;
           }
       """ % (('#E2E8F0' if is_light_mode else '#1E293B'),
              ('black' if is_light_mode else 'white'),
              ('#1E293B' if is_light_mode else '#E2E8F0'),
              ('white' if is_light_mode else 'black'))
       self.setStyleSheet(style)

class HoverButton(QPushButton):
   def __init__(self, text):
       super().__init__(text)
       self.setFixedHeight(45)
       self.setCursor(Qt.PointingHandCursor)
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

# This version has improved UI elements, animations, and better styling 
# Copy the previous ThemeToggleButton and HoverButton classes, then add:

class GradientCard(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("courseCard")
        
        # Add shadow effect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 60))
        self.setGraphicsEffect(shadow)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        path = QPainterPath()
        path.addRoundedRect(self.rect(), 15, 15)
        
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor("#1E293B"))
        gradient.setColorAt(1, QColor("#2D3B4F"))
        
        painter.fillPath(path, gradient)

class AnimatedLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self._animation = QPropertyAnimation(self, b"geometry")
        self._animation.setDuration(200)

    def enterEvent(self, event):
        geo = self.geometry()
        self._animation.setStartValue(geo)
        self._animation.setEndValue(QRect(geo.x(), geo.y()-2, geo.width(), geo.height()))
        self._animation.start()

    def leaveEvent(self, event):
        geo = self.geometry()
        self._animation.setStartValue(geo)
        self._animation.setEndValue(QRect(geo.x(), geo.y()+2, geo.width(), geo.height()))
        self._animation.start()

def create_course_card(self, title, description, chapters, is_new=False):
    card = GradientCard()
    layout = QVBoxLayout(card)
    
    header_layout = QHBoxLayout()
    title_label = AnimatedLabel(title)
    title_label.setStyleSheet("font-size: 22px; font-weight: bold; color: white;")
    header_layout.addWidget(title_label)
    
    if is_new:
        new_badge = QLabel("New")
        new_badge.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                      stop:0 #10B981, stop:1 #059669);
            color: white;
            border-radius: 12px;
            padding: 5px 15px;
            font-weight: bold;
            margin: 5px;
        """)
        header_layout.addWidget(new_badge)
    header_layout.addStretch()
    
    desc_label = QLabel(description)
    desc_label.setWordWrap(True)
    desc_label.setStyleSheet("color: #94A3B8; font-size: 14px; margin: 10px 0;")
    
    chapters_widget = QWidget()
    chapters_layout = QVBoxLayout(chapters_widget)
    for chapter in chapters:
        chapter_label = QLabel(f"• {chapter}")
        chapter_label.setStyleSheet("color: #CBD5E1; font-size: 13px;")
        chapters_layout.addWidget(chapter_label)
    
    enroll_btn = HoverButton("Enroll Now")
    
    layout.addLayout(header_layout)
    layout.addWidget(desc_label)
    layout.addWidget(chapters_widget)
    layout.addStretch()
    layout.addWidget(enroll_btn)
    
    return card


class MCQHomePage(QMainWindow):
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
           "button_gradient": self.dark_theme["button_gradient"],
           "button_hover": self.dark_theme["button_hover"],
           "new_badge": self.dark_theme["new_badge"]
       }

   def create_course_card(self, title, description, chapters, is_new=False):
       card = QFrame()
       card.setObjectName("courseCard")
       layout = QVBoxLayout(card)
       layout.setSpacing(15)

       header = QHBoxLayout()
       title_label = QLabel(title)
       title_label.setObjectName("title")
       title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
       header.addWidget(title_label)

       if is_new:
           new_badge = QLabel("New")
           new_badge.setStyleSheet("""
               background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                   stop:0 #10B981, stop:1 #059669);
               color: white;
               border-radius: 12px;
               padding: 6px 12px;
               font-size: 14px;
               font-weight: bold;
               max-width: 60px;
           """)
           header.addWidget(new_badge)
       header.addStretch()
       layout.addLayout(header)

       desc = QLabel(description)
       desc.setObjectName("desc")
       desc.setWordWrap(True)
       desc.setStyleSheet("color: #94A3B8; font-size: 14px; line-height: 1.5;")
       layout.addWidget(desc)

       chapters_label = QLabel("Chapters:")
       chapters_label.setStyleSheet("color: #94A3B8; font-weight: bold; margin-top: 10px;")
       layout.addWidget(chapters_label)

       for chapter in chapters:
           ch_label = QLabel(f"• {chapter}")
           ch_label.setStyleSheet("color: #94A3B8; margin-left: 15px;")
           layout.addWidget(ch_label)

       layout.addStretch()
       enroll_btn = HoverButton("Enroll Now")
       layout.addWidget(enroll_btn)

       shadow = QGraphicsDropShadowEffect()
       shadow.setBlurRadius(15)
       shadow.setColor(QColor(0, 0, 0, 80))
       shadow.setOffset(0, 4)
       card.setGraphicsEffect(shadow)

       card.setStyleSheet("""
           QFrame#courseCard {
               background-color: #1E293B;
               border-radius: 20px;
               padding: 25px;
               min-height: 350px;
           }
           QFrame#courseCard:hover {
               background-color: #233043;
           }
       """)
       return card

   def apply_theme(self, is_light_mode=False):
       theme = self.light_theme if is_light_mode else self.dark_theme
       self.theme_toggle.update_style(is_light_mode)
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
       """)

   def __init__(self):
        super().__init__()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setSpacing(40)

        header = QWidget()
        header_layout = QVBoxLayout(header)
        header_layout.setSpacing(20)

        title = QLabel("Hi there 👋")
        title.setStyleSheet("""
            font-size: 48px;
            color: white;
            font-weight: bold;
            margin-bottom: 20px;
        """)

        subtitle = QLabel("Glad to see you, excited to explore our new way of learning together. Let's dive in!")
        subtitle.setStyleSheet("""
            color: #94A3B8;
            font-size: 18px;
            margin-bottom: 30px;
        """)

        header_layout.addWidget(title, alignment=Qt.AlignCenter)
        header_layout.addWidget(subtitle, alignment=Qt.AlignCenter)
        main_layout.addWidget(header)

        # Create horizontal scroll area
        self.scroll_widget = HorizontalScrollArea()
        main_layout.addWidget(self.scroll_widget)

        courses = [
                    {
                        "title": "File and data structure",
                        "description": "Master fundamental data structures and algorithms with hands-on practice.",
                        "chapters": ["Basic Data Types", "Arrays & Lists", "Trees & Graphs", "Advanced Algorithms"],
                        "is_new": False
                    },
                    {
                        "title": "Algebra",
                        "description": "Dive deep into advanced algebraic concepts and their applications.",
                        "chapters": ["Linear Algebra", "Abstract Algebra", "Number Theory", "Applications"],
                        "is_new": True
                    },
                    {
                        "title": "File and data structure",
                        "description": "Master fundamental data structures and algorithms with hands-on practice.",
                        "chapters": ["Basic Data Types", "Arrays & Lists", "Trees & Graphs", "Advanced Algorithms"],
                        "is_new": False
                    },
                    {
                        "title": "Algebra",
                        "description": "Dive deep into advanced algebraic concepts and their applications.",
                        "chapters": ["Linear Algebra", "Abstract Algebra", "Number Theory", "Applications"],
                        "is_new": True
                    },
                    {
                        "title": "File and data structure",
                        "description": "Master fundamental data structures and algorithms with hands-on practice.",
                        "chapters": ["Basic Data Types", "Arrays & Lists", "Trees & Graphs", "Advanced Algorithms"],
                        "is_new": False
                    },
                    {
                        "title": "Algebra",
                        "description": "Dive deep into advanced algebraic concepts and their applications.",
                        "chapters": ["Linear Algebra", "Abstract Algebra", "Number Theory", "Applications"],
                        "is_new": True
                    },
                    # Add more courses...
                ]
       
        for i, course in enumerate(courses):
            card = self.create_course_card(
                course["title"], 
                course["description"],
                course["chapters"],
                course["is_new"]
            )
            card.setFixedWidth(400)
            self.scroll_widget.add_widget(card)


        # Theme toggle and other settings remain the same
        self.theme_toggle = ThemeToggleButton(self)
        self.theme_toggle.move(self.width() - 120, 20)

        self.setup_themes()
        self.theme_toggle.clicked.connect(lambda: self.apply_theme(self.theme_toggle.isChecked()))
        self.apply_theme(False)

        self.shortcut = QShortcut(QKeySequence('Esc'), self)
        self.shortcut.activated.connect(self.close)

        self.setWindowTitle("Interactive Quiz Platform")
        self.showFullScreen()

   def resizeEvent(self, event):
    super().resizeEvent(event)
    self.theme_toggle.move(self.width() - 120, 20)
    margin = int(min(self.width(), self.height()) * 0.1)
    self.central_widget.layout().setContentsMargins(margin, margin, margin, margin)

if __name__ == '__main__':
   app = QApplication(sys.argv)
   font = app.font()
   font.setFamily("Segoe UI")
   app.setFont(font)
   window = MCQHomePage()
   sys.exit(app.exec_())