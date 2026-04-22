from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from .question_params import QuestionParams
from .app_name import AppName

class StartQuiz(QWidget):
    def __init__(self, main_window : QMainWindow):
        super().__init__()
        self.main_window = main_window
        self.__initLayout()
        self.displayWidgets()

    def __initLayout(self):
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

    def displayWidgets(self):
        self.main_layout.addWidget(AppName(self.main_window))
        self.main_layout.addWidget(QuestionParams(self.main_window))
