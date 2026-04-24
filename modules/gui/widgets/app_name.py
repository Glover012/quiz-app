from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel
from PySide6.QtCore import Qt

class AppName(QWidget):
    def __init__(self, main_window : QMainWindow):
        super().__init__()
        self.main_window = main_window
        self.__initLayout()
        self.displayAppName()

    def __initLayout(self):
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

    def displayAppName(self):
        app_name = QLabel('Quiz App')
        app_name.setObjectName('appName')
        self.main_layout.addWidget(app_name, alignment=Qt.AlignmentFlag.AlignCenter)