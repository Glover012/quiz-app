from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt


class WelcomeLabel(QLabel):
    """Centered welcome label shown before a quiz starts."""

    def __init__(self) -> None:
        super().__init__()
        self.setText('Welcome to Quiz App!')
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setObjectName('welcomeLabel')
