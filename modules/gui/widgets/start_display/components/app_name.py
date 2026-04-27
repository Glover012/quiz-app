from PySide6.QtWidgets import QVBoxLayout, QWidget, QLabel
from PySide6.QtCore import Qt


class AppName(QWidget):
    def __init__(self):
        super().__init__()
        self._setup_layout()
        self._display_app_name()

    def _setup_layout(self):
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

    def _display_app_name(self):
        app_name = QLabel('Quiz App')
        app_name.setObjectName('appName')
        self.main_layout.addWidget(app_name, alignment=Qt.AlignmentFlag.AlignCenter)