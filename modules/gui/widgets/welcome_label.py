from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt


class WelcomeLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.setText('Welcome to Quiz App!')
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setObjectName('welcomeLabel')
