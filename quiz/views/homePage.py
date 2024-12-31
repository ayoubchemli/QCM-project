import sys
import re
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import json

import bcrypt


class ContactPage(QMainWindow):
    def __init__(self, user, parent=None, is_light_mode=False):
        super().__init__(parent)
        self.user = user  # Store user information
        self.parent = parent
        self.setup_ui()
        self.apply_theme(is_light_mode)
        print(f"Welcome {self.user['username']}!")

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)  # Reduced from 30
        main_layout.setContentsMargins(30, 20, 30, 20)  # Reduced margins

        # Create main content card
        content_card = QFrame()
        content_card.setObjectName("contentCard")
        content_layout = QVBoxLayout(content_card)
        content_layout.setSpacing(20)  # Reduced from 30
        content_layout.setContentsMargins(20, 20, 20, 20)  # Reduced margins

        # Header with back button and title
        header_layout = QHBoxLayout()
        header_layout.setSpacing(10)  # Added spacing control
        
        back_button = HoverButton("← Return to Home")
        back_button.setFixedWidth(200)  
        back_button.clicked.connect(self.return_to_home)
        
        title = AnimatedLabel("Contact Us")
        title.setObjectName("contactTitle")
        
        header_layout.addWidget(back_button)
        header_layout.addWidget(title, alignment=Qt.AlignCenter)
        header_layout.addStretch()  # Better than fixed spacing
        
        content_layout.addLayout(header_layout)

        # Contact Methods Section
        methods_container = QFrame()
        methods_container.setObjectName("methodsContainer")
        methods_layout = QHBoxLayout(methods_container)
        methods_layout.setSpacing(15)  # Reduced from 20
        methods_layout.setContentsMargins(10, 10, 10, 10)  # Added margins

        contact_methods = [
            ("📧", "Email Us", "support@example.com", "Send us an email anytime"),
            ("📱", "Call Us", "+1 (555) 123-4567", "Mon-Fri, 9:00-17:00"),
            ("💬", "Live Chat", "Available 24/7", "Chat with our support team")
        ]

        for icon, title, detail, description in contact_methods:
            card = self.create_contact_card(icon, title, detail, description)
            methods_layout.addWidget(card)

        content_layout.addWidget(methods_container)

        # Form and FAQ side by side
        bottom_container = QHBoxLayout()
        bottom_container.setSpacing(15)

        # Left side - Contact Form
        form_container = QFrame()
        form_container.setObjectName("formContainer")
        form_layout = QVBoxLayout(form_container)
        form_layout.setSpacing(15)  # Reduced from 20
        form_layout.setContentsMargins(15, 15, 15, 15)

        form_title = QLabel("Send us a Message")
        form_title.setObjectName("sectionTitle")
        form_layout.addWidget(form_title)

        # Form fields
        form_grid = QGridLayout()
        form_grid.setSpacing(10)  # Reduced from 15

        # Name fields in one row
        first_name = QLineEdit()
        first_name.setPlaceholderText("First Name")
        first_name.setObjectName("formInput")
        
        last_name = QLineEdit()
        last_name.setPlaceholderText("Last Name")
        last_name.setObjectName("formInput")
        
        form_grid.addWidget(first_name, 0, 0)
        form_grid.addWidget(last_name, 0, 1)

        # Other fields
        email = QLineEdit()
        email.setPlaceholderText("Email Address")
        email.setObjectName("formInput")
        form_grid.addWidget(email, 1, 0, 1, 2)

        subject = QLineEdit()
        subject.setPlaceholderText("Subject")
        subject.setObjectName("formInput")
        form_grid.addWidget(subject, 2, 0, 1, 2)

        message = QTextEdit()
        message.setPlaceholderText("Your Message")
        message.setObjectName("messageInput")
        message.setMinimumHeight(100)  # Reduced from 150
        form_grid.addWidget(message, 3, 0, 1, 2)

        form_layout.addLayout(form_grid)

        submit_btn = HoverButton("Send Message")
        submit_btn.setObjectName("submitButton")
        submit_btn.setFixedWidth(150)  # Reduced from 200
        submit_btn.clicked.connect(self.submit_form)
        form_layout.addWidget(submit_btn, alignment=Qt.AlignCenter)

        # Right side - FAQ
        faq_container = QFrame()
        faq_container.setObjectName("faqContainer")
        faq_layout = QVBoxLayout(faq_container)
        faq_layout.setSpacing(10)
        faq_layout.setContentsMargins(15, 15, 15, 15)

        faq_title = QLabel("Frequently Asked Questions")
        faq_title.setObjectName("sectionTitle")
        faq_layout.addWidget(faq_title)

        faqs = [
            ("How do I reset my password?", 
            "Click on the 'Forgot Password' link on the login page and follow the instructions sent to your email."),
            ("Can I change my username?", 
            "Yes, you can change your username in your profile settings."),
            ("How are the MCQ scores calculated?", 
            "Scores are calculated based on the number of correct answers. Each question carries equal marks."),
            ("What happens if I lose connection during a test?", 
            "Don't worry! Your progress is automatically saved. You can resume from where you left off.")
        ]

        for question, answer in faqs:
            faq_item = self.create_faq_item(question, answer)
            faq_layout.addWidget(faq_item)

        # Add form and FAQ to bottom container
        bottom_container.addWidget(form_container, 1)  # 1 is stretch factor
        bottom_container.addWidget(faq_container, 1)   # 1 is stretch factor

        content_layout.addLayout(bottom_container)
        main_layout.addWidget(content_card)

    def create_contact_card(self, icon, title, detail, description):
        card = QFrame()
        card.setObjectName("contactCard")
        layout = QVBoxLayout(card)
        layout.setSpacing(8)
        layout.setContentsMargins(15, 15, 15, 15)


        icon_label = QLabel(icon)
        icon_label.setObjectName("contactIcon")
        icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_label)

        title_label = QLabel(title)
        title_label.setObjectName("contactTitle")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        detail_label = QLabel(detail)
        detail_label.setObjectName("contactDetail")
        detail_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(detail_label)

        desc_label = QLabel(description)
        desc_label.setObjectName("contactDescription")
        desc_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(desc_label)

        return card

    def create_faq_item(self, question, answer):
        item = QFrame()
        item.setObjectName("faqItem")
        layout = QVBoxLayout(item)

        question_label = QLabel(question)
        question_label.setObjectName("faqQuestion")
        layout.addWidget(question_label)

        answer_label = QLabel(answer)
        answer_label.setObjectName("faqAnswer")
        answer_label.setWordWrap(True)
        layout.addWidget(answer_label)

        return item

    def submit_form(self):
        submit_btn = self.findChild(HoverButton, "submitButton")
        original_text = submit_btn.text()
        submit_btn.setText("Sending...")
        submit_btn.setEnabled(False)

        # Simulate sending message
        QTimer.singleShot(2000, lambda: self.show_submit_success(submit_btn, original_text))

    def show_submit_success(self, button, original_text):
        msg = QMessageBox(self)
        msg.setWindowTitle("Success")
        msg.setText("Message sent successfully!")
        msg.setInformativeText("We'll get back to you soon.")
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
        
        button.setText(original_text)
        button.setEnabled(True)
        
        msg.exec_()

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
                #contactCard {
                    background-color: #F8FAFC;
                    border: 1px solid #E2E8F0;
                    border-radius: 15px;
                    padding: 25px;
                }
                #contactIcon {
                    font-size: 36px;
                    margin-bottom: 10px;
                }
                #contactTitle {
                    color: #1E293B;
                    font-size: 20px;
                    font-weight: bold;
                }
                #contactDetail {
                    color: #4F46E5;
                    font-size: 16px;
                }
                #contactDescription {
                    color: #64748B;
                    font-size: 14px;
                }
                #formContainer, #faqContainer {
                    background-color: #F8FAFC;
                    border: 1px solid #E2E8F0;
                    border-radius: 15px;
                    padding: 25px;
                }
                #sectionTitle {
                    color: #1E293B;
                    font-size: 24px;
                    font-weight: bold;
                    margin-bottom: 20px;
                }
                #formInput, #messageInput {
                    background-color: white;
                    border: 2px solid #E2E8F0;
                    border-radius: 8px;
                    padding: 12px;
                    color: #1E293B;
                }
                #formInput:focus, #messageInput:focus {
                    border-color: #4F46E5;
                }
                #faqItem {
                    background-color: white;
                    border: 1px solid #E2E8F0;
                    border-radius: 10px;
                    padding: 15px;
                    margin-bottom: 10px;
                }
                #faqQuestion {
                    color: #1E293B;
                    font-size: 16px;
                    font-weight: bold;
                }
                #faqAnswer {
                    color: #64748B;
                    font-size: 14px;
                    margin-top: 8px;
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
                #contactCard {
                    background-color: #0F172A;
                    border: 1px solid #2D3748;
                    border-radius: 15px;
                    padding: 25px;
                }
                #contactIcon {
                    font-size: 36px;
                    margin-bottom: 10px;
                }
                #contactTitle {
                    color: white;
                    font-size: 20px;
                    font-weight: bold;
                }
                #contactDetail {
                    color: #818CF8;
                    font-size: 16px;
                }
                #contactDescription {
                    color: #94A3B8;
                    font-size: 14px;
                }
                #formContainer, #faqContainer {
                    background-color: #0F172A;
                    border: 1px solid #2D3748;
                    border-radius: 15px;
                    padding: 25px;
                }
                #sectionTitle {
                    color: white;
                    font-size: 24px;
                    font-weight: bold;
                    margin-bottom: 20px;
                }
                #formInput, #messageInput {
                    background-color: #1E293B;
                    border: 2px solid #2D3748;
                    border-radius: 8px;
                    padding: 12px;
                    color: white;
                }
                #formInput:focus, #messageInput:focus {
                    border-color: #4F46E5;
                }
                #faqItem {
                    background-color: #1E293B;
                    border: 1px solid #2D3748;
                    border-radius: 10px;
                    padding: 15px;
                    margin-bottom: 10px;
                }
                #faqQuestion {
                    color: white;
                    font-size: 16px;
                    font-weight: bold;
                }
                #faqAnswer {
                    color: #94A3B8;
                    font-size: 14px;
                    margin-top: 8px;
                }
            """)

    def return_to_home(self):
        self.close()
        if self.parent:
            self.parent.show()

class ExportResultsPage(QMainWindow):
    def __init__(self, user, parent=None, is_light_mode=False):
        super().__init__(parent)
        self.user = user  # Store user information
        self.parent = parent
        self.selected_date_range = "all"  # Default to all time
        self.selected_format = "csv"  # Default to CSV
        self.setup_ui()
        self.apply_theme(is_light_mode)
        print(f"Welcome {self.user['username']}!")

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)  # Reduced from 30
        main_layout.setContentsMargins(30, 20, 30, 20)  # Reduced margins

        # Create main content card
        content_card = QFrame()
        content_card.setObjectName("contentCard")
        content_layout = QVBoxLayout(content_card)
        content_layout.setSpacing(20)  # Reduced from 30
        content_layout.setContentsMargins(30, 20, 30, 20)  # Reduced margins

        # Header with back button and title in one row
        header_layout = QHBoxLayout()
        header_layout.setSpacing(15)
        
        back_button = HoverButton("← Return to Home")
        back_button.setFixedWidth(200)  # Reduced width
        back_button.clicked.connect(self.return_to_home)
        
        title = AnimatedLabel("Export Results")
        title.setObjectName("exportTitle")
        
        header_layout.addWidget(back_button)
        header_layout.addWidget(title, alignment=Qt.AlignCenter)
        header_layout.addSpacing(150)  # Balance the layout
        
        content_layout.addLayout(header_layout)

        # Create a horizontal layout for options and preview
        main_content_layout = QHBoxLayout()
        main_content_layout.setSpacing(20)

        # Left side - Export Options
        options_container = QFrame()
        options_container.setFixedWidth(400)  # Fixed width for options
        options_container.setObjectName("optionsContainer")
        options_layout = QVBoxLayout(options_container)
        options_layout.setSpacing(15)  # Reduced spacing
        options_layout.setContentsMargins(20, 20, 20, 20)

        # Date Range Selection
        date_group = QFrame()
        date_group.setObjectName("optionGroup")
        date_layout = QVBoxLayout(date_group)
        date_layout.setSpacing(10)
        
        date_title = QLabel("Select Date Range")
        date_title.setObjectName("optionTitle")
        date_layout.addWidget(date_title)

        date_buttons_layout = QGridLayout()  # Changed to grid layout
        date_buttons_layout.setSpacing(10)
        date_ranges = ["Last 7 Days", "Last 30 Days", "Last 3 Months", "All Time"]
        
        for i, date_range in enumerate(date_ranges):
            btn = QPushButton(date_range)
            btn.setObjectName("dateRangeButton")
            btn.setCheckable(True)
            btn.setCursor(Qt.PointingHandCursor)
            if date_range == "All Time":
                btn.setChecked(True)
            btn.clicked.connect(lambda checked, r=date_range: self.set_date_range(r))
            date_buttons_layout.addWidget(btn, i//2, i%2)
        
        date_layout.addLayout(date_buttons_layout)
        options_layout.addWidget(date_group)

        # Custom Range Selection (in a more compact layout)
        custom_range = QFrame()
        custom_range.setObjectName("optionGroup")
        custom_layout = QGridLayout(custom_range)
        custom_layout.setSpacing(10)
        
        from_date = QDateEdit()
        from_date.setCalendarPopup(True)
        from_date.setDate(QDate.currentDate().addDays(-30))
        to_date = QDateEdit()
        to_date.setCalendarPopup(True)
        to_date.setDate(QDate.currentDate())
        
        custom_layout.addWidget(QLabel("From:"), 0, 0)
        custom_layout.addWidget(from_date, 0, 1)
        custom_layout.addWidget(QLabel("To:"), 1, 0)
        custom_layout.addWidget(to_date, 1, 1)
        
        options_layout.addWidget(custom_range)

        # Export Format Selection
        format_group = QFrame()
        format_group.setObjectName("optionGroup")
        format_layout = QVBoxLayout(format_group)
        format_layout.setSpacing(10)
        
        format_title = QLabel("Select Export Format")
        format_title.setObjectName("optionTitle")
        format_layout.addWidget(format_title)

        format_buttons_layout = QGridLayout()  # Changed to grid layout
        format_buttons_layout.setSpacing(10)
        formats = [
            ("CSV File", "csv", "📊"),
            ("Text File", "txt", "📝"),
            ("Excel File", "xlsx", "📘"),
            ("PDF Document", "pdf", "📄")
        ]
        
        for i, (format_name, format_id, icon) in enumerate(formats):
            btn = QPushButton(f"{icon} {format_name}")
            btn.setObjectName("formatButton")
            btn.setCheckable(True)
            btn.setCursor(Qt.PointingHandCursor)
            if format_id == "csv":
                btn.setChecked(True)
            btn.clicked.connect(lambda checked, f=format_id: self.set_format(f))
            format_buttons_layout.addWidget(btn, i//2, i%2)
        
        format_layout.addLayout(format_buttons_layout)
        options_layout.addWidget(format_group)

        # Data Selection with better organization
        data_group = QFrame()
        data_group.setObjectName("optionGroup")
        data_layout = QVBoxLayout(data_group)
        data_layout.setSpacing(10)
        
        data_title = QLabel("Select Data to Export")
        data_title.setObjectName("optionTitle")
        data_layout.addWidget(data_title)

        data_grid = QGridLayout()
        data_grid.setSpacing(8)  # Reduced spacing
        data_options = [
            ("Test Scores", True), ("Date & Time", True),
            ("Subject Details", True), ("Time Taken", True),
            ("Correct Answers", True), ("Wrong Answers", True),
            ("Performance Analysis", False), ("Detailed Responses", False)
        ]
        
        for i, (option, checked) in enumerate(data_options):
            checkbox = QCheckBox(option)
            checkbox.setChecked(checked)
            data_grid.addWidget(checkbox, i//2, i%2)
        
        data_layout.addLayout(data_grid)
        options_layout.addWidget(data_group)

        # Right side - Preview Section
        preview_container = QFrame()
        preview_container.setObjectName("previewContainer")
        preview_layout = QVBoxLayout(preview_container)
        preview_layout.setSpacing(15)
        
        preview_header = QHBoxLayout()
        preview_title = QLabel("Preview")
        preview_title.setObjectName("previewTitle")
        preview_header.addWidget(preview_title)
        
        refresh_btn = QPushButton("🔄 Refresh Preview")
        refresh_btn.setObjectName("refreshButton")
        refresh_btn.setCursor(Qt.PointingHandCursor)
        preview_header.addWidget(refresh_btn, alignment=Qt.AlignRight)
        
        preview_layout.addLayout(preview_header)
        
        # Preview table
        preview_table = QTableWidget()
        preview_table.setRowCount(5)
        preview_table.setColumnCount(6)
        preview_table.setHorizontalHeaderLabels([
            "Date", "Subject", "Score", "Time Taken", "Correct", "Wrong" #TODO chabiba makach kifech nejebdo chhal jaweb shih ou ghalet m database
        ])
        preview_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        json_file_path = '././data/users.json'
        username = self.user["username"]

        sample_data = self.format_scores(json_file_path, username)
        
        for row, data in enumerate(sample_data):
            for col, value in enumerate(data):
                item = QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignCenter)
                preview_table.setItem(row, col, item)
        
        preview_layout.addWidget(preview_table)

        # Add options and preview to main content layout
        main_content_layout.addWidget(options_container)
        main_content_layout.addWidget(preview_container, stretch=1)
        content_layout.addLayout(main_content_layout)

        # Export Button at the bottom
        export_btn = HoverButton("Export Results")
        export_btn.setObjectName("exportButton")
        export_btn.setFixedWidth(200)
        export_btn.setFixedHeight(50)
        export_btn.clicked.connect(self.export_results)
        
        content_layout.addWidget(export_btn, alignment=Qt.AlignCenter)

        # Add the content card to main layout
        main_layout.addWidget(content_card)
        
    def load_user_data(self, json_file_path, username):
        """Loads user data from a JSON file based on the username."""
        with open(json_file_path, 'r') as f:
            data = json.load(f)
        # Find the user with the matching username
        for user in data:
            if user.get("username") == username:
                return user
        return None  # Return None if user not found

    def format_scores(self, json_file_path, username):
        """Formats scores dynamically from the JSON file."""
        # Load user data
        user_data = self.load_user_data(json_file_path, username)
        if not user_data:
            return []  # Return an empty list if user not found

        # Extract scores from the user data
        scores = user_data.get("scores", [])

        # Convert each score entry to the desired format
        formatted_scores = []
        for score in scores:
            date = score.get("date", "").split(" ")[0]  # Extract the date only
            chapter = score["subject"].get("chapter", "Unknown Chapter")
            points = f"{score.get('points', 0)}%"  # Format points as percentage
            duration = "N/A"  # Assuming duration is not in the database; set default
            status = "Passed" if score.get("points", 0) >=50 else "Failed"  # Determine pass/fail

            # Append the formatted entry
            formatted_scores.append((date, chapter, points, duration, status))

        return formatted_scores


    def set_date_range(self, range_value):
        self.selected_date_range = range_value
        # Update buttons state
        for btn in self.findChildren(QPushButton, "dateRangeButton"):
            btn.setChecked(btn.text() == range_value)

    def set_format(self, format_value):
        self.selected_format = format_value
        # Update buttons state
        for btn in self.findChildren(QPushButton, "formatButton"):
            btn.setChecked(btn.text().split()[-1].lower().startswith(format_value))

    def export_results(self):
        # Show loading state
        export_btn = self.findChild(HoverButton, "exportButton")
        original_text = export_btn.text()
        export_btn.setText("Exporting...")
        export_btn.setEnabled(False)

        # Simulate export process
        QTimer.singleShot(2000, lambda: self.show_export_success(export_btn, original_text))

    def show_export_success(self, button, original_text):
        # Create success message
        msg = QMessageBox(self)
        msg.setWindowTitle("Success")
        msg.setText("Results exported successfully!")
        msg.setInformativeText(f"File saved as: results_{QDate.currentDate().toString('yyyy-MM-dd')}.{self.selected_format}")
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

    def apply_theme(self, is_light_mode):
        # [Previous theme code remains the same, add these new styles:]
        if is_light_mode:
            self.setStyleSheet("""
                /* ... [Previous light theme styles] ... */
                #optionsContainer {
                    background-color: #F8FAFC;
                    border-radius: 15px;
                    border: 1px solid #E2E8F0;
                }
                #optionGroup {
                    background-color: white;
                    border-radius: 10px;
                    border: 1px solid #E2E8F0;
                    padding: 20px;
                }
                #optionTitle {
                    color: #1E293B;
                    font-size: 18px;
                    font-weight: bold;
                    margin-bottom: 15px;
                }
                #dateRangeButton, #formatButton {
                    background-color: white;
                    border: 2px solid #E2E8F0;
                    border-radius: 8px;
                    padding: 10px 20px;
                    color: #4A5568;
                }
                #dateRangeButton:checked, #formatButton:checked {
                    background-color: #4F46E5;
                    color: white;
                    border-color: #4F46E5;
                }
                QCheckBox {
                    color: #4A5568;
                    font-size: 14px;
                    padding: 5px;
                }
                QCheckBox::indicator {
                    width: 18px;
                    height: 18px;
                }
                #refreshButton {
                    background-color: #F1F5F9;
                    border: none;
                    border-radius: 5px;
                    padding: 8px 15px;
                    color: #4A5568;
                }
                #refreshButton:hover {
                    background-color: #E2E8F0;
                }
                #exportButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #4F46E5, stop:1 #7C3AED);
                    color: white;
                    border: none;
                    border-radius: 25px;
                    font-weight: bold;
                }
                #exportButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #4338CA, stop:1 #6D28D9);
                }
            """)
        else:
            self.setStyleSheet("""
                /* ... [Previous dark theme styles] ... */
                #optionsContainer {
                    background-color: #0F172A;
                    border-radius: 15px;
                    border: 1px solid #2D3748;
                }
                #optionGroup {
                    background-color: #1E293B;
                    border-radius: 10px;
                    border: 1px solid #2D3748;
                    padding: 20px;
                }
                #optionTitle {
                    color: white;
                    font-size: 18px;
                    font-weight: bold;
                    margin-bottom: 15px;
                }
                #dateRangeButton, #formatButton {
                    background-color: #1E293B;
                    border: 2px solid #2D3748;
                    border-radius: 8px;
                    padding: 10px 20px;
                    color: #E2E8F0;
                }
                #dateRangeButton:checked, #formatButton:checked {
                    background-color: #4F46E5;
                    color: white;
                    border-color: #4F46E5;
                }
                QCheckBox {
                    color: #E2E8F0;
                    font-size: 14px;
                    padding: 5px;
                }
                QCheckBox::indicator {
                    width: 18px;
                    height: 18px;
                }
                #refreshButton {
                    background-color: #2D3748;
                    border: none;
                    border-radius: 5px;
                    padding: 8px 15px;
                    color: #E2E8F0;
                }
                #refreshButton:hover {
                    background-color: #374151;
                }
                #exportButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #4F46E5, stop:1 #7C3AED);
                    color: white;
                    border: none;
                    border-radius: 25px;
                    font-weight: bold;
                }
                #exportButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #4338CA, stop:1 #6D28D9);
                }
            """)

    def return_to_home(self):
        self.close()
        if self.parent:
            self.parent.show()
                    
                    
class MCQHistoryPage(QMainWindow):
    def __init__(self, user, parent=None, is_light_mode=False):
        super().__init__(parent)
        self.user = user  # Store user information
        self.parent = parent
        self.setup_ui()
        self.apply_theme(is_light_mode)
        print(f"Welcome {self.user['username']}!")

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

        # Dynamic stat cards
        stat_cards = self.get_dynamic_stat_cards()

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
    
    def load_user_data(self, json_file_path, username):
        """Loads user data from a JSON file based on the username."""
        with open(json_file_path, 'r') as f:
            data = json.load(f)
        # Find the user with the matching username
        for user in data:
            if user.get("username") == username:
                return user
        return None  # Return None if user not found

    def format_scores(self, json_file_path, username):
        """Formats scores dynamically from the JSON file."""
        # Load user data
        user_data = self.load_user_data(json_file_path, username)
        if not user_data:
            return []  # Return an empty list if user not found

        # Extract scores from the user data
        scores = user_data.get("scores", [])

        # Convert each score entry to the desired format
        formatted_scores = []
        for score in scores:
            date = score.get("date", "").split(" ")[0]  # Extract the date only
            chapter = score["subject"].get("chapter", "Unknown Chapter")
            points = f"{score.get('points', 0)}%"  # Format points as percentage
            duration = "N/A"  # Assuming duration is not in the database; set default
            status = "Passed" if score.get("points", 0) >=50 else "Failed"  # Determine pass/fail

            # Append the formatted entry
            formatted_scores.append((date, chapter, points, duration, status))

        return formatted_scores
    
    def get_dynamic_stat_cards(self):
        """Generates dynamic stat cards based on user data."""
        json_file_path = '././data/users.json'
        username = self.user["username"]

        # Load and format the user data
        formatted_scores = self.format_scores(json_file_path, username)

        total_tests_taken = len(formatted_scores)
        average_score = self.calculate_average_score(formatted_scores)
        best_performance = self.get_best_performance(formatted_scores)
        tests_this_month = self.get_tests_this_month(formatted_scores)

        # Return the dynamically generated stat cards
        return [
            ("Total Tests Taken", str(total_tests_taken), "📝"),
            ("Average Score", f"{average_score}%", "📊"),
            ("Best Performance", f"{best_performance}%", "🏆"),
            ("Tests This Month", str(tests_this_month), "📅")
        ]

    def calculate_average_score(self, scores):
        """Calculates the average score from the formatted scores."""
        total_score = 0
        count = 0
        for score in scores:
            # Remove '%' and convert to float to handle decimal values like '12.5%'
            try:
                total_score += float(score[2].strip('%'))  # Convert to float after removing '%'
                count += 1
            except ValueError:
                continue  # If a ValueError occurs (e.g., score is not valid), skip that score

        return total_score / count if count else 0  # Return 0 if no valid scores

    def get_best_performance(self, scores):
        """Gets the best performance from the formatted scores."""
        return max([float(score[2].strip('%')) for score in scores], default=0)

    def get_tests_this_month(self, scores):
        """Gets the number of tests taken this month."""
        current_month = QDate.currentDate().month()
        return sum(1 for score in scores if QDate.fromString(score[0], "yyyy-MM-dd").month() == current_month)

    def add_sample_data(self):
        json_file_path = '././data/users.json'
        username = self.user["username"]

        test_data = self.format_scores(json_file_path, username)

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
    def __init__(self, parent=None, is_light_mode=False):
        super().__init__(parent)
        self.is_light_mode = is_light_mode
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
                req.setStyleSheet(f"color: {'#64748B' if self.is_light_mode else '#94A3B8'}; font-size: 14px;")

        
        # Update strength indicator
        self.strength_bar.setValue(score)
        
        # Update strength label
        if score <= 20:
            strength_text = "Weak"
            strength_color = "#EF4444"  # Red
        elif score <= 60:
            strength_text = "Medium"
            strength_color = "#F59E0B"  # Yellow
        elif score <= 80:
            strength_text = "Strong"
            strength_color = "#10B981"  # Green
        else:
            strength_text = "very Strong"
            strength_color = "#0fa900"  # DARK Green
            
        self.strength_label.setText(strength_text)
        self.strength_label.setStyleSheet(f"color: {strength_color}; font-size: 14px; font-weight: bold;")
        self.strength_bar.setStyleSheet(f"""
            QProgressBar {{
                border-radius: 4px;
                background-color: {'#F8FAFC' if self.is_light_mode else '#0F172A'};
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
        if self.is_light_mode:
            # Light theme styles
            self.setStyleSheet("""
                QFrame {
                    background: transparent;
                }
                
                #passwordInput {
                    padding: 12px 15px;
                    border: 2px solid #E2E8F0;
                    border-radius: 10px;
                    font-size: 16px;
                    background-color: white;
                    min-width: 300px;
                    color: #1E293B;
                }
                
                #passwordInput:focus {
                    border-color: #4F46E5;
                }
                
                #togglePassword {
                    background-color: white;
                    border: 2px solid #E2E8F0;
                    border-radius: 10px;
                    padding: 5px;
                    font-size: 20px;
                    margin-left: 10px;
                    color: #1E293B;
                }
                
                #togglePassword:hover {
                    background-color: #F8FAFC;
                    border-color: #4F46E5;
                }
                
                #strengthBar {
                    border-radius: 4px;
                    background-color: #F8FAFC;
                    min-width: 200px;
                    border: 1px solid #E2E8F0;
                    height: 8px;
                }
                
                #strengthLabel {
                    font-size: 14px;
                    font-weight: bold;
                    margin-left: 15px;
                    min-width: 100px;
                    color: #1E293B;
                }
                
                #requirement {
                    font-size: 14px;
                    padding: 3px 0;
                    color: #64748B;
                }
                
                #requirement[met="true"] {
                    color: #10B981;
                }
            """)
        else:
            # Dark theme styles
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
                    color: #10B981;
                }
            """)


class ProfilePage(QMainWindow):
    def __init__(self, user, parent=None, is_light_mode=False):
        super().__init__(parent)
        self.user = user  # Store user information
        self.parent = parent
        self.setup_ui(is_light_mode)
        self.apply_theme(is_light_mode)
        print(f"Welcome {self.user['username']}!")

    def setup_ui(self, theme):
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

        self.password_field = PasswordField(is_light_mode=theme)

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
        
        # Get all the field values
        profile_data = {
            'full_name': self.fields['full_name'].text(),
            'email': self.fields['email'].text(),
            'username': self.fields['username'].text(),
            'password': self.password_field.get_password() if self.password_field.get_password() else None
        }
        
        # Validate fields
        if not self.validate_fields(profile_data):
            save_button.setText(original_text)
            save_button.setEnabled(True)
            return
        
        try:
            # Path to your local JSON file
            json_file_path = '././data/users.json'

            # Read the current content of the JSON file
            with open(json_file_path, 'r') as f:
                data = json.load(f)

            # Assume the current user is stored in self.user
            print("here", self.user["username"])
            current_user = self.user

            # Locate and update the user in the JSON data (assuming `data` is a list)
            user_found = False
            for user in data:
                if user['username'] == current_user['username']:  # Match by username or unique identifier
                    user['fullname'] = profile_data['full_name']
                    user['email'] = profile_data['email']
                    user['username'] = profile_data['username']
                    if profile_data['password']:
                        hashed_password = bcrypt.hashpw(profile_data['password'].encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
                        user['password'] = hashed_password
                    user_found = True
                    break

            if not user_found:
                print("Error: User not found in the data!")

            # Save the updated data back to the JSON file
            with open(json_file_path, 'w') as f:
                json.dump(data, f, indent=4)


            
            # Simulate network delay
            QTimer.singleShot(1500, lambda: self.show_save_success(save_button, original_text))
            
        except Exception as e:
            # Show error message
            msg = QMessageBox(self)
            msg.setWindowTitle("Error")
            msg.setText(f"Failed to save changes: {str(e)}")
            msg.setIcon(QMessageBox.Critical)
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
                    background-color: #EF4444;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    padding: 8px 16px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #DC2626;
                }
            """)
            msg.exec_()
            
            # Reset button state
            save_button.setText(original_text)
            save_button.setEnabled(True)

    def validate_fields(self, profile_data):
        # Validate email format
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, profile_data['email']):
            self.show_error("Invalid email format")
            return False
        
        # Validate required fields
        if not profile_data['full_name'] or not profile_data['username']:
            self.show_error("Please fill in all required fields")
            return False
        
        # Validate username format (example: alphanumeric only)
        if not profile_data['username'].isalnum():
            self.show_error("Username must contain only letters and numbers")
            return False
        
        # If password is being changed, validate it
        if profile_data['password']:
            if len(profile_data['password']) < 8:
                self.show_error("Password must be at least 8 characters long")
                return False
        
        return True

    def show_error(self, message):
        msg = QMessageBox(self)
        msg.setWindowTitle("Error")
        msg.setText(message)
        msg.setIcon(QMessageBox.Critical)
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
                background-color: #EF4444;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #DC2626;
            }
        """)
        msg.exec_()

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
            if icon_text == "❌ Sign out":
                action.triggered.connect(self.sign_out)  # Connect to the sign-out method

    def sign_out(self):
        # Implement your logout logic here
        print("User signed out.")
        # Example: Redirect to login screen or exit application
        QApplication.instance().quit()


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
    
    def setup_menu_actions(self, user):
        # Connect menu actions to their respective functions
        for action in self.dropdown_button.menu.actions():
            if action.text() == "👤 Profile":
                action.triggered.connect(lambda checked, u=user: self.open_profile(u))
            elif action.text() == "📊 MCQ History":
                action.triggered.connect(lambda checked, u=user: self.open_mcq_history(u))
            elif action.text() == "💾 Export Results":
                action.triggered.connect(lambda checked, u=user: self.open_export_results(u))
            elif action.text() == "📞 Contact":
                action.triggered.connect(lambda checked, u=user: self.open_contact(u))


    def open_contact(self, user):
        self.contact_page = ContactPage(user, self, self.theme_toggle.isChecked())
        self.contact_page.showFullScreen()

    def open_export_results(self, user):
        self.export_results_page = ExportResultsPage(user, self, self.theme_toggle.isChecked())
        self.export_results_page.showFullScreen()

    def open_mcq_history(self, user):
        self.mcq_history_page = MCQHistoryPage(user, self, self.theme_toggle.isChecked())
        self.mcq_history_page.showFullScreen()

    def open_profile(self, user):
        self.profile_page = ProfilePage(user, self, self.theme_toggle.isChecked())
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
        enroll_btn.clicked.connect(lambda checked, t=title: self.handle_enroll(t))
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

    # Add this new method to handle enrollment
   
    def handle_enroll(self, course_title):
        # TODO : Add your enrollment logic here
        # For example:
        print(f"Enrolling in course: {course_title}")
        # You could:
        # 1. Open an enrollment confirmation dialog
        # 2. Make an API call to your backend
        # 3. Update the database
        # 4. Show a success message
        # 5. Navigate to the course content

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

    def __init__(self, user, parent=None):
        """
        Initialize the home page with user data.
        """
        super().__init__(parent)
        self.user = user  # Store user information
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

        self.setup_menu_actions(self.user)

        # Create center content container
        center_content = QWidget()
        center_layout = QVBoxLayout(center_content)
        center_layout.setSpacing(20)

        # Personalized title using user's name
        title = QLabel(f"Welcome {self.user['username']}!")  # Use user data here
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

        # Path to your subjects.json file
        file_path = '././data/subjects.json'

        # Load courses
        # courses = self.load_courses_from_json(file_path)
        try:
            with open(file_path, 'r') as file:
                courses_file = json.load(file)
                courses = courses_file
        except FileNotFoundError:
            print(f"Error: The file '{file_path}' was not found.")
            return []
        except json.JSONDecodeError:
            print(f"Error: Failed to decode JSON from the file '{file_path}'.")
            return []

        for course in courses:
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
        """
        Load courses from a local JSON file.
        """

    def open_settings(self):
        """
        Example callback function for the dropdown menu.
        """
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