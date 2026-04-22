from PySide6.QtWidgets import QVBoxLayout, QWidget, QLabel, QRadioButton, QButtonGroup
from ...questions import Question

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