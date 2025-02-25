import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import re
import json
import os

from quiz.login_register import login, register
from quiz.User import User
from .homePage import MCQHomePage

class EnhancedFancyLineEdit(QLineEdit):
    def __init__(self, placeholder_text, validator_type=None, parent=None):
        super().__init__(parent)
        self.validator_type = validator_type
        self.setPlaceholderText(placeholder_text)
        self.setup_animations()
        self.setup_styling()
        self.textChanged.connect(self.validate)
        
    def setup_animations(self):
        # Size animation for focus
        self.size_animation = QPropertyAnimation(self, b"geometry")
        self.size_animation.setDuration(200)
        
        # Border animation
        self.border_animation = QPropertyAnimation(self, b"styleSheet")
        self.border_animation.setDuration(300)
        
    def setup_styling(self):
        self.setStyleSheet("""
            QLineEdit {
                padding: 15px;
                background: rgba(255, 255, 255, 0.2);
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 10px;
                color: white;
                font-size: 16px;
                font-family: 'Poppins';
            }
            QLineEdit:focus {
                background: rgba(255, 255, 255, 0.3);
                border: 2px solid rgba(255, 255, 255, 0.5);
            }
        """)

    def validate(self):
        text = self.text()
        valid = False

        if self.validator_type == "fullname":
            valid = " " in text.strip()
        elif self.validator_type == "email":
            valid = re.match(r"[^@]+@[^@]+\.[^@]+", text) is not None
        elif self.validator_type == "password":
            has_upper = any(c.isupper() for c in text)
            has_lower = any(c.islower() for c in text)
            has_digit = any(c.isdigit() for c in text)
            has_special = any(not c.isalnum() for c in text)
            valid = len(text) >= 8 and has_digit and (has_upper or has_lower or has_special)
        elif self.validator_type == "confirm password":
            parent_widget = self.parent()
            while parent_widget and not hasattr(parent_widget, 'reg_password_input'):
                parent_widget = parent_widget.parent()
            if parent_widget and hasattr(parent_widget, 'reg_password_input'):
                valid = text == parent_widget.reg_password_input.text()
            else:
                valid = False
        elif self.validator_type == "username":
            valid = len(text) >= 4 and text.isalnum()
        else:
            valid = len(text) > 0

        self.update_validation_style(valid)
        return valid


    def update_validation_style(self, valid):
        if self.text():
            if valid:
                color = "#4CAF50"  # Green
            else:
                color = "#FF5252"  # Red
                
            self.setStyleSheet(f"""
                QLineEdit {{
                    padding: 15px;
                    background: rgba(255, 255, 255, 0.2);
                    border: 2px solid {color};
                    border-radius: 10px;
                    color: white;
                    font-size: 16px;
                    font-family: 'Poppins';
                }}
                QLineEdit:focus {{
                    background: rgba(255, 255, 255, 0.3);
                }}
            """)
        else:
            self.setup_styling()

    def focusInEvent(self, event):
        rect = self.geometry()
        self.size_animation.setStartValue(rect)
        self.size_animation.setEndValue(QRect(rect.x()-5, rect.y(), rect.width()+10, rect.height()))
        self.size_animation.start()
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        rect = self.geometry()
        self.size_animation.setStartValue(rect)
        self.size_animation.setEndValue(QRect(rect.x()+5, rect.y(), rect.width()-10, rect.height()))
        self.size_animation.start()
        super().focusOutEvent(event)

class PasswordStrengthIndicator(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        self.strength_bar = QProgressBar()
        self.strength_bar.setMaximum(100)
        self.strength_bar.setTextVisible(False)
        self.strength_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 5px;
                height: 6px;
            }
            QProgressBar::chunk {
                border-radius: 5px;
            }
        """)
        
        self.strength_label = QLabel("Password Strength")
        self.strength_label.setStyleSheet("color: white; font-size: 12px;")
        
        layout.addWidget(self.strength_label)
        layout.addWidget(self.strength_bar)
        
    def update_strength(self, password):
        strength = 0
        feedback = []
        
        if len(password) >= 8:
            strength += 25
            feedback.append("Length ✓")
        if any(c.isupper() for c in password):
            strength += 25
            feedback.append("Uppercase ✓")
        if any(c.isdigit() for c in password):
            strength += 25
            feedback.append("Number ✓")
        if any(not c.isalnum() for c in password):
            strength += 25
            feedback.append("Special char ✓")
            
        self.strength_bar.setValue(strength)
        
        if strength <= 25:
            color = "#FF5252"  # Red
            text = "Weak"
        elif strength <= 50:
            color = "#FFC107"  # Yellow
            text = "Medium"
        elif strength <= 75:
            color = "#2196F3"  # Blue
            text = "Strong"
        else:
            color = "#4CAF50"  # Green
            text = "Very Strong"
            
        self.strength_bar.setStyleSheet(f"""
            QProgressBar {{
                border: none;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 5px;
                height: 6px;
            }}
            QProgressBar::chunk {{
                background: {color};
                border-radius: 5px;
            }}
        """)
        
        self.strength_label.setText(f"Password Strength: {text}\n{' | '.join(feedback)}")

class AnimatedButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        # Store the original geometry
        self._original_geometry = None
        self._animation = QPropertyAnimation(self, b"geometry")
        self._animation.setDuration(100)
        self._animation.setEasingCurve(QEasingCurve.OutCubic)
        
        # Connect animation finished signal to ensure proper reset
        self._animation.finished.connect(self._on_animation_finished)
        
    def showEvent(self, event):
        # Store the original geometry when the button is first shown
        if self._original_geometry is None:
            self._original_geometry = self.geometry()
        super().showEvent(event)

    def enterEvent(self, event):
        if self._original_geometry is None:
            self._original_geometry = self.geometry()
            
        current_rect = self._original_geometry
        self._animation.setStartValue(current_rect)
        self._animation.setEndValue(QRect(
            current_rect.x() - 5,
            current_rect.y() - 5,
            current_rect.width() + 10,
            current_rect.height() + 10
        ))
        self._animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        if self._original_geometry is None:
            self._original_geometry = self.geometry()
            
        current_rect = self.geometry()
        self._animation.setStartValue(current_rect)
        self._animation.setEndValue(self._original_geometry)
        self._animation.start()
        super().leaveEvent(event)
        
    def _on_animation_finished(self):
        # When leaving animation finishes, ensure we're at original geometry
        if not self.underMouse():
            self.setGeometry(self._original_geometry)
        
        
class SuccessMessage(QFrame):
    def __init__(self, username):
        super().__init__()
        self.setup_ui(username)
        
    def setup_ui(self, username):
        # Set frame style
        self.setStyleSheet("""
            QFrame {
                background: rgba(76, 175, 80, 0.1);
                border: 1px solid #4CAF50;
                border-radius: 8px;
                padding: 15px;
                margin: 10px;
            }
        """)
        
        # Create layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(12)
        
        # Create success icon
        self.icon_label = QLabel("✓")
        self.icon_label.setStyleSheet("""
            font-size: 20px;
            color: #4CAF50;
            font-weight: bold;
        """)
        
        # Create welcome message
        message_label = QLabel(f"Welcome back, {username}!")
        message_label.setStyleSheet("""
            color: #4CAF50;
            font-size: 16px;
            font-weight: 500;
            letter-spacing: 0.3px;
        """)
        
        # Add widgets to layout
        layout.addWidget(self.icon_label)
        layout.addWidget(message_label)
        layout.addStretch()

class FancyLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setProperty("class", "fancy")
        self._animation = QPropertyAnimation(self, b"geometry")
        self._animation.setDuration(200)

    def focusInEvent(self, event):
        rect = self.geometry()
        self._animation.setStartValue(rect)
        self._animation.setEndValue(QRect(rect.x()-5, rect.y(), 
                                        rect.width()+10, rect.height()))
        self._animation.start()
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        rect = self.geometry()
        self._animation.setStartValue(rect)
        self._animation.setEndValue(QRect(rect.x()+5, rect.y(), 
                                        rect.width()-10, rect.height()))
        self._animation.start()
        super().focusOutEvent(event)
        
class PageTransitionManager:
    def __init__(self, login_page, home_page):
        self.login_page = login_page
        self.home_page = home_page
        self.setup_animations()
        
    def setup_animations(self):
        # Fade out animation for login page
        self.login_fade_out = QPropertyAnimation(self.login_page, b"windowOpacity")
        self.login_fade_out.setDuration(800)
        self.login_fade_out.setEasingCurve(QEasingCurve.InOutQuad)
        self.login_fade_out.setStartValue(1.0)
        self.login_fade_out.setEndValue(0.0)
        
        # Slide up animation for home page
        self.home_slide_up = QPropertyAnimation(self.home_page, b"geometry")
        self.home_slide_up.setDuration(1000)
        self.home_slide_up.setEasingCurve(QEasingCurve.OutExpo)
        
        # Fade in animation for home page
        self.home_fade_in = QPropertyAnimation(self.home_page, b"windowOpacity")
        self.home_fade_in.setDuration(800)
        self.home_fade_in.setEasingCurve(QEasingCurve.InOutQuad)
        self.home_fade_in.setStartValue(0.0)
        self.home_fade_in.setEndValue(1.0)
        
    def start_transition(self):
        # Set initial state
        self.home_page.setWindowOpacity(0.0)
        screen = QApplication.primaryScreen().geometry()
        
        # Set initial and final positions for slide animation
        start_rect = QRect(0, screen.height(), screen.width(), screen.height())
        end_rect = QRect(0, 0, screen.width(), screen.height())
        self.home_slide_up.setStartValue(start_rect)
        self.home_slide_up.setEndValue(end_rect)
        
        # Create parallel animation group
        self.parallel_group = QParallelAnimationGroup()
        self.parallel_group.addAnimation(self.login_fade_out)
        self.parallel_group.addAnimation(self.home_slide_up)
        self.parallel_group.addAnimation(self.home_fade_in)
        
        # Connect finished signal
        self.parallel_group.finished.connect(self.finish_transition)
        
        # Show home page and start animations
        self.home_page.showFullScreen()
        self.parallel_group.start()
        
    def finish_transition(self):
        self.login_page.close()

class MCQApp(QMainWindow):
    
    def create_registration_page(self):
        registration_page = QWidget()
        layout = QVBoxLayout(registration_page)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(15)
        
        # Create glass-morphism container
        container = QFrame()
        self.container = container
        container.setObjectName("glassContainer")
        container.setStyleSheet("""
            #glassContainer {
                background: rgba(255, 255, 255, 0.15);
                border-radius: 25px;
                border: 2px solid rgba(255, 255, 255, 0.2);
            }
        """)
        
        # Enhanced shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(QColor(0, 0, 0, 80))
        container.setGraphicsEffect(shadow)
        
        # Main container layout is now horizontal
        container_layout = QHBoxLayout(container)
        self.container_layout = container_layout
        container_layout.setContentsMargins(40, 40, 40, 40)
        container_layout.setSpacing(30)

        # Left column for form inputs
        left_column = QVBoxLayout()
        left_column.setSpacing(10)
        
        # Title section
        title_label = QLabel("Create Account")
        title_label.setFont(QFont('Poppins', 32, QFont.Bold))
        title_label.setStyleSheet("color: white;")
        title_label.setAlignment(Qt.AlignLeft)
        
        subtitle_label = QLabel("Join Our Learning Community")
        subtitle_label.setFont(QFont('Poppins', 14))
        subtitle_label.setStyleSheet("color: rgba(255, 255, 255, 0.8);")
        subtitle_label.setAlignment(Qt.AlignLeft)
        
        # Input fields container
        inputs_container = QFrame()
        inputs_layout = QVBoxLayout(inputs_container)
        inputs_layout.setSpacing(10)
        inputs_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create input field containers
        # Full Name
        fullname_container = QFrame()
        fullname_layout = QVBoxLayout(fullname_container)
        fullname_layout.setContentsMargins(0, 0, 0, 0)
        fullname_layout.setSpacing(3)
        
        fullname_label = QLabel("Full Name")
        fullname_label.setFont(QFont('Poppins', 12))
        fullname_label.setStyleSheet("color: white;")
        
        fullname_input_container = QHBoxLayout()
        fullname_icon = QLabel()
        fullname_icon.setPixmap(QIcon(":/icons/user.png").pixmap(24, 24))
        self.fullname_input = EnhancedFancyLineEdit("Enter your full name", "fullname")
        
        fullname_input_container.addWidget(fullname_icon)
        fullname_input_container.addWidget(self.fullname_input)
        
        fullname_layout.addWidget(fullname_label)
        fullname_layout.addLayout(fullname_input_container)
        
        # Email
        email_container = QFrame()
        email_layout = QVBoxLayout(email_container)
        email_layout.setContentsMargins(0, 0, 0, 0)
        email_layout.setSpacing(3)
        
        email_label = QLabel("Email Address")
        email_label.setFont(QFont('Poppins', 12))
        email_label.setStyleSheet("color: white;")
        
        email_input_container = QHBoxLayout()
        email_icon = QLabel()
        email_icon.setPixmap(QIcon(":/icons/email.png").pixmap(24, 24))
        self.email_input = EnhancedFancyLineEdit("Enter your email address", "email")
        
        email_input_container.addWidget(email_icon)
        email_input_container.addWidget(self.email_input)
        
        email_layout.addWidget(email_label)
        email_layout.addLayout(email_input_container)
        
        # Username
        username_container = QFrame()
        username_layout = QVBoxLayout(username_container)
        username_layout.setContentsMargins(0, 0, 0, 0)
        username_layout.setSpacing(3)
        
        username_label = QLabel("Username")
        username_label.setFont(QFont('Poppins', 12))
        username_label.setStyleSheet("color: white;")
        
        username_input_container = QHBoxLayout()
        username_icon = QLabel()
        username_icon.setPixmap(QIcon(":/icons/user.png").pixmap(24, 24))
        self.reg_username_input = EnhancedFancyLineEdit("Choose a username", "username")
        
        username_input_container.addWidget(username_icon)
        username_input_container.addWidget(self.reg_username_input)
        
        username_layout.addWidget(username_label)
        username_layout.addLayout(username_input_container)
        
        # Password
        password_container = QFrame()
        password_layout = QVBoxLayout(password_container)
        password_layout.setContentsMargins(0, 0, 0, 0)
        password_layout.setSpacing(3)
        
        password_label = QLabel("Password")
        password_label.setFont(QFont('Poppins', 12))
        password_label.setStyleSheet("color: white;")
        
        password_input_container = QHBoxLayout()
        password_icon = QLabel()
        password_icon.setPixmap(QIcon(":/icons/lock.png").pixmap(24, 24))
        self.reg_password_input = EnhancedFancyLineEdit("Create a password", "password")
        self.reg_password_input.setEchoMode(QLineEdit.Password)
        
        password_input_container.addWidget(password_icon)
        password_input_container.addWidget(self.reg_password_input)
        
        password_layout.addWidget(password_label)
        password_layout.addLayout(password_input_container)
        
        # Password Strength Indicator
        self.password_strength = PasswordStrengthIndicator()
        self.reg_password_input.textChanged.connect(self.password_strength.update_strength)
        
        # Confirm Password
        confirm_password_container = QFrame()
        confirm_password_layout = QVBoxLayout(confirm_password_container)
        confirm_password_layout.setContentsMargins(0, 0, 0, 0)
        confirm_password_layout.setSpacing(3)
        
        confirm_password_label = QLabel("Confirm Password")
        confirm_password_label.setFont(QFont('Poppins', 12))
        confirm_password_label.setStyleSheet("color: white;")
        
        confirm_password_input_container = QHBoxLayout()
        confirm_password_icon = QLabel()
        confirm_password_icon.setPixmap(QIcon(":/icons/lock.png").pixmap(24, 24))
        self.confirm_password_input = EnhancedFancyLineEdit("Confirm your password", "confirm password")

        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        
        confirm_password_input_container.addWidget(confirm_password_icon)
        confirm_password_input_container.addWidget(self.confirm_password_input)
        
        confirm_password_layout.addWidget(confirm_password_label)
        confirm_password_layout.addLayout(confirm_password_input_container)
        
        self.reg_password_input.textChanged.connect(
            lambda: self.confirm_password_input.validate()
        )
        self.confirm_password_input.textChanged.connect(
            lambda: self.confirm_password_input.validate()
        )
        
        # Add all inputs to the inputs container
        inputs_layout.addWidget(fullname_container)
        inputs_layout.addWidget(email_container)
        inputs_layout.addWidget(username_container)
        inputs_layout.addWidget(password_container)
        inputs_layout.addWidget(self.password_strength)
        inputs_layout.addWidget(confirm_password_container)
        
        # Buttons at the bottom
        buttons_container = QVBoxLayout()
        buttons_container.setSpacing(15)
        
        register_button = AnimatedButton("Create Account")
        register_button.setFont(QFont('Poppins', 14, QFont.Bold))
        register_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #FF512F, stop:1 #DD2476);
                color: white;
                padding: 15px;
                border: none;
                border-radius: 10px;
                min-width: 200px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #FF6B6B, stop:1 #FF3C85);
            }
        """)
        register_button.clicked.connect(self.handle_registration)
        
        back_button = AnimatedButton("Already have an account? Login here")
        back_button.setFont(QFont('Poppins', 12))
        back_button.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: rgba(255, 255, 255, 0.8);
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 10px;
                padding: 12px;
                min-width: 200px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.1);
                border-color: rgba(255, 255, 255, 0.3);
            }
        """)
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        
        buttons_container.addWidget(register_button, alignment=Qt.AlignCenter)
        buttons_container.addWidget(back_button, alignment=Qt.AlignCenter)
        
        # Add elements to left column
        left_column.addWidget(title_label)
        left_column.addWidget(subtitle_label)
        left_column.addSpacing(20)
        left_column.addWidget(inputs_container)
        left_column.addStretch()
        left_column.addLayout(buttons_container)
        
        # Right column for validation messages
        right_column = QVBoxLayout()
        right_column.setSpacing(15)
        
        # Validation status container
        self.validation_container = QFrame()
        self.validation_container.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.1);
                border-radius: 15px;
                padding: 20px;
                min-width: 300px;
            }
        """)
        validation_layout = QVBoxLayout(self.validation_container)
        
        validation_title = QLabel("Registration Status")
        validation_title.setFont(QFont('Poppins', 16, QFont.Bold))
        validation_title.setStyleSheet("color: white;")
        
        self.validation_list = QVBoxLayout()
        self.validation_list.setSpacing(10)
        
        validation_layout.addWidget(validation_title)
        validation_layout.addLayout(self.validation_list)
        validation_layout.addStretch()
        
        # Error container
        self.error_container = QFrame()
        self.error_layout = QVBoxLayout(self.error_container)
        self.error_container.hide()
        
        # Add to right column
        right_column.addWidget(self.validation_container)
        right_column.addWidget(self.error_container)
        right_column.addStretch()
        
        # Add both columns to container
        left_widget = QWidget()
        left_widget.setLayout(left_column)
        right_widget = QWidget()
        right_widget.setLayout(right_column)
        
        # Set the ratio of left to right columns (60:40)
        container_layout.addWidget(left_widget, 60)
        container_layout.addWidget(right_widget, 40)
        
        # Add container to main layout
        layout.addWidget(container)
        
        # Footer
        footer_label = QLabel("© 2024 USTHB Computer Science. Made with ❤️")
        footer_label.setFont(QFont('Poppins', 10))
        footer_label.setStyleSheet("color: rgba(255, 255, 255, 0.7);")
        footer_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(footer_label)
        
        self.stacked_widget.addWidget(registration_page)
        
        # Add slide-in animation for the container
        self.registration_animation = QPropertyAnimation(container, b"pos")
        self.registration_animation.setDuration(500)
        self.registration_animation.setStartValue(QPoint(self.width(), 0))
        self.registration_animation.setEndValue(QPoint(0, 0))
        self.registration_animation.setEasingCurve(QEasingCurve.OutCubic)
        self.registration_animation.start()

    def validate_registration_form(self):
        self.clear_error_messages()
        errors = []
        
        # Get the absolute path to users.json
        current_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        users_file_path = os.path.join(current_dir, 'data', 'users.json')

        # Validate full name (minimum 2 words, alphabetic)
        fullname = self.fullname_input.text().strip()
        if len(fullname.split()) < 2 or not all(word.isalpha() for word in fullname.split()):
            errors.append("Please enter your full name (first and last name)")
            self.fullname_input.update_validation_style(False)

        # Validate email
        if not self.email_input.validate():
            errors.append("Please enter a valid email address")
            
        # Validate username (minimum 4 chars, alphanumeric)
        username = self.reg_username_input.text().strip()
        if not self.reg_username_input.validate():
            errors.append("Username must be at least 4 characters long and contain only letters and numbers")
        else:
            # Check if username already exists
            try:
                with open(users_file_path, 'r') as file:
                    users = json.loads(file.read())
                    username = self.reg_username_input.text().strip()
                    if any(user['username'].lower() == username.lower() for user in users):
                        errors.append("Username is already taken")
                        self.reg_username_input.update_validation_style(False)
            except FileNotFoundError:
                errors.append("Error: Unable to validate username. Please try again later.")
                print(f"Could not find users.json at: {users_file_path}")
                    
        # Validate password
        if not self.reg_password_input.validate():
            errors.append("Password must be at least 8 characters and contain uppercase, lowercase, number, and special character")
            
        # Validate password match
        if self.reg_password_input.text() != self.confirm_password_input.text():
            errors.append("Passwords do not match")
            self.confirm_password_input.update_validation_style(False)

        if errors:
            self.show_error_messages(errors)
            return False
            
        return True

    def show_error_messages(self, messages):
        self.clear_error_messages()
        
        for message in messages:
            error_frame = QFrame()
            error_frame.setStyleSheet("""
                QFrame {
                    background: rgba(255, 82, 82, 0.1);
                    border-left: 4px solid #FF5252;
                    border-radius: 5px;
                    padding: 12px;
                    margin-bottom: 8px;
                }
            """)
            
            error_layout = QHBoxLayout(error_frame)
            error_layout.setContentsMargins(12, 8, 12, 8)
            
            icon_label = QLabel("⚠️")
            icon_label.setStyleSheet("font-size: 16px;")
            
            error_label = QLabel(message)
            error_label.setStyleSheet("""
                color: #FF5252;
                font-size: 14px;
                font-weight: bold;
            """)
            error_label.setWordWrap(True)
            
            error_layout.addWidget(icon_label)
            error_layout.addWidget(error_label, 1)
            
            self.error_layout.addWidget(error_frame)
        
        self.error_container.show()

    def clear_error_messages(self):
        while self.error_layout.count():
            item = self.error_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.error_container.hide()

    def handle_registration(self):
        if hasattr(self, '_registration_in_progress') and self._registration_in_progress:
            return
            
        self._registration_in_progress = True
        
        if self.validate_registration_form():
            # Simulate checking for existing username/email
            self.disable_form_inputs(True)
            QTimer.singleShot(1000, lambda: self.complete_registration())
        else:
            self._registration_in_progress = False
            
            if not hasattr(self, '_shake_animation_running') or not self._shake_animation_running:
                self._shake_animation_running = True
                current_pos = self.container.pos()
                shake_animation = QPropertyAnimation(self.container, b"pos")
                shake_animation.setDuration(100)
                shake_animation.setLoopCount(3)
                
                for i in range(shake_animation.loopCount()):
                    shake_animation.setKeyValueAt(i/shake_animation.loopCount(), 
                        QPoint(current_pos.x() + (10 if i % 2 == 0 else -10), current_pos.y()))
                shake_animation.setEndValue(current_pos)
                
                def finish_shake():
                    self._shake_animation_running = False
                
                shake_animation.finished.connect(finish_shake)
                shake_animation.start()

    def complete_registration(self):
        try:
            # Get form data
            fullname = self.fullname_input.text().strip()
            email = self.email_input.text().strip()
            username = self.reg_username_input.text().strip()
            password = self.reg_password_input.text().strip()

            user = register(fullname, email, username, password)
            if isinstance(user, User):
                print(f"Registration successful! Welcome, {user.fullname}!")
                # If registration is successful, show success message
                success_frame = QFrame()
                success_frame.setStyleSheet("""
                    QFrame {
                        background: rgba(76, 175, 80, 0.1);
                        border: 1px solid #4CAF50;
                        border-radius: 5px;
                        padding: 10px;
                    }
                """)
                
                success_layout = QVBoxLayout(success_frame)
                
                success_label = QLabel("✓ Registration Successful!")
                success_label.setStyleSheet("""
                    color: #4CAF50;
                    font-size: 18px;
                    font-weight: bold;
                """)
                success_layout.addWidget(success_label)
                
                self.error_layout.addWidget(success_frame)
                self.error_container.show()
                
                # Re-enable form inputs
                self.disable_form_inputs(False)
                
                # Wait 2 seconds then clear form and return to login page
                QTimer.singleShot(2000, lambda: [
                    self.clear_form(),
                    self.stacked_widget.setCurrentIndex(0)
                ])
            else:
                raise Exception(user)
            
        except Exception as e:
            # Handle registration errors
            error_message = f"Registration failed: {str(e)}"
            self.show_error_messages([error_message])
            self.disable_form_inputs(False)
        
        finally:
            self._registration_in_progress = False

    def disable_form_inputs(self, disabled):
        self.fullname_input.setDisabled(disabled)
        self.email_input.setDisabled(disabled)
        self.reg_username_input.setDisabled(disabled)
        self.reg_password_input.setDisabled(disabled)
        self.confirm_password_input.setDisabled(disabled)

    def clear_form(self):
        self.fullname_input.clear()
        self.email_input.clear()
        self.reg_username_input.clear()
        self.reg_password_input.clear()
        self.confirm_password_input.clear()
        self.clear_error_messages()

      
        
    def __init__(self, appstate):
        super().__init__()
        self.appstate = appstate
        self.setWindowTitle("Computer Science MCQ")
        self.setMinimumSize(1200, 800)
        
        # Apply custom font
        QFontDatabase.addApplicationFont(":/fonts/Poppins-Regular.ttf")
        QFontDatabase.addApplicationFont(":/fonts/Poppins-Bold.ttf")
        
        # Set window style
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1A2980, stop:1 #26D0CE);
            }
        """)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(60, 60, 60, 60)
        
        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)
        
        self.create_login_page()
        self.create_registration_page()
        self.showFullScreen()
        
        self.shortcut = QShortcut(QKeySequence('Esc'), self)
        self.shortcut.activated.connect(self.close)

    def create_login_page(self):
        login_page = QWidget()
        layout = QVBoxLayout(login_page)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(40)
        
        # Create glass-morphism container
        container = QFrame()
        container.setObjectName("glassContainer")
        container.setStyleSheet("""
            #glassContainer {
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 20px;
                border: 2px solid rgba(255, 255, 255, 0.1);
            }
        """)
        
        # Add shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(QColor(0, 0, 0, 60))
        container.setGraphicsEffect(shadow)
        
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(30)
        container_layout.setContentsMargins(40, 40, 40, 40)
        
        # Logo and title section
        logo_label = QLabel()
        logo_label.setPixmap(QIcon(":/images/logo.png").pixmap(100, 100))
        logo_label.setAlignment(Qt.AlignCenter)
        
        title_label = QLabel("Computer Science MCQ")
        title_label.setFont(QFont('Poppins', 36, QFont.Bold))
        title_label.setStyleSheet("color: white;")
        title_label.setAlignment(Qt.AlignCenter)
        
        subtitle_label = QLabel("Enhance Your Knowledge Through Interactive Learning")
        subtitle_label.setFont(QFont('Poppins', 16))
        subtitle_label.setStyleSheet("color: rgba(255, 255, 255, 0.8);")
        subtitle_label.setAlignment(Qt.AlignCenter)
        
        # Username input with icon
        username_container = QFrame()
        username_layout = QHBoxLayout(username_container)
        username_layout.setContentsMargins(0, 0, 0, 0)
        
        username_icon = QLabel()
        username_icon.setPixmap(QIcon(":/icons/user.png").pixmap(24, 24))
        
        self.username_input = FancyLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setStyleSheet("""
            QLineEdit {
                padding: 15px;
                background: rgba(255, 255, 255, 0.2);
                border: none;
                border-radius: 10px;
                color: white;
                font-size: 16px;
                font-family: 'Poppins';
            }
            QLineEdit:focus {
                background: rgba(255, 255, 255, 0.3);
            }
        """)
        
        username_layout.addWidget(username_icon)
        username_layout.addWidget(self.username_input)

        # Password input with icon
        password_container = QFrame()
        password_layout = QHBoxLayout(password_container)
        password_layout.setContentsMargins(0, 0, 0, 0)

        password_icon = QLabel()
        password_icon.setPixmap(QIcon(":/icons/lock.png").pixmap(24, 24))

        self.password_input = FancyLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("""
            QLineEdit {
                padding: 15px;
                background: rgba(255, 255, 255, 0.2);
                border: none;
                border-radius: 10px;
                color: white;
                font-size: 16px;
                font-family: 'Poppins';
            }
            QLineEdit:focus {
                background: rgba(255, 255, 255, 0.3);
            }
        """)

        password_layout.addWidget(password_icon)
        password_layout.addWidget(self.password_input)
        
        # Buttons
        start_button = AnimatedButton("Start Your Journey")
        start_button.setFont(QFont('Poppins', 14, QFont.Bold))
        start_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #FF512F, stop:1 #DD2476);
                color: white;
                padding: 15px;
                border: none;
                border-radius: 10px;
                min-width: 250px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #FF6B6B, stop:1 #FF3C85);
            }
        """)
        start_button.clicked.connect(self.handle_login)
        
        guest_button = AnimatedButton("New member? Registration here")
        guest_button.setFont(QFont('Poppins', 12))
        guest_button.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: rgba(255, 255, 255, 0.8);
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 10px;
                padding: 12px;
                min-width: 200px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.1);
                border-color: rgba(255, 255, 255, 0.3);
            }
        """)
        guest_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        
        # Add all elements to container
        container_layout.addWidget(logo_label)
        container_layout.addWidget(title_label)
        container_layout.addWidget(subtitle_label)
        container_layout.addWidget(username_container)
        container_layout.addWidget(password_container)
        container_layout.addWidget(start_button, alignment=Qt.AlignCenter)
        container_layout.addWidget(guest_button, alignment=Qt.AlignCenter)
        
        # Add container to main layout
        layout.addWidget(container)
        
        # Footer
        footer_label = QLabel("© 2024 USTHB Computer Science. Made with ♥")
        footer_label.setFont(QFont('Poppins', 10))
        footer_label.setStyleSheet("color: rgba(255, 255, 255, 0.7);")
        footer_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(footer_label)
        
        self.stacked_widget.addWidget(login_page)
        
    def handle_login(self):
        # Disable login button and show loading state
        start_button = self.findChild(AnimatedButton, "start_button")
        if start_button:
            original_text = start_button.text()
            start_button.setText("Logging in...")
            start_button.setEnabled(False)

        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        # Input validation
        validation_errors = []
        
        if not username:
            validation_errors.append("Username is required")
            self.username_input.setStyleSheet("""
                QLineEdit {
                    padding: 15px;
                    background: rgba(255, 82, 82, 0.2);
                    border: 2px solid #FF5252;
                    border-radius: 10px;
                    color: white;
                    font-size: 16px;
                    font-family: 'Poppins';
                }
            """)
        
        if not password:
            validation_errors.append("Password is required")
            self.password_input.setStyleSheet("""
                QLineEdit {
                    padding: 15px;
                    background: rgba(255, 82, 82, 0.2);
                    border: 2px solid #FF5252;
                    border-radius: 10px;
                    color: white;
                    font-size: 16px;
                    font-family: 'Poppins';
                }
            """)

        if validation_errors:
            self.show_login_error("\n".join(validation_errors))
            if start_button:
                start_button.setText(original_text)
                start_button.setEnabled(True)
            return

        try:
            # Attempt login
            user = login(username, password)

            if isinstance(user, User):
                self.appstate.setUser(user)
                self.login_successful(user)
            else:
                error_message = self.get_login_error_message(user)
                self.show_login_error(error_message)
                self.handle_failed_login_attempt()

        except Exception as e:
            error_message = self.handle_login_exception(e)
            self.show_login_error(error_message)
            if start_button:
                start_button.setText(original_text)
                start_button.setEnabled(True)

    def get_login_error_message(self, error):
        """Convert login error responses to user-friendly messages"""
        error_messages = {
            "Invalid credentials": "Incorrect username or password",
            "Account locked": "Your account has been locked due to too many failed attempts",
            "Account not verified": "Please verify your email address before logging in",
            "Account disabled": "Your account has been disabled. Please contact support",
            "Database error": "We're experiencing technical difficulties. Please try again later"
        }
        return error_messages.get(error, "Login failed. Please try again")

    def handle_login_exception(self, exception):
        """Handle different types of login exceptions"""
        if "connection" in str(exception).lower():
            return "Unable to connect to server. Please check your internet connection"
        elif "timeout" in str(exception).lower():
            return "Server is taking too long to respond. Please try again"
        elif "database" in str(exception).lower():
            return "Database error occurred. Please try again later"
        else:
            return f"An unexpected error occurred: {str(exception)}"

    def show_login_error(self, message):
        """Display error message with improved visual feedback"""
        # Create error frame if it doesn't exist
        if not hasattr(self, 'error_frame'):
            self.error_frame = QFrame()
            self.error_frame.setStyleSheet("""
                QFrame {
                    background: rgba(255, 82, 82, 0.1);
                    border-left: 4px solid #FF5252;
                    border-radius: 5px;
                    margin-top: 10px;
                    margin-bottom: 10px;
                }
            """)
            
            error_layout = QHBoxLayout(self.error_frame)
            error_layout.setContentsMargins(12, 8, 12, 8)
            
            self.error_icon = QLabel("⚠️")
            self.error_icon.setStyleSheet("font-size: 16px;")
            
            self.error_label = QLabel()
            self.error_label.setStyleSheet("""
                color: #FF5252;
                font-size: 14px;
                font-weight: bold;
            """)
            self.error_label.setWordWrap(True)
            
            error_layout.addWidget(self.error_icon)
            error_layout.addWidget(self.error_label, 1)
            
            # Find container and add error frame
            container = self.username_input.parent().parent()
            layout = container.layout()
            layout.insertWidget(layout.count()-2, self.error_frame)
            
        # Update error message
        self.error_label.setText(message)
        self.error_frame.show()
        
        # Shake animation for error feedback
        if not hasattr(self, '_shake_animation_running') or not self._shake_animation_running:
            self._shake_animation_running = True
            current_pos = self.error_frame.pos()
            shake_animation = QPropertyAnimation(self.error_frame, b"pos")
            shake_animation.setDuration(100)
            shake_animation.setLoopCount(3)
            
            for i in range(shake_animation.loopCount()):
                shake_animation.setKeyValueAt(i/shake_animation.loopCount(), 
                    QPoint(current_pos.x() + (10 if i % 2 == 0 else -10), current_pos.y()))
            shake_animation.setEndValue(current_pos)
            
            def finish_shake():
                self._shake_animation_running = False
            
            shake_animation.finished.connect(finish_shake)
            shake_animation.start()

        # Auto-hide error after 5 seconds
        QTimer.singleShot(5000, lambda: self.error_frame.hide())

    def handle_failed_login_attempt(self):
        """Track and handle failed login attempts"""
        if not hasattr(self, '_failed_attempts'):
            self._failed_attempts = 0
        
        self._failed_attempts += 1
        
        if self._failed_attempts >= 5:
            # Lock login for 5 minutes
            self.lock_login(60)  # 60 seconds = 1 minutes
        

    def lock_login(self, duration):
        """Temporarily lock login functionality"""
        self.username_input.setEnabled(False)
        self.password_input.setEnabled(False)
        start_button = self.findChild(AnimatedButton, "start_button")
        if start_button:
            start_button.setEnabled(False)
        
        # Create countdown timer
        if not hasattr(self, '_lock_timer'):
            self._lock_timer = duration
            self._countdown = QTimer()
            self._countdown.timeout.connect(self.update_lock_countdown)
            self._countdown.start(1000)  # Update every second
            
        self.show_login_error(f"Too many failed attempts. Please try again in {duration} seconds")

    def update_lock_countdown(self):
        """Update the login lock countdown"""
        self._lock_timer -= 1
        if self._lock_timer <= 0:
            # Unlock login
            self.username_input.setEnabled(True)
            self.password_input.setEnabled(True)
            start_button = self.findChild(AnimatedButton, "start_button")
            if start_button:
                start_button.setEnabled(True)
            self._countdown.stop()
            self.error_frame.hide()
            self._failed_attempts = 0
        else:
            self.show_login_error(f"Too many failed attempts. Please try again in {self._lock_timer} seconds")

    
            
    def login_successful(self, user):
        # Disable inputs immediately
        self.username_input.setEnabled(False)
        self.password_input.setEnabled(False)
        
        # Find the container and remove the existing buttons temporarily
        container = self.username_input.parent().parent()
        layout = container.layout()
        
        # Store references to the buttons we need to remove
        buttons = []
        for i in range(layout.count()):
            widget = layout.itemAt(i).widget()
            if isinstance(widget, AnimatedButton):
                buttons.append((i, widget))
        
        # Remove buttons from bottom to top to maintain correct indices
        for idx, button in reversed(buttons):
            layout.removeWidget(button)
            button.hide()
        
        # Create success message with animation
        success_message = SuccessMessage(user.username)
        layout.addWidget(success_message)
        
        # Create and setup home page
        self.home_page = MCQHomePage(self.appstate)
        
        # Create transition manager
        self.transition_manager = PageTransitionManager(self, self.home_page)
        
        # Start transition after showing success message
        QTimer.singleShot(1200, self.transition_manager.start_transition)
        

def main():
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_EnableHighDpiScaling)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps)
    
    window = MCQApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()