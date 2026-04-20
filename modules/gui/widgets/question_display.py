from PySide6.QtWidgets import QVBoxLayout, QWidget, QLabel, QRadioButton, QScrollArea
from PySide6.QtCore import Qt

class QuestionDisplay(QWidget):
    """Widget to display questions."""
    def __init__(self):
        super().__init__()
        self.initUI()
        self.printQuestions()

    def initUI(self):
        self.main_layout = QVBoxLayout(self)

        self.question_layout = QVBoxLayout()
        self.question_widget = QWidget()
        self.question_widget.setLayout(self.question_layout)
        self.main_layout.addWidget(self.question_widget)

        scroll = QScrollArea()
        scroll.setWidget(self.question_widget)
        scroll.setWidgetResizable(True)
        self.main_layout.addWidget(scroll)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def printQuestions(self):
        for q in range(1, 30):
            question = QLabel(f'{q}. To jest testowe pytanie?')
            self.question_layout.addWidget(question)
            for i, a in enumerate(['a', 'b', 'c', 'd']):
                answer = QRadioButton(f'{a}. Odpowiedź {i}')
                self.question_layout.addWidget(answer)
