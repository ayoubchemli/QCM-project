import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve, QSize, QTimer
from PyQt5.QtGui import QFont, QColor, QPainter, QPainterPath, QLinearGradient, QIcon, QKeySequence

# TODO : ayoubchemli (💾 Export Results + password field light theme)

class MCQHistoryPage(QMainWindow):
    def __init__(self, parent=None, is_light_mode=False):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()
        self.apply_theme(is_light_mode)

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(30)
        main_layout.setContentsMargins(50, 40, 50, 40)

        # Create main content card
        content_card = QFrame()
        content_card.setObjectName("contentCard")
        content_layout = QVBoxLayout(content_card)
        content_layout.setSpacing(30)
        content_layout.setContentsMargins(40, 40, 40, 40)

        # Header with back button and title
        header_layout = QHBoxLayout()
        
        # Back button
        back_button = HoverButton("← Return to Home")
        back_button.setFixedWidth(200)
        back_button.clicked.connect(self.return_to_home)
        header_layout.addWidget(back_button)
        
        # Title
        title = AnimatedLabel("MCQ History")
        title.setObjectName("historyTitle")
        header_layout.addWidget(title, alignment=Qt.AlignCenter)
        header_layout.addSpacing(200)  # Balance the layout
        
        content_layout.addLayout(header_layout)

        # Statistics Overview Cards
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(20)

        # Create stat cards
        stat_cards = [
            ("Total Tests Taken", "42", "📝"),
            ("Average Score", "78%", "📊"),
            ("Best Performance", "95%", "🏆"),
            ("Tests This Month", "8", "📅")
        ]

        for title, value, icon in stat_cards:
            card = self.create_stat_card(title, value, icon)
            stats_layout.addWidget(card)

        content_layout.addLayout(stats_layout)

        # Recent Tests Section
        recent_tests_container = QFrame()
        recent_tests_container.setObjectName("recentTestsContainer")
        recent_tests_layout = QVBoxLayout(recent_tests_container)

        # Section title
        section_title = QLabel("Recent Tests")
        section_title.setObjectName("sectionTitle")
        recent_tests_layout.addWidget(section_title)

        # Test history table
        self.history_table = QTableWidget()
        self.history_table.setObjectName("historyTable")
        self.history_table.setColumnCount(5)
        self.history_table.setHorizontalHeaderLabels([
            "Date", "Subject", "Score", "Time Taken", "Status"
        ])
        
        # Add sample data
        self.add_sample_data()
        
        # Style the table
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.history_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.history_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        recent_tests_layout.addWidget(self.history_table)
        content_layout.addWidget(recent_tests_container)

        # Add the content card to main layout
        main_layout.addWidget(content_card)

    def create_stat_card(self, title, value, icon):
        card = QFrame()
        card.setObjectName("statCard")
        layout = QVBoxLayout(card)
        layout.setSpacing(10)

        # Icon
        icon_label = QLabel(icon)
        icon_label.setObjectName("statIcon")
        icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_label)

        # Value
        value_label = QLabel(value)
        value_label.setObjectName("statValue")
        value_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(value_label)

        # Title
        title_label = QLabel(title)
        title_label.setObjectName("statTitle")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        return card

    def add_sample_data(self):
        # Sample test data
        test_data = [
            ("2024-12-27", "Algebra", "85%", "45 mins", "Passed"),
            ("2024-12-25", "Data Structures", "92%", "60 mins", "Passed"),
            ("2024-12-23", "File Systems", "78%", "30 mins", "Passed"),
            ("2024-12-20", "Linear Algebra", "65%", "45 mins", "Failed"),
            ("2024-12-18", "Algorithms", "88%", "50 mins", "Passed"),
            ("2024-12-15", "Graph Theory", "73%", "40 mins", "Passed"),
            ("2024-12-12", "Number Theory", "95%", "55 mins", "Passed"),
            ("2024-12-10", "Binary Trees", "82%", "35 mins", "Passed")
        ]

        self.history_table.setRowCount(len(test_data))
        for row, (date, subject, score, time, status) in enumerate(test_data):
            self.history_table.setItem(row, 0, QTableWidgetItem(date))
            self.history_table.setItem(row, 1, QTableWidgetItem(subject))
            self.history_table.setItem(row, 2, QTableWidgetItem(score))
            self.history_table.setItem(row, 3, QTableWidgetItem(time))
            
            status_item = QTableWidgetItem(status)
            status_item.setTextAlignment(Qt.AlignCenter)
            if status == "Passed":
                status_item.setForeground(QColor("#10B981"))  # Green
            else:
                status_item.setForeground(QColor("#EF4444"))  # Red
            self.history_table.setItem(row, 4, status_item)

    def apply_theme(self, is_light_mode):
        if is_light_mode:
            self.setStyleSheet("""
                QMainWindow {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                        stop:0 #F8FAFC, stop:1 #F1F5F9);
                }
                #contentCard {
                    background-color: white;
                    border-radius: 20px;
                    border: 1px solid #E2E8F0;
                }
                #historyTitle {
                    color: #1E293B;
                    font-size: 36px;
                    font-weight: bold;
                }
                #statCard {
                    background-color: #F8FAFC;
                    border: 1px solid #E2E8F0;
                    border-radius: 15px;
                    padding: 20px;
                    min-width: 200px;
                }
                #statIcon {
                    font-size: 32px;
                }
                #statValue {
                    color: #1E293B;
                    font-size: 28px;
                    font-weight: bold;
                }
                #statTitle {
                    color: #64748B;
                    font-size: 14px;
                }
                #recentTestsContainer {
                    background-color: #F8FAFC;
                    border-radius: 15px;
                    border: 1px solid #E2E8F0;
                    padding: 20px;
                }
                #sectionTitle {
                    color: #1E293B;
                    font-size: 24px;
                    font-weight: bold;
                    margin-bottom: 20px;
                }
                QTableWidget {
                    background-color: white;
                    border: none;
                    border-radius: 10px;
                    gridline-color: #E2E8F0;
                }
                QTableWidget::item {
                    padding: 12px;
                    color: #1E293B;
                }
                QHeaderView::section {
                    background-color: #F1F5F9;
                    color: #64748B;
                    padding: 12px;
                    border: none;
                    font-weight: bold;
                }
                QTableWidget::item:selected {
                    background-color: #EDE9FE;
                    color: #1E293B;
                }
            """)
        else:
            self.setStyleSheet("""
                QMainWindow {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                        stop:0 #0F172A, stop:1 #1E293B);
                }
                #contentCard {
                    background-color: #1E293B;
                    border-radius: 20px;
                    border: 1px solid #2D3748;
                }
                #historyTitle {
                    color: white;
                    font-size: 36px;
                    font-weight: bold;
                }
                #statCard {
                    background-color: #0F172A;
                    border: 1px solid #2D3748;
                    border-radius: 15px;
                    padding: 20px;
                    min-width: 200px;
                }
                #statIcon {
                    font-size: 32px;
                }
                #statValue {
                    color: white;
                    font-size: 28px;
                    font-weight: bold;
                }
                #statTitle {
                    color: #94A3B8;
                    font-size: 14px;
                }
                #recentTestsContainer {
                    background-color: #0F172A;
                    border-radius: 15px;
                    border: 1px solid #2D3748;
                    padding: 20px;
                }
                #sectionTitle {
                    color: white;
                    font-size: 24px;
                    font-weight: bold;
                    margin-bottom: 20px;
                }
                QTableWidget {
                    background-color: #1E293B;
                    border: none;
                    border-radius: 10px;
                    gridline-color: #2D3748;
                }
                QTableWidget::item {
                    padding: 12px;
                    color: #E2E8F0;
                }
                QHeaderView::section {
                    background-color: #0F172A;
                    color: #94A3B8;
                    padding: 12px;
                    border: none;
                    font-weight: bold;
                }
                QTableWidget::item:selected {
                    background-color: #312E81;
                    color: white;
                }
            """)

    def return_to_home(self):
        self.close()
        if self.parent:
            self.parent.show()
            
            
class PasswordField(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.setup_connections()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(15)
        
        # Password input container
        self.input_container = QFrame()
        input_layout = QHBoxLayout(self.input_container)
        input_layout.setContentsMargins(0, 0, 0, 0)
        
        # Password input field
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your new password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setObjectName("passwordInput")
        self.password_input.setMinimumHeight(45)
        
        # Toggle password visibility button
        self.toggle_btn = QPushButton()
        self.toggle_btn.setText("👁")
        self.toggle_btn.setCheckable(True)
        self.toggle_btn.setObjectName("togglePassword")
        self.toggle_btn.setMinimumSize(45, 45)
        
        input_layout.addWidget(self.password_input)
        input_layout.addWidget(self.toggle_btn)
        
        # Password strength indicator
        self.strength_container = QFrame()
        strength_layout = QHBoxLayout(self.strength_container)
        strength_layout.setContentsMargins(0, 0, 0, 0)
        
        self.strength_bar = QProgressBar()
        self.strength_bar.setTextVisible(False)
        self.strength_bar.setFixedHeight(8)
        self.strength_bar.setRange(0, 100)
        self.strength_bar.setObjectName("strengthBar")
        
        self.strength_label = QLabel("Password Strength")
        self.strength_label.setObjectName("strengthLabel")
        
        strength_layout.addWidget(self.strength_bar)
        strength_layout.addWidget(self.strength_label)
        
        # Requirements list
        self.requirements_list = QFrame()
        req_layout = QVBoxLayout(self.requirements_list)
        req_layout.setContentsMargins(0, 10, 0, 0)
        req_layout.setSpacing(10)
        
        self.requirements = {
            'length': QLabel("• At least 8 characters"),
            'uppercase': QLabel("• At least one uppercase letter"),
            'lowercase': QLabel("• At least one lowercase letter"),
            'number': QLabel("• At least one number"),
            'special': QLabel("• At least one special character")
        }
        
        for req in self.requirements.values():
            req.setObjectName("requirement")
            req_layout.addWidget(req)
        
        # Add everything to main layout
        self.layout.addWidget(self.input_container)
        self.layout.addWidget(self.strength_container)
        self.layout.addWidget(self.requirements_list)
        
        self.apply_styles()

    def setup_connections(self):
        self.toggle_btn.clicked.connect(self.toggle_password_visibility)
        self.password_input.textChanged.connect(self.check_password_strength)

    def toggle_password_visibility(self):
        if self.toggle_btn.isChecked():
            self.password_input.setEchoMode(QLineEdit.Normal)
            self.toggle_btn.setText("👁‍🗨")
        else:
            self.password_input.setEchoMode(QLineEdit.Password)
            self.toggle_btn.setText("👁")

    def check_password_strength(self):
        password = self.password_input.text()
        score = 0
        
        # Check requirements
        has_length = len(password) >= 8
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_number = any(c.isdigit() for c in password)
        has_special = any(not c.isalnum() for c in password)
        
        # Update requirement labels
        self.requirements['length'].setProperty("met", has_length)
        self.requirements['uppercase'].setProperty("met", has_upper)
        self.requirements['lowercase'].setProperty("met", has_lower)
        self.requirements['number'].setProperty("met", has_number)
        self.requirements['special'].setProperty("met", has_special)
        
        # Calculate score
        if has_length: score += 20
        if has_upper: score += 20
        if has_lower: score += 20
        if has_number: score += 20
        if has_special: score += 20
        
        # Update requirement styles
        for req in self.requirements.values():
            if req.property("met"):
                req.setStyleSheet("color: #10B981; font-size: 14px;")  # Green
            else:
                req.setStyleSheet("color: #6B7280; font-size: 14px;")  # Gray
        
        # Update strength indicator
        self.strength_bar.setValue(score)
        
        # Update strength label
        if score < 40:
            strength_text = "Weak"
            strength_color = "#EF4444"  # Red
        elif score < 80:
            strength_text = "Medium"
            strength_color = "#F59E0B"  # Yellow
        else:
            strength_text = "Strong"
            strength_color = "#10B981"  # Green
            
        self.strength_label.setText(strength_text)
        self.strength_label.setStyleSheet(f"color: {strength_color}; font-size: 14px; font-weight: bold;")
        self.strength_bar.setStyleSheet(f"""
            QProgressBar {{
                border-radius: 4px;
                background-color: #E2E8F0;
            }}
            QProgressBar::chunk {{
                border-radius: 4px;
                background-color: {strength_color};
            }}
        """)

    def get_password(self):
        return self.password_input.text()

    def set_password(self, password):
        self.password_input.setText(password)

    def apply_styles(self):
        self.setStyleSheet("""
            QFrame {
                background: transparent;
            }
            
            #passwordInput {
                padding: 12px 15px;
                border: 2px solid #2D3748;
                border-radius: 10px;
                font-size: 16px;
                background-color: #1E293B;
                min-width: 300px;
                color: white;
            }
            
            #passwordInput:focus {
                border-color: #4F46E5;
            }
            
            #togglePassword {
                background-color: #1E293B;
                border: 2px solid #2D3748;
                border-radius: 10px;
                padding: 5px;
                font-size: 20px;
                margin-left: 10px;
                color: white;
            }
            
            #togglePassword:hover {
                background-color: #2D3748;
                border-color: #4F46E5;
            }
            
            #strengthBar {
                border-radius: 4px;
                background-color: #0F172A;
                min-width: 200px;
                border: 1px solid #2D3748;
                height: 8px;
            }
            
            #strengthLabel {
                font-size: 14px;
                font-weight: bold;
                margin-left: 15px;
                min-width: 100px;
                color: #E2E8F0;
            }
            
            #requirement {
                font-size: 14px;
                padding: 3px 0;
                color: #94A3B8;
            }
            
            #requirement[met="true"] {
                color: #4F46E5;
            }
        """)

class ProfilePage(QMainWindow):
    def __init__(self, parent=None, is_light_mode=False):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()
        self.apply_theme(is_light_mode)

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(30)
        main_layout.setContentsMargins(50, 40, 50, 40)

        # Create a card-like container for the entire content
        content_card = QFrame()
        content_card.setObjectName("contentCard")
        content_layout = QVBoxLayout(content_card)
        content_layout.setSpacing(5)
        content_layout.setContentsMargins(40, 10, 40, 10)

        # Header with back button
        header_layout = QHBoxLayout()
        back_button = HoverButton("← Return to Home")
        back_button.setFixedWidth(200)
        back_button.clicked.connect(self.return_to_home)
        header_layout.addWidget(back_button)
        header_layout.addStretch()
        content_layout.addLayout(header_layout)

        # Profile Section
        profile_section = QHBoxLayout()
      
        # Right side - Profile Info
        profile_info = QVBoxLayout()
        
        # Title with animation
        title = AnimatedLabel("Profile Settings")
        title.setObjectName("profileTitle")
        profile_info.addWidget(title)

        # Subtitle
        subtitle = QLabel("Manage your personal information and account settings")
        subtitle.setObjectName("profileSubtitle")
        profile_info.addWidget(subtitle)
        
        # Add profile sections to layout
        profile_section.addSpacing(40)
        profile_section.addLayout(profile_info, stretch=1)
        content_layout.addLayout(profile_section)

        # Create a form container with a nice background
        form_container = QFrame()
        form_container.setObjectName("formContainer")
        form_layout = QVBoxLayout(form_container)
        form_layout.setSpacing(1)
        form_layout.setContentsMargins(30, 30, 30, 30)

        # Input fields with icons and labels
        self.fields = {}
        field_configs = {
            'full_name': ('👤 Full Name', 'Enter your full name'),
            'email': ('📧 Email Address', 'Enter your email'),
            'username': ('🔤 Username', 'Choose a username'),
        }

        for field_name, (label, placeholder) in field_configs.items():
            field_container = QFrame()
            field_container.setObjectName("fieldContainer")
            field_layout = QVBoxLayout(field_container)
            field_layout.setSpacing(8)

            # Label
            label_widget = QLabel(label)
            label_widget.setObjectName("fieldLabel")
            field_layout.addWidget(label_widget)

            # Input field
            input_field = QLineEdit()
            input_field.setPlaceholderText(placeholder)
            input_field.setObjectName("inputField")
            
            self.fields[field_name] = input_field
            field_layout.addWidget(input_field)

            # Add to form layout
            form_layout.addWidget(field_container)
            
        # Add the new password field after the regular fields
        password_container = QFrame()
        password_container.setObjectName("fieldContainer")  # Match other fields' style
        password_layout = QVBoxLayout(password_container)
        password_layout.setSpacing(8)
        password_layout.setContentsMargins(0, 0, 0, 0)

        password_label = QLabel("🔒 Password")
        password_label.setObjectName("fieldLabel")
        password_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                margin-bottom: 5px;
            }
        """)

        self.password_field = PasswordField()

        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_field)

        form_layout.addWidget(password_container)

        content_layout.addWidget(form_container)

        # Save button with animation
        save_button = HoverButton("Save Changes")
        save_button.setObjectName("saveButton")
        save_button.setFixedWidth(200)
        save_button.setFixedHeight(50)
        save_button.clicked.connect(self.save_changes)
        
        # Button container for center alignment
        button_container = QHBoxLayout()
        button_container.addStretch()
        button_container.addWidget(save_button)
        button_container.addStretch()
        content_layout.addLayout(button_container)

        # Add the content card to main layout
        main_layout.addWidget(content_card)

    def apply_theme(self, is_light_mode):
        if is_light_mode:
            self.setStyleSheet("""
                QMainWindow {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                        stop:0 #F8FAFC, stop:1 #F1F5F9);
                }
                #contentCard {
                    background-color: white;
                    border-radius: 20px;
                    border: 1px solid #E2E8F0;
                }
                #profileTitle {
                    color: #1E293B;
                    font-size: 36px;
                    font-weight: bold;
                    margin-bottom: 10px;
                }
                #profileSubtitle {
                    color: #64748B;
                    font-size: 16px;
                    margin-bottom: 20px;
                }
                #formContainer {
                    background-color: #F8FAFC;
                    border-radius: 15px;
                    border: 1px solid #E2E8F0;
                }
                #fieldContainer {
                    background: transparent;
                    margin-bottom: 10px;
                }
                #fieldLabel {
                    color: #4A5568;
                    font-size: 14px;
                    font-weight: bold;
                }
                #inputField {
                    background-color: white;
                    border: 2px solid #E2E8F0;
                    border-radius: 10px;
                    padding: 12px 15px;
                    font-size: 14px;
                    color: #1E293B;
                }
                #inputField:focus {
                    border-color: #4F46E5;
                }

            """)
        else:
            self.setStyleSheet("""
                QMainWindow {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                        stop:0 #0F172A, stop:1 #1E293B);
                }
                #contentCard {
                    background-color: #1E293B;
                    border-radius: 20px;
                    border: 1px solid #2D3748;
                }
                #profileTitle {
                    color: white;
                    font-size: 36px;
                    font-weight: bold;
                    margin-bottom: 10px;
                }
                #profileSubtitle {
                    color: #94A3B8;
                    font-size: 16px;
                    margin-bottom: 20px;
                }
                #formContainer {
                    background-color: #0F172A;
                    border-radius: 15px;
                    border: 1px solid #2D3748;
                }
                #fieldContainer {
                    background: transparent;
                    margin-bottom: 10px;
                }
                #fieldLabel {
                    color: #E2E8F0;
                    font-size: 14px;
                    font-weight: bold;
                }
                #inputField {
                    background-color: #1E293B;
                    border: 2px solid #2D3748;
                    border-radius: 10px;
                    padding: 12px 15px;
                    font-size: 14px;
                    color: white;
                }
                #inputField:focus {
                    border-color: #4F46E5;
                }
            """)

    def return_to_home(self):
        self.close()
        if self.parent:
            self.parent.show()

    def save_changes(self):
        # Add loading animation
        save_button = self.findChild(HoverButton, "saveButton")
        original_text = save_button.text()
        save_button.setText("Saving...")
        save_button.setEnabled(False)
        
        # Simulate saving delay
        QTimer.singleShot(1500, lambda: self.show_save_success(save_button, original_text))

    def show_save_success(self, button, original_text):
        # Create a custom success message box
        msg = QMessageBox(self)
        msg.setWindowTitle("Success")
        msg.setText("Profile changes saved successfully!")
        msg.setIcon(QMessageBox.Information)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #1E293B;
            }
            QMessageBox QLabel {
                color: white;
                font-size: 14px;
                padding: 10px;
            }
            QPushButton {
                background-color: #4F46E5;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4338CA;
            }
        """)
        
        # Reset button state
        button.setText(original_text)
        button.setEnabled(True)
        
        msg.exec_()
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
    
   def setup_menu_actions(self):
        # Connect menu actions to their respective functions
        for action in self.dropdown_button.menu.actions():
            if action.text() == "👤 Profile":
                action.triggered.connect(self.open_profile)
            elif action.text() == "📊 MCQ History":
                action.triggered.connect(self.open_mcq_history)

   def open_mcq_history(self):
        self.mcq_history_page = MCQHistoryPage(self, self.theme_toggle.isChecked())
        self.mcq_history_page.showFullScreen()

   def open_profile(self):
        self.profile_page = ProfilePage(self, self.theme_toggle.isChecked())
        self.profile_page.showFullScreen()
        
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
        
        self.setup_menu_actions()

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