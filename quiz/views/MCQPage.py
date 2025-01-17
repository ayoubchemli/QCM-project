from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import json
from datetime import datetime
import sys
import os

class MCQPage(QMainWindow):
    def __init__(self, appstate, is_light_mode=True):
        super().__init__()
        self.appstate = appstate
        self.current_question = 0
        self.score = 0
        self.answers = {}
        self.setup_questions()
        self.setup_ui()
        self.apply_theme(is_light_mode)
        self.start_timer()
        self.showFullScreen()
        
        # Setup animation properties
        self.opacity_effect = QGraphicsOpacityEffect(self.question_card)
        self.question_card.setGraphicsEffect(self.opacity_effect)
        self.fade_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_animation.setDuration(300)  # 300ms duration
        


        
    def setup_questions(self):
        self.questions = self.appstate.getQuestions()
        self.total_questions = len(self.questions)

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(30)
        main_layout.setContentsMargins(50, 40, 50, 40)

        timer_widget = QWidget()
        timer_layout = QHBoxLayout(timer_widget)
        
        self.time_left = self.appstate.getTestInstance().subject.get_time_limit() * 60
        self.timer_label = QLabel(f"Time Left: {self.time_left}s")
        self.timer_label.setObjectName("timerLabel")
        self.timer_label.setAlignment(Qt.AlignCenter)
        
        self.timer_progress = QProgressBar()
        self.timer_progress.setRange(0, self.time_left)
        self.timer_progress.setValue(self.time_left)
        self.timer_progress.setObjectName("timerProgress")
        self.timer_progress.setFixedHeight(8)
        
        timer_layout.addWidget(self.timer_label)
        timer_layout.addWidget(self.timer_progress)
        main_layout.addWidget(timer_widget)

        # Question Card
        self.question_card = QFrame()
        self.question_card.setObjectName("questionCard")
        card_layout = QVBoxLayout(self.question_card)
        card_layout.setSpacing(20)
        card_layout.setContentsMargins(40, 40, 40, 40)

        # Question Text
        self.question_label = QLabel()
        self.question_label.setObjectName("questionLabel")
        self.question_label.setWordWrap(True)
        self.question_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        card_layout.addWidget(self.question_label)

        # Options
        self.option_group = QButtonGroup(self)
        self.option_buttons = []
        for i in range(4):
            button = QRadioButton()
            button.setObjectName(f"optionButton{i}")
            button.setCursor(Qt.PointingHandCursor)
            self.option_group.addButton(button, i)
            self.option_buttons.append(button)
            card_layout.addWidget(button)

        # Add stretch to center content vertically
        card_layout.addStretch()

        # Navigation Buttons
        nav_layout = QHBoxLayout()
        
        self.prev_button = QPushButton("Previous")
        self.prev_button.setObjectName("navButton")
        self.prev_button.clicked.connect(self.prev_question)
        self.prev_button.setFixedWidth(150)
        
        self.next_button = QPushButton("Next")
        self.next_button.setObjectName("navButton")
        self.next_button.clicked.connect(self.next_question)
        self.next_button.setFixedWidth(150)
        
        self.submit_button = QPushButton("Submit Quiz")
        self.submit_button.setObjectName("submitButton")
        self.submit_button.clicked.connect(self.show_results)
        self.submit_button.setFixedWidth(150)
        self.submit_button.hide()

        nav_layout.addStretch()
        nav_layout.addWidget(self.prev_button)
        nav_layout.addWidget(self.next_button)
        nav_layout.addWidget(self.submit_button)
        nav_layout.addStretch()

        card_layout.addLayout(nav_layout)
        main_layout.addWidget(self.question_card)

        # Progress Bar at bottom
        self.progress = QProgressBar()
        self.progress.setRange(0, len(self.questions))
        self.progress.setValue(1)
        self.progress.setFormat("Question %v of %m")
        self.progress.setObjectName("progressBar")
        self.progress.setFixedHeight(10)
        main_layout.addWidget(self.progress)

        # Add shadow to question card
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 50))
        shadow.setOffset(0, 4)
        self.question_card.setGraphicsEffect(shadow)

        self.load_question(0)
        self.update_navigation_buttons()
        
        self.timer_animation = QPropertyAnimation(self.timer_label, b"styleSheet")
        self.timer_animation.setDuration(500)

    def start_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)

    def update_timer(self):
        self.time_left -= 1
        self.timer_progress.setValue(self.time_left)
        self.timer_label.setText(f"Time Left: {self.time_left}s")
        
        # Flash timer when time is running low
        if self.time_left <= 10:
            if self.time_left % 2 == 0:
                self.timer_animation.setStartValue("color: #EF4444; font-size: 22px;")
                self.timer_animation.setEndValue("color: #EF4444; font-size: 20px;")
            else:
                self.timer_animation.setStartValue("color: #EF4444; font-size: 20px;")
                self.timer_animation.setEndValue("color: #EF4444; font-size: 22px;")
            self.timer_animation.start()
        
        if self.time_left <= 0:
            self.timer.stop()
            self.show_results()
            
    def load_next_question_content(self):
        # Load new question content
        self.load_question(self.current_question)
        
        # Fade in
        self.fade_animation.finished.disconnect()
        self.fade_animation.setStartValue(0.0)
        self.fade_animation.setEndValue(1.0)
        self.fade_animation.start()
            
    def animate_question_transition(self):
        # Fade out
        self.fade_animation.setStartValue(1.0)
        self.fade_animation.setEndValue(0.0)
        self.fade_animation.finished.connect(self.load_next_question_content)
        self.fade_animation.start()

    def load_question(self, index):
        if index < len(self.questions):
            question = self.questions[index]
            self.question_label.setText(f"Q{index + 1}. {question['question']}")
            
            # Load options and restore previous answer if exists
            for i, option in enumerate(question['answers']):
                self.option_buttons[i].setText(f"{chr(65 + i)}. {option}")
                self.option_buttons[i].setChecked(False)
            
            if index in self.answers:
                self.option_buttons[self.answers[index]].setChecked(True)

    def save_current_answer(self):
        selected_button = self.option_group.checkedButton()
        if selected_button:
            self.answers[self.current_question] = self.option_group.id(selected_button)

    def prev_question(self):
        self.save_current_answer()
        self.current_question -= 1
        self.progress.setValue(self.current_question + 1)
        self.animate_question_transition()
        self.update_navigation_buttons()

    def next_question(self):
        self.save_current_answer()
        self.current_question += 1
        self.progress.setValue(self.current_question + 1)
        self.animate_question_transition()
        self.update_navigation_buttons()

    def update_navigation_buttons(self):
        self.prev_button.setEnabled(self.current_question > 0)
        
        if self.current_question == len(self.questions) - 1:
            self.next_button.hide()
            self.submit_button.show()
        else:
            self.next_button.show()
            self.submit_button.hide()

    def show_results(self):
        self.save_current_answer()
        self.timer.stop()
        
        # Create results dialog with fade-in effect
        self.results = QDialog(self)
        self.results.setWindowTitle("Quiz Results")
        self.results.setModal(True)
        self.results.setMinimumWidth(600)
        
        # Override closeEvent for the results dialog
        def closeEvent(event):
            self.return_to_home()
            event.accept()
        
        # Add the closeEvent method to the dialog
        self.results.closeEvent = closeEvent
        
        # Apply fade-in effect to results dialog
        opacity_effect = QGraphicsOpacityEffect(self.results)
        self.results.setGraphicsEffect(opacity_effect)
        fade_animation = QPropertyAnimation(opacity_effect, b"opacity")
        fade_animation.setDuration(500)
        fade_animation.setStartValue(0.0)
        fade_animation.setEndValue(1.0)
        
        # Calculate score
        self.score = 0
        results_data = []

        answers_object = self.answers
        answers_array = list(answers_object.values())
        self.appstate.getTestInstance().set_list_of_answers(answers_array)
        
        for q_index in range(len(self.questions)):
            if q_index in self.answers:
                selected_option = self.answers[q_index]
                correct_answer = self.questions[q_index]['correctAnswer']
                is_correct = selected_option == correct_answer
                
                if is_correct:
                    self.score += 1
                    
                results_data.append({
                    'question_index': q_index,
                    'selected_option': selected_option,
                    'correct_option': correct_answer,
                    'is_correct': is_correct
                })

        # Create results window
        self.results = QDialog(self)
        self.results.setWindowTitle("Quiz Results")
        self.results.setModal(True)
        self.results.setMinimumWidth(600)
        
        layout = QVBoxLayout(self.results)
        
        # Calculate percentage
        percentage = (self.score / self.total_questions) * 100
        
        # Results summary
        summary = QLabel(f"Final Score: {self.score}/{self.total_questions} ({percentage:.1f}%)")
        summary.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px;")
        summary.setAlignment(Qt.AlignCenter)
        layout.addWidget(summary)
        
        # Detailed results in a scroll area
        scroll = QScrollArea()
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        
        for result in results_data:
            q_index = result['question_index']
            question = self.questions[q_index]
            
            # Question frame
            q_frame = QFrame()
            q_frame.setObjectName("resultCard")
            q_layout = QVBoxLayout(q_frame)
            
            # Question text
            q_text = QLabel(f"Q{q_index + 1}: {question['question']}")
            q_text.setWordWrap(True)
            q_layout.addWidget(q_text)
            
            # Answer details
            if result['is_correct']:
                status = QLabel("✓ Correct")
                status.setStyleSheet("color: #22C55E; font-weight: bold;")
            else:
                status = QLabel("✗ Incorrect")
                status.setStyleSheet("color: #EF4444; font-weight: bold;")
                
                selected = QLabel(f"Your answer: {question['answers'][result['selected_option']]}")
                correct = QLabel(f"Correct answer: {question['answers'][result['correct_option']]}")
                explanation = QLabel(f"Explanation: {question['explanation']}")
                explanation.setWordWrap(True)
                
                q_layout.addWidget(selected)
                q_layout.addWidget(correct)
                q_layout.addWidget(explanation)
            
            q_layout.addWidget(status)
            scroll_layout.addWidget(q_frame)
        
        scroll_content.setLayout(scroll_layout)
        scroll.setWidget(scroll_content)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)
        
        # Export button
        export_button = QPushButton("Export Results")
        export_button.clicked.connect(lambda: self.export_results(results_data))
        export_button.setFixedWidth(200)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(export_button)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        # Override closeEvent for the results dialog again since we recreated the dialog
        self.results.closeEvent = closeEvent
        
        self.results.show()
        fade_animation.start()
        
        self.results.exec_()

    def export_results(self, results_data):
        # Prepare results data
        export_data = {
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'total_questions': self.total_questions,
            'score': self.score,
            'percentage': (self.score / self.total_questions) * 100,
            'time_taken': self.appstate.getTestInstance().subject.get_time_limit() * 60 - self.time_left,
            'questions': []
        }

        for result in results_data:
            q_index = result['question_index']
            question = self.questions[q_index]
            export_data['questions'].append({
                'question': question['question'],
                'selected_answer': question['answers'][result['selected_option']],
                'correct_answer': question['answers'][result['correct_option']],
                'is_correct': result['is_correct'],
                'explanation': question['explanation']
            })

        # Generate default filename
        default_filename = f"{self.appstate.getUser().fullname.replace(' ', '')}__{self.appstate.getCourse().replace(' ', '')}_{datetime.now().strftime('%Y_%m_%d')}.json"

        # Determine the "records" folder path in the root of the project
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # Path to the current script
        records_folder = os.path.join(project_root, 'records')

        # Create the "records" folder if it doesn't exist
        if not os.path.exists(records_folder):
            os.makedirs(records_folder)

        # Open file dialog
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle('Save Results')
        file_dialog.setDirectory(records_folder)  # Start in user's home directory
        file_dialog.setAcceptMode(QFileDialog.AcceptSave)
        file_dialog.setNameFilter('JSON files (*.json)')
        file_dialog.selectFile(default_filename)

        if file_dialog.exec_() == QFileDialog.Accepted:
            # Get the selected file path
            selected_path = file_dialog.selectedFiles()[0]

            # Ensure .json extension
            if not selected_path.endswith('.json'):
                selected_path += '.json'

            try:
                # Save to selected location
                with open(selected_path, 'w') as f:
                    json.dump(export_data, f, indent=4)

                msg = QMessageBox()
                msg.setWindowTitle("Export Success")
                msg.setText(f"Results have been exported to:\n{selected_path}")
                msg.setIcon(QMessageBox.Information)
                msg.setStandardButtons(QMessageBox.Ok)
                msg.button(QMessageBox.Ok).setText("Return to Home")

                msg.exec_()
                self.return_to_home()  # Return to home when OK is clicked

            except Exception as e:
                QMessageBox.critical(self, "Export Error",
                                     f"An error occurred while saving the file:\n{str(e)}")

        self.results.close()

    def return_to_home(self):
        self.parent().setCurrentWidget(self.parent().parent().central_widget)

    def apply_theme(self, is_light_mode):
        if is_light_mode:
            self.setStyleSheet("""
                QMainWindow {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                        stop:0 #F8FAFC, stop:1 #F1F5F9);
                }
                #questionCard {
                    background-color: white;
                    border-radius: 20px;
                    border: 1px solid #E2E8F0;
                    min-height: 600px;
                }
                #questionLabel {
                    color: #1E293B;
                    font-size: 24px;
                    font-weight: bold;
                    margin-bottom: 30px;
                }
                QRadioButton {
                    background-color: #F8FAFC;
                    border: 2px solid #E2E8F0;
                    border-radius: 10px;
                    padding: 20px;
                    color: #1E293B;
                    font-size: 16px;
                    margin: 5px;
                }
                QRadioButton:hover {
                    background-color: #F1F5F9;
                    border-color: #4F46E5;
                }
                QRadioButton:checked {
                    background-color: #EEF2FF;
                    border-color: #4F46E5;
                }
                #navButton, #submitButton {
                    background-color: #4F46E5;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 12px 24px;
                    font-size: 16px;
                    font-weight: bold;
                }
                #navButton:hover, #submitButton:hover {
                    background-color: #4338CA;
                }
                #navButton:disabled {
                    background-color: #94A3B8;
                }
                #timerLabel {
                    color: #1E293B;
                    font-size: 20px;
                    font-weight: bold;
                    margin: 20px;
                }
                QProgressBar {
                    border: none;
                    background-color: #E2E8F0;
                    border-radius: 5px;
                    text-align: center;
                    color: transparent;
                }
                QProgressBar::chunk {
                    background: #4F46E5;
                    border-radius: 5px;
                }
                #resultCard {
                    background-color: white;
                    border: 1px solid #E2E8F0;
                    border-radius: 10px;
                    padding: 20px;
                    margin: 10px;
                }
                * {
                transition: background-color 0.3s, color 0.3s, border-color 0.3s;
                }
                #timerProgress {
                    border: none;
                    background-color: #E2E8F0;
                    border-radius: 4px;
                }
                #timerProgress::chunk {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                        stop:0 #4F46E5, stop:1 #6366F1);
                    border-radius: 4px;
                }
                """)
        else:
            self.setStyleSheet("""
                QMainWindow {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                        stop:0 #0F172A, stop:1 #1E293B);
                }
                #questionCard {
                    background-color: #1E293B;
                    border-radius: 20px;
                    border: 1px solid #334155;
                    min-height: 600px;
                }
                #questionLabel {
                    color: white;
                    font-size: 24px;
                    font-weight: bold;
                    margin-bottom: 30px;
                }
                QRadioButton {
                    background-color: #334155;
                    border: 2px solid #475569;
                    border-radius: 10px;
                    padding: 20px;
                    color: white;
                    font-size: 16px;
                    margin: 5px;
                }
                QRadioButton:hover {
                    background-color: #475569;
                    border-color: #6366F1;
                }
                QRadioButton:checked {
                    background-color: #312E81;
                    border-color: #6366F1;
                }
                #navButton, #submitButton {
                    background-color: #6366F1;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 12px 24px;
                    font-size: 16px;
                    font-weight: bold;
                }
                #navButton:hover, #submitButton:hover {
                    background-color: #4F46E5;
                }
                #navButton:disabled {
                    background-color: #64748B;
                }
                #timerLabel {
                    color: white;
                    font-size: 20px;
                    font-weight: bold;
                    margin: 20px;
                }
                QProgressBar {
                    border: none;
                    background-color: #334155;
                    border-radius: 5px;
                    text-align: center;
                    color: transparent;
                }
                QProgressBar::chunk {
                    background: #6366F1;
                    border-radius: 5px;
                }
                #resultCard {
                    background-color: #1E293B;
                    border: 1px solid #334155;
                    border-radius: 10px;
                    padding: 20px;
                    margin: 10px;
                }
                QDialog {
                    background-color: #0F172A;
                }
                QScrollArea {
                    background-color: #0F172A;
                    border: none;
                }
                QLabel {
                    color: white;
                }
                QPushButton {
                    background-color: #6366F1;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 12px 24px;
                    font-size: 16px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #4F46E5;
                }
                                * {
                transition: background-color 0.3s, color 0.3s, border-color 0.3s;
                }
                #timerProgress {
                    border: none;
                    background-color: #E2E8F0;
                    border-radius: 4px;
                }
                #timerProgress::chunk {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                        stop:0 #4F46E5, stop:1 #6366F1);
                    border-radius: 4px;
                }
            """)

# if __name__ == '__main__':
    
#     app = QApplication(sys.argv)
#     font = QFont("Segoe UI", 10)
#     app.setFont(font)
#     window = MCQPage(is_light_mode=False)
#     sys.exit(app.exec_())