from PySide6.QtWidgets import QVBoxLayout, QWidget, QLabel
from PySide6.QtCore import Qt


class AppNameWidget(QWidget):
    """Widget that displays the application name."""

    def __init__(self) -> None:
        super().__init__()
        self._setup_layout()
        self._display_app_name()

    def _setup_layout(self) -> None:
        self._main_layout = QVBoxLayout()
        self._main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self._main_layout)

    def _display_app_name(self) -> None:
        app_name = QLabel('Quiz App')
        app_name.setObjectName('appName')
        self._main_layout.addWidget(app_name)
        
