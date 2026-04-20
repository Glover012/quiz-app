from PySide6.QtWidgets import QVBoxLayout, QGridLayout, QWidget, QLabel,QPushButton
from PySide6.QtCore import Qt

class StartQuiz(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        quizWidget = QWidget(self)
        quizWidgetVBoxLayout = QVBoxLayout()
        quizWidget.setLayout(quizWidgetVBoxLayout)
        
        quizLabel = QLabel('Quiz') # border: 2px solid #3498db;
        quizLabel.setStyleSheet('''
                                font-size: 40px;
                                font-weight: bold;
                                font-family: Arial;
                                border-radius: 10px;
                                ''')
        quizWidgetVBoxLayout.addWidget(quizLabel, alignment=Qt.AlignmentFlag.AlignCenter)

        self.startButton = QPushButton('Start')
        self.startButton.setStyleSheet('''
                                  font-size: 30px;
                                  font-family: Arial;
                                  ''')
        quizWidgetVBoxLayout.addWidget(self.startButton, alignment=Qt.AlignmentFlag.AlignCenter)

        # Question Parameters Widget
        questionParamsWidget = QWidget(self)
        questionParamsGridLayout = QGridLayout()
        questionParamsWidget.setLayout(questionParamsGridLayout)

        questionAmount = QLabel('Ilość')
        questionDifficulty = QLabel('Trudność')
        questionCategory = QLabel('Kategoria')
        questionType = QLabel('Typ')

        questionParamsGridLayout.addWidget(questionAmount, 0, 0)
        questionParamsGridLayout.addWidget(questionDifficulty, 0, 1)
        questionParamsGridLayout.addWidget(questionCategory, 0, 2)
        questionParamsGridLayout.addWidget(questionType, 0, 3)

        # StartQuiz
        layout.addWidget(quizWidget)
        layout.addWidget(questionParamsWidget)

    def label(self, text: str):
        label = QLabel(text)
        label.setStyleSheet('''
                            font-size: 20px;
                            ''')
