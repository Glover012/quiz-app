from PySide6.QtWidgets import QVBoxLayout, QWidget, QScrollArea, QPushButton
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
        style = ''''''
        self.finish_button = QPushButton('Finish')
        self.finish_button.clicked.connect(self.finishButtonClicked)
        self.main_layout.addWidget(self.finish_button)

    def finishButtonClicked(self):
        print('Clicked finish')
        self.displayResults()
        self.finish_button.deleteLater()

    def displayResults(self):
        print('Results')