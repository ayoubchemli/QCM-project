import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                            QStackedWidget, QFrame, QGraphicsDropShadowEffect)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect
from PyQt5.QtGui import QFont, QIcon, QColor, QPalette, QFontDatabase
import qdarkstyle

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
        
        guest_button = AnimatedButton("Continue as Guest")
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
        
        # Add all elements to container
        container_layout.addWidget(logo_label)
        container_layout.addWidget(title_label)
        container_layout.addWidget(subtitle_label)
        container_layout.addWidget(username_container)
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
        if username.strip():
            print(f"User {username} logged in")
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