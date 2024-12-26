from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMenu, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QIcon

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aesthetic Dropdown Menu")
        self.setGeometry(100, 100, 400, 300)

        main_widget = QWidget()
        layout = QVBoxLayout(main_widget)

        # Enhanced Dropdown Button
        dropdown_button = QPushButton("☰")
        dropdown_button.setFixedSize(70, 65)
        dropdown_button.setFont(QFont('Segoe UI', 16))
        dropdown_button.setStyleSheet("""
            QPushButton {
                background-color: #2A2A3D;
                color: #FFFFFF;
                font-weight: bold;
                border: 2px solid #3C3C4F;
                border-radius: 25px;
                padding: 5px;
                margin: 10px;
            }
            QPushButton:hover {
                background-color: #3E3E5E;
                border-color: #6C6C8F;
                color: #E0E0FF;
                transition: all 0.3s ease;
            }
            QPushButton:pressed {
                background-color: #4E4E6E;
                border-color: #7F7F9F;
                padding: 6px 4px 4px 6px;
            }
        """)

        # Enhanced Dropdown Menu
        dropdown_menu = QMenu()
        dropdown_menu.setFont(QFont('Segoe UI', 11))
        dropdown_menu.setStyleSheet("""
            QMenu {
                background-color: #2D2D45;
                border: 2px solid #4A4A5F;
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
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #3C3C5F, stop:1 #4A4A7F);
                color: #FFFFFF;
            }
            QMenu::separator {
                height: 2px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #40406F, stop:0.5 #50507F, stop:1 #40406F);
                margin: 6px 15px;
            }
        """)

        # Menu items with icons (you'll need to add actual icons)
        actions = {
            "📚 Docs": "Documentation",
            "🎓 Courses": "Online Courses",
            "📞 Contact": "Contact Us",
            "📝 Blog": "Our Blog",
            "👤 Sign in": "Account Access"
        }

        for icon_text, tooltip in actions.items():
            if icon_text == "👤 Sign in":
                dropdown_menu.addSeparator()
            action = dropdown_menu.addAction(icon_text)
            action.setToolTip(tooltip)

        dropdown_button.setMenu(dropdown_menu)
        layout.addWidget(dropdown_button, alignment=Qt.AlignTop | Qt.AlignRight)
        self.setCentralWidget(main_widget)

        # Enhanced window style
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1E1E2E, stop:1 #2A2A3D);
            }
        """)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()