from PySide6.QtWidgets import QVBoxLayout, QWidget, QScrollArea, QPushButton
from PySide6.QtCore import Qt
from .items import QuestionWidget, ResultWidget
from ....questions import Question

class QuestionDisplay(QWidget):
    """
    Widget to display questions, handle and check user answers. 
    Display results and format question widgets accordingly.
    """
    widget_list = []

    def __init__(self, questions_list: list[Question]) -> None:
        super().__init__()
        self.questions_list = questions_list
        self.__initLayout()
        self.__initScrollableWidget()
        self.widget_list.clear() # Clear widget list before displaying new questions
        # Default result values
        self.total_question_points = 0
        self.user_points = 0
        self.user_good_answers = 0
        # Widget display
        self.displayQuestions(self.scrollable_widget_layout)
        self.addFinishQuizButton()

    def __initLayout(self) -> None:
        """Initialize main widget layout."""
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

    def __initScrollableWidget(self) -> None:
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

    def displayQuestions(self, scrollable_widget_layout: QVBoxLayout) -> None:
        """Display questions in scrollable widget."""
        for question in self.questions_list:
            question_widget = QuestionWidget(question)
            self.widget_list.append(question_widget)
            question_widget.label.setText( f"{len(self.widget_list)}. {question_widget.label.text()}") # Numbering questions
            scrollable_widget_layout.addWidget(question_widget)

    def calculateScore(self):
        """Calculate total points, user points and good answers."""
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
        result_widget = ResultWidget(
            len(self.widget_list), 
            self.total_question_points, 
            self.user_points, 
            self.user_good_answers
            )
        self.main_layout.addWidget(result_widget)
