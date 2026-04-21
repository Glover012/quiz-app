from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel, QRadioButton, QScrollArea, QButtonGroup
from PySide6.QtCore import Qt
from ...questions import Question

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

class QuestionWidget(QWidget):
    question_style = ''

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
        self.label = QLabel(self.question.question)
        self.main_layout.addWidget(self.label)

    def questionAnswersRadioButtons(self):
        index = ['a', 'b', 'c', 'd']
        self.a_button_group = QButtonGroup()
        for i, answer in enumerate(self.question.all_answers):
            button = QRadioButton(f'{f'{index[i]}. ' if self.question.tp == "multiple" else ""}{answer}')
            self.a_button_group.addButton(button)
            self.main_layout.addWidget(button)
        self.a_button_group.buttonClicked.connect(self.onButtonClicked)

    def onButtonClicked(self, button):
        self.user_answer = button.text()
        if self.question.correct_answer in self.user_answer:
            print('Correct')
        else:
            print('Incorrect')