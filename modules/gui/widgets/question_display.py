from PySide6.QtWidgets import QVBoxLayout, QWidget, QScrollArea, QPushButton, QLabel
from PySide6.QtCore import Qt
from .question_widget import QuestionWidget

class QuestionDisplay(QWidget):
    """
    Widget to display questions, handle and check user answers. 
    Display results and format question widgets accordingly.
    """
    widget_list = []

    def __init__(self, questionsList):
        super().__init__()
        self.questionsList = questionsList
        self.__initLayout()
        self.__initScrollableWidget()
        self.widget_list.clear() # Clear widget list before displaying new questions
        self.displayQuestions(self.scrollable_widget_layout)
        self.addFinishQuizButton()

    def __initLayout(self):
        """Initialize main widget layout."""
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

    def __initScrollableWidget(self):
        """Initialize scrollable widget to display questions."""
        self.scrollable_widget = QWidget()
        self.scrollable_widget_layout = QVBoxLayout()
        self.scrollable_widget.setLayout(self.scrollable_widget_layout)

        scroll = QScrollArea()
        scroll.setFrameShape(QScrollArea.Shape.NoFrame) # Remove scroll area default frame
        scroll.setWidget(self.scrollable_widget)
        scroll.setWidgetResizable(True)
        self.main_layout.addWidget(scroll)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def displayQuestions(self, scrollable_widget_layout):
        """Display questions in scrollable widget."""
        for question in self.questionsList:
            question_widget = QuestionWidget(question)
            self.widget_list.append(question_widget)
            question_widget.label.setText( f"{len(self.widget_list)}. {question_widget.label.text()}") # Numbering questions
            scrollable_widget_layout.addWidget(question_widget)

    def calculateScore(self):
        """Calculate total points, user points and good answers."""
        self.total_question_points = 0
        self.user_points = 0
        self.user_good_answers = 0
        for widget in self.widget_list:
            self.total_question_points += widget.question.points
            if widget.correct_answer:
                self.user_points += widget.question.points
                self.user_good_answers += 1

    def formatQuestionWidgetsStyle(self):
        """Format QuestionWidgets frame and button text based on correct/incorrect answer."""
        for widget in self.widget_list:
            # Color widget frames based on user_answer
            if widget.correct_answer:
                widget.setProperty('answerState', 'correct')
            else:
                widget.setProperty('answerState', 'incorrect')
            # Color button text based on which contain correct answer
            for button in widget.a_button_group.buttons():
                if widget.question.correct_answer in button.text():
                    button.setProperty('containAnswer', 'correct')
                else:
                    button.setProperty('containAnswer', 'incorrect')
                button.style().polish(button) # Refresh button style
                button.setEnabled(False) # Disable all button from manipulation
            # Refresh widget style to apply new properties
            widget.style().polish(widget)

    def displayResults(self):
        """Display quiz results."""
        quiz_result_label = QLabel("Results", alignment=Qt.AlignmentFlag.AlignCenter)
        quiz_result_label.setObjectName('quizResultLabel')

        user_good_answers_label = QLabel(f'Good answers - {self.user_good_answers}/{len(self.questionsList)}', alignment=Qt.AlignmentFlag.AlignCenter)
        user_good_answers_label.setObjectName('userGoodAnswersLabel')

        quiz_score_label = QLabel(f'Score - {self.user_points}/{self.total_question_points} points. {(self.user_points/float(self.total_question_points*0.01)):.2f}%', alignment=Qt.AlignmentFlag.AlignCenter)
        quiz_score_label.setObjectName('quizScoreLabel')

        self.main_layout.addWidget(quiz_result_label)
        self.main_layout.addWidget(quiz_score_label)
        self.main_layout.addWidget(user_good_answers_label)

    def addFinishQuizButton(self):
        """Add button to finish quiz."""
        self.finish_quiz_button = QPushButton('Finish Quiz')
        self.finish_quiz_button.setObjectName('finishQuizButton')
        self.finish_quiz_button.clicked.connect(self.finishQuizButtonClicked)
        self.main_layout.addWidget(self.finish_quiz_button)

    def finishQuizButtonClicked(self):
        """Handle finish quiz button click, calculate score, format question widgets and display results."""
        print('Clicked finish')
        self.finish_quiz_button.deleteLater()
        self.calculateScore()
        self.formatQuestionWidgetsStyle()
        self.displayResults()
