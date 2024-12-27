import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class AnimatedButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self._animation = QPropertyAnimation(self, b"geometry")
        self._animation.setDuration(100)
        self._animation.setEasingCurve(QEasingCurve.OutCubic)

    def enterEvent(self, event):
        rect = self.geometry()
        self._animation.setStartValue(rect)
        self._animation.setEndValue(QRect(rect.x()-5, rect.y()-5, 
                                        rect.width()+10, rect.height()+10))
        self._animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        rect = self.geometry()
        self._animation.setStartValue(rect)
        self._animation.setEndValue(QRect(rect.x()+5, rect.y()+5, 
                                        rect.width()-10, rect.height()-10))
        self._animation.start()
        super().leaveEvent(event)

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

class MCQApp(QMainWindow):
    
    def create_registration_page(self):
        registration_page = QWidget()
        layout = QVBoxLayout(registration_page)
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
                backdrop-filter: blur(10px);
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
        container_layout.setSpacing(25)
        container_layout.setContentsMargins(40, 40, 40, 40)
        
        # Title section
        title_label = QLabel("Create Account")
        title_label.setFont(QFont('Poppins', 36, QFont.Bold))
        title_label.setStyleSheet("color: white;")
        title_label.setAlignment(Qt.AlignCenter)
        
        subtitle_label = QLabel("Join Our Learning Community")
        subtitle_label.setFont(QFont('Poppins', 16))
        subtitle_label.setStyleSheet("color: rgba(255, 255, 255, 0.8);")
        subtitle_label.setAlignment(Qt.AlignCenter)
        
        # Input fields
        # Full Name
        fullname_container = QFrame()
        fullname_layout = QHBoxLayout(fullname_container)
        fullname_layout.setContentsMargins(0, 0, 0, 0)
        
        fullname_icon = QLabel()
        fullname_icon.setPixmap(QIcon(":/icons/user.png").pixmap(24, 24))
        
        self.fullname_input = FancyLineEdit()
        self.fullname_input.setPlaceholderText("Enter your full name")
        self.fullname_input.setStyleSheet("""
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
        
        fullname_layout.addWidget(fullname_icon)
        fullname_layout.addWidget(self.fullname_input)
        
        # Email
        email_container = QFrame()
        email_layout = QHBoxLayout(email_container)
        email_layout.setContentsMargins(0, 0, 0, 0)
        
        email_icon = QLabel()
        email_icon.setPixmap(QIcon(":/icons/email.png").pixmap(24, 24))
        
        self.email_input = FancyLineEdit()
        self.email_input.setPlaceholderText("Enter your email")
        self.email_input.setStyleSheet(self.fullname_input.styleSheet())
        
        email_layout.addWidget(email_icon)
        email_layout.addWidget(self.email_input)
        
        # Username
        username_container = QFrame()
        username_layout = QHBoxLayout(username_container)
        username_layout.setContentsMargins(0, 0, 0, 0)
        
        username_icon = QLabel()
        username_icon.setPixmap(QIcon(":/icons/user.png").pixmap(24, 24))
        
        self.reg_username_input = FancyLineEdit()
        self.reg_username_input.setPlaceholderText("Choose a username (must be unique)")
        self.reg_username_input.setStyleSheet(self.fullname_input.styleSheet())
        
        username_layout.addWidget(username_icon)
        username_layout.addWidget(self.reg_username_input)
        
        # Password
        password_container = QFrame()
        password_layout = QHBoxLayout(password_container)
        password_layout.setContentsMargins(0, 0, 0, 0)
        
        password_icon = QLabel()
        password_icon.setPixmap(QIcon(":/icons/lock.png").pixmap(24, 24))
        
        self.reg_password_input = FancyLineEdit()
        self.reg_password_input.setPlaceholderText("Create a password")
        self.reg_password_input.setEchoMode(QLineEdit.Password)
        self.reg_password_input.setStyleSheet(self.fullname_input.styleSheet())
        
        password_layout.addWidget(password_icon)
        password_layout.addWidget(self.reg_password_input)
        
        # Confirm Password
        confirm_password_container = QFrame()
        confirm_password_layout = QHBoxLayout(confirm_password_container)
        confirm_password_layout.setContentsMargins(0, 0, 0, 0)
        
        confirm_password_icon = QLabel()
        confirm_password_icon.setPixmap(QIcon(":/icons/lock.png").pixmap(24, 24))
        
        self.confirm_password_input = FancyLineEdit()
        self.confirm_password_input.setPlaceholderText("Confirm your password")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setStyleSheet(self.fullname_input.styleSheet())
        
        confirm_password_layout.addWidget(confirm_password_icon)
        confirm_password_layout.addWidget(self.confirm_password_input)
        
        # Register Button
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
                min-width: 250px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #FF6B6B, stop:1 #FF3C85);
            }
        """)
        register_button.clicked.connect(self.handle_registration)
        
        # Back to Login Button
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
        
        # Add all elements to container
        container_layout.addWidget(title_label)
        container_layout.addWidget(subtitle_label)
        container_layout.addWidget(fullname_container)
        container_layout.addWidget(email_container)
        container_layout.addWidget(username_container)
        container_layout.addWidget(password_container)
        container_layout.addWidget(confirm_password_container)
        container_layout.addWidget(register_button, alignment=Qt.AlignCenter)
        container_layout.addWidget(back_button, alignment=Qt.AlignCenter)
        
        # Add container to main layout
        layout.addWidget(container)
        
        # Footer
        footer_label = QLabel("© 2024 USTHB Computer Science. Made with ♥")
        footer_label.setFont(QFont('Poppins', 10))
        footer_label.setStyleSheet("color: rgba(255, 255, 255, 0.7);")
        footer_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(footer_label)
        
        self.stacked_widget.addWidget(registration_page)

    def handle_registration(self):
        fullname = self.fullname_input.text()
        email = self.email_input.text()
        username = self.reg_username_input.text()
        password = self.reg_password_input.text()
        confirm_password = self.confirm_password_input.text()
        
        if all([fullname.strip(), email.strip(), username.strip(), 
                password.strip(), confirm_password.strip()]):
            if password == confirm_password:
                print(f"Registering new user: {username}")
                # Add your registration logic here
                self.stacked_widget.setCurrentIndex(0)  # Return to login page
            else:
                # Add error handling for password mismatch
                pass
            
        
    def __init__(self):
        super().__init__()
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
                backdrop-filter: blur(10px);
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
        username = self.username_input.text()
        password = self.password_input.text()
        if username.strip() and password.strip():
            print(f"User {username} attempting to log in")
            # Add your login logic here

def main():
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_EnableHighDpiScaling)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps)
    
    window = MCQApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()