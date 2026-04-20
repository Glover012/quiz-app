from PySide6.QtWidgets import QMainWindow, QMenu
from PySide6.QtGui import QAction

class QuizMenu(QMenu):
    def __init__(self, main_window : QMainWindow):
        super().__init__()
        self.main_window = main_window
        self.__setFeatures()
        self.__initActions()

    def __setFeatures(self):
        self.setTitle('Quiz')

    def __initActions(self):
        start_quiz = QAction('Start Quiz', self)
        start_quiz.setShortcut('Ctrl+N')
        start_quiz.triggered.connect(self.pressedStartQuiz)
        self.addAction(start_quiz)
    
    def pressedStartQuiz(self):
        print('Pressed New')
