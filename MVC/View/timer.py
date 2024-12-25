import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QPushButton, QLabel, QFrame, QGraphicsDropShadowEffect)
from PyQt5.QtCore import QTimer, Qt, QPropertyAnimation, QEasingCurve, QRect
from PyQt5.QtGui import QFont, QColor, QPainterPath, QPainter, QGradient, QLinearGradient

class LuxuryTimer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Luxury Timer")
        self.setGeometry(100, 100, 500, 600)
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1A1A2E,
                    stop:1 #16213E);
            }
            QLabel {
                color: #E2E2E2;
                background-color: rgba(255, 255, 255, 0.05);
                border: 2px solid rgba(255, 255, 255, 0.1);
                border-radius: 20px;
            }
            QPushButton {
                background-color: rgba(255, 255, 255, 0.1);
                color: #FFFFFF;
                border: 2px solid rgba(255, 255, 255, 0.1);
                border-radius: 25px;
                padding: 15px;
                font-size: 16px;
                min-width: 200px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.15);
                border: 2px solid rgba(255, 255, 255, 0.2);
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.05);
            }
        """)
        
        # Create central widget with glass morphism effect
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(30)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Create timer container
        self.timer_container = QFrame()
        self.timer_container.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.05);
                border: 2px solid rgba(255, 255, 255, 0.1);
                border-radius: 30px;
            }
        """)
        container_layout = QVBoxLayout(self.timer_container)
        container_layout.setContentsMargins(30, 30, 30, 30)
        
        # Add shadow effect to container
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 160))
        shadow.setOffset(0, 0)
        self.timer_container.setGraphicsEffect(shadow)
        
        # Create digital display
        self.time_left = 15 * 60
        self.timer_display = QLabel("15:00")
        self.timer_display.setAlignment(Qt.AlignCenter)
        display_font = QFont('Arial', 85, QFont.Bold)
        self.timer_display.setFont(display_font)
        
        # Add shadow to text
        text_shadow = QGraphicsDropShadowEffect()
        text_shadow.setBlurRadius(15)
        text_shadow.setColor(QColor(0, 0, 0, 180))
        text_shadow.setOffset(0, 0)
        self.timer_display.setGraphicsEffect(text_shadow)
        
        container_layout.addWidget(self.timer_display)
        layout.addWidget(self.timer_container)
        
        # Create animated progress bar
        self.progress_bar = QFrame()
        self.progress_bar.setFixedHeight(6)
        self.progress_bar.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 3px;
            }
        """)
        layout.addWidget(self.progress_bar)
        
        # Create progress indicator
        self.progress_indicator = QFrame(self.progress_bar)
        self.progress_indicator.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4FA6B2,
                    stop:1 #6BB5F9);
                border-radius: 3px;
            }
        """)
        self.progress_indicator.setFixedHeight(6)
        
        # Create control buttons with modern styling
        button_container = QWidget()
        button_layout = QVBoxLayout(button_container)
        button_layout.setSpacing(20)
        
        self.start_button = QPushButton("START")
        self.start_button.setCursor(Qt.PointingHandCursor)
        self.start_button.clicked.connect(self.start_timer)
        button_layout.addWidget(self.start_button)
        
        self.reset_button = QPushButton("RESET")
        self.reset_button.setCursor(Qt.PointingHandCursor)
        self.reset_button.clicked.connect(self.reset_timer)
        button_layout.addWidget(self.reset_button)
        
        layout.addWidget(button_container)
        
        # Timer setup
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.timer.setInterval(1000)
        
        self.is_running = False
        self.initial_time = 15 * 60
        
        # Animation setup
        self.progress_animation = QPropertyAnimation(self.progress_indicator, b"geometry")
        self.progress_animation.setDuration(1000)
        self.progress_animation.setEasingCurve(QEasingCurve.OutCubic)
        
    def start_timer(self):
        if not self.is_running:
            self.timer.start()
            self.is_running = True
            self.start_button.setText("PAUSE")
            self.start_button.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #4FA6B2,
                        stop:1 #6BB5F9);
                    color: #FFFFFF;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #5FB6C2,
                        stop:1 #7BC5FF);
                }
            """)
        else:
            self.timer.stop()
            self.is_running = False
            self.start_button.setText("RESUME")
            self.start_button.setStyleSheet("")
    
    def reset_timer(self):
        self.timer.stop()
        self.is_running = False
        self.time_left = 15 * 60
        self.timer_display.setText("15:00")
        self.start_button.setText("START")
        self.start_button.setStyleSheet("")
        self.animate_progress(100)
        
    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            minutes = self.time_left // 60
            seconds = self.time_left % 60
            self.timer_display.setText(f"{minutes:02d}:{seconds:02d}")
            
            # Update progress bar
            progress = (self.time_left / self.initial_time) * 100
            self.animate_progress(progress)
        else:
            self.timer.stop()
            self.is_running = False
            self.start_button.setText("START")
            self.start_button.setStyleSheet("")
            
    def animate_progress(self, progress):
        width = self.progress_bar.width() * (progress / 100)
        self.progress_animation.setStartValue(self.progress_indicator.geometry())
        self.progress_animation.setEndValue(QRect(0, 0, int(width), 6))
        self.progress_animation.start()
        
    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Update progress bar on resize
        if hasattr(self, 'time_left'):
            progress = (self.time_left / self.initial_time) * 100
            width = self.progress_bar.width() * (progress / 100)
            self.progress_indicator.setGeometry(0, 0, int(width), 6)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set application-wide font
    app.setFont(QFont('Arial', 10))
    
    timer = LuxuryTimer()
    timer.show()
    sys.exit(app.exec_())