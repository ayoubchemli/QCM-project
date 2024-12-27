import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve, QSize
from PyQt5.QtGui import QFont, QColor, QPainter, QPainterPath, QLinearGradient, QIcon, QKeySequence



class CustomDropdownMenu(QMenu):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_menu()
        
    def setup_menu(self):
        self.setFont(QFont('Segoe UI', 11))
        self.update_theme(False)  # Default to dark theme
        self.add_default_items()

    def update_theme(self, is_light_mode):
        if is_light_mode:
            self.setStyleSheet("""
                QMenu {
                    background-color: white;
                    border: 2px solid #E2E8F0;
                    border-radius: 15px;
                    padding: 8px;
                    min-width: 200px;
                }
                QMenu::item {
                    padding: 12px 24px;
                    color: #2D3748;
                    border-radius: 8px;
                    margin: 2px 5px;
                }
                QMenu::item:selected {
                    background-color: #F7FAFC;
                    color: #2D3748;
                }
                QMenu::separator {
                    height: 2px;
                    background: #E2E8F0;
                    margin: 6px 15px;
                }
            """)
        else:
            self.setStyleSheet("""
                QMenu {
                    background-color: #1E293B;
                    border: 2px solid #2D3748;
                    border-radius: 15px;
                    padding: 8px;
                    min-width: 200px;
                }
                QMenu::item {
                    padding: 12px 24px;
                    color: #E0E0E0;
                    border-radius: 8px;
                    margin: 2px 5px;
                }
                QMenu::item:selected {
                    background-color: #2D3748;
                    color: #FFFFFF;
                }
                QMenu::separator {
                    height: 2px;
                    background: #2D3748;
                    margin: 6px 15px;
                }
            """)

        
    def add_default_items(self):
        actions = {
            "👤 Profile": "View Profile and History",
            "📊 MCQ History": "View Past Test Scores",
            "💾 Export Results": "Export Results to File",
            "📞 Contact": "Contact Us",
            "❌ Sign out": "Account Access"
        }

        for icon_text, tooltip in actions.items():
            if icon_text == "❌ Sign out":
                self.addSeparator()
            action = self.addAction(icon_text)
            action.setToolTip(tooltip)

class CustomDropdownButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__("☰", parent)
        self.setup_button()
        self.setup_menu()
        
    def setup_button(self):
        self.setFixedSize(70, 65)
        self.setFont(QFont('Segoe UI', 16))
        self.update_theme(False)  # Default to dark theme

    def update_theme(self, is_light_mode):
        if is_light_mode:
            self.setStyleSheet("""
                QPushButton {
                    background-color: white;
                    color: #2D3748;
                    font-weight: bold;
                    border: 2px solid #E2E8F0;
                    border-radius: 25px;
                    padding: 5px;
                    margin: 10px;
                }
                QPushButton:hover {
                    background-color: #F7FAFC;
                    border-color: #CBD5E0;
                    color: #2D3748;
                    transition: all 0.3s ease;
                }
                QPushButton:pressed {
                    background-color: #EDF2F7;
                    border-color: #CBD5E0;
                    padding: 6px 4px 4px 6px;
                }
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #1E293B;
                    color: #E0E0E0;
                    font-weight: bold;
                    border: 2px solid #2D3748;
                    border-radius: 25px;
                    padding: 5px;
                    margin: 10px;
                }
                QPushButton:hover {
                    background-color: #2D3748;
                    border-color: #4A5568;
                    color: #FFFFFF;
                    transition: all 0.3s ease;
                }
                QPushButton:pressed {
                    background-color: #374151;
                    border-color: #4A5568;
                    padding: 6px 4px 4px 6px;
                }
            """)
        
    def setup_menu(self):
        self.menu = CustomDropdownMenu(self)
        self.setMenu(self.menu)
        
    def add_custom_action(self, text, tooltip="", callback=None):
        """Add a custom action to the menu"""
        action = self.menu.addAction(text)
        action.setToolTip(tooltip)
        if callback:
            action.triggered.connect(callback)
            
    def add_separator(self):
        """Add a separator to the menu"""
        self.menu.addSeparator()

class ScrollButton(QPushButton):
    def __init__(self, direction, parent=None):
        super().__init__(parent)
        self.direction = direction
        self.setFixedSize(45, 45)  # Slightly smaller for elegance
        self.setCursor(Qt.PointingHandCursor)
        
        # Set arrow symbols based on direction using more elegant unicode arrows
        self.setText('❮' if direction == 'left' else '❯')
        
        # Create animation for hover effect
        self._animation = QPropertyAnimation(self, b"geometry")
        self._animation.setDuration(150)
        
        self.setStyleSheet("""
            QPushButton {
                background-color: rgba(79, 70, 229, 0.15);
                border: 2px solid rgba(79, 70, 229, 0.8);
                border-radius: 22px;
                color: rgba(79, 70, 229, 1);
                font-size: 18px;
                font-weight: bold;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: rgba(79, 70, 229, 1);
                border: 2px solid rgba(79, 70, 229, 1);
                color: white;
            }
            QPushButton:pressed {
                background-color: rgba(67, 56, 202, 1);
                border: 2px solid rgba(67, 56, 202, 1);
                color: white;
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
            "main_bg": "background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #FFFFFF, stop:1 #F0F4F8)",
            "card_bg": "#FFFFFF",
            "text_primary": "#2D3748",  # Darker text for better contrast
            "text_secondary": "#4A5568", # Warmer gray for secondary text
            "button_gradient": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4F46E5, stop:1 #7C3AED)", # Keeping the button gradient
            "button_hover": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4338CA, stop:1 #6D28D9)",
            "new_badge": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #10B981, stop:1 #059669)"
        }

   def create_course_card(self, title, description, chapters, is_new=False):
    card = QFrame()
    card.setObjectName("courseCard")
    layout = QVBoxLayout(card)
    layout.setSpacing(15)

    header = QHBoxLayout()
    title_label = QLabel(title)
    title_label.setObjectName("title")
    # Remove the hardcoded color here - let the theme handle it
    title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
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
    # Remove hardcoded color here too
    desc.setStyleSheet("font-size: 14px; line-height: 1.5;")
    layout.addWidget(desc)

    chapters_label = QLabel("Chapters:")
    # Remove hardcoded color
    chapters_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
    layout.addWidget(chapters_label)

    for chapter in chapters:
        ch_label = QLabel(f"• {chapter}")
        ch_label.setProperty("class", "chapter")  # Add a class property for styling
        # Remove hardcoded color
        ch_label.setStyleSheet("margin-left: 15px;")
        layout.addWidget(ch_label)

    layout.addStretch()
    enroll_btn = HoverButton("Enroll Now")
    layout.addWidget(enroll_btn)

    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(15)
    shadow.setColor(QColor(0, 0, 0, 80))
    shadow.setOffset(0, 4)
    card.setGraphicsEffect(shadow)

    # Remove hardcoded colors from card styling
    card.setStyleSheet("""
        QFrame#courseCard {
            border-radius: 20px;
            padding: 25px;
            min-height: 350px;
        }
    """)
    return card

   def apply_theme(self, is_light_mode=False):
    theme = self.light_theme if is_light_mode else self.dark_theme
    self.theme_toggle.update_style(is_light_mode)
    
    # Update dropdown menu and button themes
    self.dropdown_button.update_theme(is_light_mode)
    self.dropdown_button.menu.update_theme(is_light_mode)
    
    # Main window and scrollbar styling
    self.setStyleSheet(f"""
        QMainWindow {{
            {theme["main_bg"]};
        }}
        QScrollArea {{
            border: none;
            background-color: transparent;
        }}
        QScrollBar:horizontal {{
            height: 8px;
            background: rgba(0, 0, 0, 0.1);
            border-radius: 4px;
            margin: 0px;
        }}
        QScrollBar::handle:horizontal {{
            background: #4F46E5;
            border-radius: 4px;
            min-width: 40px;
        }}
        QScrollBar::handle:horizontal:hover {{
            background: #6D28D9;
        }}
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
            width: 0px;
        }}
    """)

    # Card styling based on theme
    if is_light_mode:
        card_style = """
            QFrame#courseCard {
                background-color: white;
                border-radius: 20px;
                padding: 25px;
                min-height: 350px;
                border: 1px solid #E2E8F0;
            }
            QFrame#courseCard:hover {
                background-color: #F8FAFC;
            }
            QFrame#courseCard QLabel#title {
                color: #2D3748;
                font-size: 24px;
                font-weight: bold;
            }
            QFrame#courseCard QLabel#desc {
                color: #4A5568;
                font-size: 14px;
                line-height: 1.5;
            }
            QFrame#courseCard QLabel {
                color: #4A5568;
            }
            QFrame#courseCard QLabel[class="chapter"] {
                color: #4A5568;
                margin-left: 15px;
            }
        """
    else:
        card_style = """
            QFrame#courseCard {
                background-color: #1E293B;
                border-radius: 20px;
                padding: 25px;
                min-height: 350px;
            }
            QFrame#courseCard:hover {
                background-color: #233043;
            }
            QFrame#courseCard QLabel#title {
                color: white;
                font-size: 24px;
                font-weight: bold;
            }
            QFrame#courseCard QLabel#desc {
                color: #94A3B8;
                font-size: 14px;
                line-height: 1.5;
            }
            QFrame#courseCard QLabel {
                color: #94A3B8;
            }
            QFrame#courseCard QLabel[class="chapter"] {
                color: #94A3B8;
                margin-left: 15px;
            }
        """

    # Apply card styling to all course cards
    for card in self.findChildren(QFrame, "courseCard"):
        card.setStyleSheet(card_style)

    # Update title and subtitle styling
    title_style = f"color: {theme['text_primary']}; font-size: 48px; font-weight: bold; margin-bottom: 20px;"
    subtitle_style = f"color: {theme['text_secondary']}; font-size: 18px; margin-bottom: 30px;"
    
    for label in self.findChildren(QLabel):
        if label.text().startswith("welcome"):
            label.setStyleSheet(title_style)
        elif label.text().startswith("Glad to see you"):
            label.setStyleSheet(subtitle_style)

   def __init__(self):
        super().__init__()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setSpacing(40)
        
        # Create header container
        header_container = QWidget()
        header_layout = QHBoxLayout(header_container)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(0)

        # Add dropdown button to the left
        self.dropdown_button = CustomDropdownButton()
        header_layout.addWidget(self.dropdown_button, alignment=Qt.AlignLeft | Qt.AlignTop)

        
        # Optional: Add custom actions with callbacks
        self.dropdown_button.add_custom_action("⚙️ Settings", "Open Settings", self.open_settings)

        # Create center content container
        center_content = QWidget()
        center_layout = QVBoxLayout(center_content)
        center_layout.setSpacing(20)

        title = QLabel("welcome (name)")
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

        center_layout.addWidget(title, alignment=Qt.AlignCenter)
        center_layout.addWidget(subtitle, alignment=Qt.AlignCenter)
        center_layout.setAlignment(Qt.AlignCenter)

        # Add center content to header layout with stretch
        header_layout.addWidget(center_content, 1)

        # Add empty widget for right side balance (matches dropdown width)
        spacer = QWidget()
        spacer.setFixedSize(70, 65)
        header_layout.addWidget(spacer)

        main_layout.addWidget(header_container)

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
            }
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

        # Theme toggle and other settings
        self.theme_toggle = ThemeToggleButton(self)
        self.theme_toggle.move(self.width() - 120, 20)

        self.setup_themes()
        self.theme_toggle.clicked.connect(lambda: self.apply_theme(self.theme_toggle.isChecked()))
        self.apply_theme(False)

        self.shortcut = QShortcut(QKeySequence('Esc'), self)
        self.shortcut.activated.connect(self.close)

        self.setWindowTitle("Interactive Quiz Platform")
        self.showFullScreen()

   def open_settings(self):
        # Example callback function
        print("Settings opened")
    
   def resizeEvent(self, event):
    super().resizeEvent(event)
    self.theme_toggle.move(self.width() - 120, 20)
    margin = int(min(self.width(), self.height()) * 0.1)
    self.central_widget.layout().setContentsMargins(20, 20, margin, margin)
    
    
if __name__ == '__main__':
   app = QApplication(sys.argv)
   font = app.font()
   font.setFamily("Segoe UI")
   app.setFont(font)
   window = MCQHomePage()
   sys.exit(app.exec_())