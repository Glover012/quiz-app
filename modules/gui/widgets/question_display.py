from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel, QRadioButton, QScrollArea
from PySide6.QtCore import Qt
from ...questions import Question

class QuestionDisplay(QWidget):
    """Widget to display questions."""
    def __init__(self, questionsList):
        super().__init__()
        self.questionsList = questionsList
        self.__initLayout()
        self.__initScrollWidget()
        self.displayQuestions(self.scrollable_widget_layout)

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
            scrollable_widget_layout.addWidget(QuestionWidget(question))

class QuestionWidget(QWidget):
    question_style = ''
    question_number = 1

    def __init__(self, question : Question):
        super().__init__()
        self.question = question
        self.__initLayout()
        self.questionLabel()
        self.questionAnswersRadioButtons()

    def __initLayout(self):
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

    def questionLabel(self):
        label = QLabel(f'{self.question_number}. {self.question.question}')
        self.main_layout.addWidget(label)
        self.question_number += 1 # For iterating questions

    def questionAnswersRadioButtons(self):
        if self.question.tp == 'multiple':
            index = ['a', 'b', 'c', 'd']
            for i, answer in enumerate(self.question.all_answers):
                a_button = QRadioButton(f'{index[i]}. {answer}')
                self.main_layout.addWidget(a_button)
        elif self.question.tp == 'boolean':
            for answer in self.question.all_answers:
                a_button = QRadioButton(answer)
                self.main_layout.addWidget(a_button)
