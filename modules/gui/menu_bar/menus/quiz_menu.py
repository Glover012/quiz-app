from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ...main_window import MainWindow

from PySide6.QtWidgets import QMainWindow, QMenu
from PySide6.QtGui import QAction
from ...widgets import StartQuiz

class QuizMenu(QMenu):
    def __init__(self, main_window: MainWindow):
        super().__init__()
        self.main_window = main_window
        self.__setFeatures()
        self.__initStartAction()
        self.__initExitAction()

    def __setFeatures(self):
        self.setTitle('Quiz')

    def __initStartAction(self):
        start_quiz = QAction('Start Quiz', self.main_window)
        start_quiz.setShortcut('Ctrl+N')
        start_quiz.triggered.connect(self.pressedStartQuiz)
        self.addAction(start_quiz)

    def __initExitAction(self):
        exit = QAction('Exit', self.main_window)
        exit.setShortcut('Ctrl+Q')
        exit.triggered.connect(self.pressedExit)
        self.addAction(exit)
    
    def pressedStartQuiz(self):
        print('pressedStartQuiz')
        self.main_window.displayWidget(StartQuiz(self.main_window))
    
    def pressedExit(self):
        print('Exit')
        self.main_window.close()
