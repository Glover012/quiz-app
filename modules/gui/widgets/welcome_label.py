from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt

class WelcomeLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.setText('Welcome to Quiz!')
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet('''
                           font-size: 40px;
                           font-weight: bold;
                           font-family: Arial;
                           border-radius: 10px;
                           ''')



