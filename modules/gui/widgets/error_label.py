from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt, QTimer, QThread

from ...questions import OpenTriviaClientError
from ..workers import QuestionLoader, WorkerThreadControllerError


class ErrorLabel(QLabel):
    """Error label."""
    
    def __init__(self, parent, error: OpenTriviaClientError | WorkerThreadControllerError) -> None:
        super().__init__(parent)
        self.error = error
        self._setup_label()

    def _setup_label(self) -> None:
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setObjectName('errorLabel')
        self.setWordWrap(True)

    def show_error(self) -> None:
        if isinstance(self.error, OpenTriviaClientError):
            self.setText(f'API Error - {self.error}')
        elif isinstance(self.error, WorkerThreadControllerError):
            self.setText(f'Thread Error - {self.error}')
        self.show()
        timer = QTimer.singleShot(5000, self.deleteLater)
