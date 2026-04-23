from PySide6.QtWidgets import QVBoxLayout, QWidget, QScrollArea, QPushButton, QLabel
from PySide6.QtCore import Qt
from .question_widget import QuestionWidget

class QuestionDisplay(QWidget):
    """Widget to display questions."""
    widget_list = []

    def __init__(self, questionsList):
        super().__init__()
        self.questionsList = questionsList
        self.__initLayout()
        self.__initScrollWidget()
        self.widget_list.clear() # Clear widget list before displaying new questions
        self.displayQuestions(self.scrollable_widget_layout)
        self.addFinishButton()

    def __initLayout(self):
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

    def __initScrollWidget(self):
        self.scrollable_widget = QWidget()
        self.scrollable_widget_layout = QVBoxLayout()
        self.scrollable_widget.setLayout(self.scrollable_widget_layout)

        scroll = QScrollArea()
        scroll.setWidget(self.scrollable_widget)
        scroll.setWidgetResizable(True)
        self.main_layout.addWidget(scroll)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def displayQuestions(self, scrollable_widget_layout):
        for question in self.questionsList:
            question_widget = QuestionWidget(question)
            self.widget_list.append(question_widget)
            question_widget.label.setText( f"{len(self.widget_list)}. {question_widget.label.text()}") # Numbering questions
            scrollable_widget_layout.addWidget(question_widget)

    def addFinishButton(self):
        self.finish_button = QPushButton('Finish Quiz')
        self.finish_button.clicked.connect(self.finishButtonClicked)
        self.main_layout.addWidget(self.finish_button)

    def finishButtonClicked(self):
        print('Clicked finish')
        self.finish_button.deleteLater()
        self.displayResults()

    def displayResults(self):
        print('Results')
        total_questions = len(self.widget_list)
        total_points = 0
        user_points = 0
        user_good_answers = 0
        # Result calculation
        for widget in self.widget_list:
            # Color button text based on which contain correct answer. Disable all button from manipulation.
            for button in widget.a_button_group.buttons(): 
                if widget.question.correct_answer in button.text():
                    button.setStyleSheet('color: #2ecc71;')
                else:
                    button.setStyleSheet('color: #e74c3c;')
                button.setEnabled(False)
            # Calculate results, color QuestionWidget Frame based on user answer
            total_points += widget.question.points
            if widget.correct_answer:
                widget.setStyleSheet('''
                                     QFrame#questionFrame {
                                        border: 2px solid #2ecc71;
                                     }
                                     ''')
                user_points += widget.question.points
                user_good_answers += 1
            else:
                widget.setStyleSheet('''
                                     QFrame#questionFrame {
                                        border: 2px solid #e74c3c;
                                     }
                                     ''')

        result_label = QLabel("Results", alignment=Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(result_label)
        score_label = QLabel(f'Score - {user_points}/{total_points} points. {(user_points/float(total_points*0.01)):.2f}%', alignment=Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(score_label)
        good_answers_label = QLabel(f'Good answers - {user_good_answers}/{total_questions}', alignment=Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(good_answers_label)
