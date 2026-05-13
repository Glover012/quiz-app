from PySide6.QtWidgets import QVBoxLayout, QWidget
from PySide6.QtCore import Signal, Slot

from .components import AppNameWidget, StartButtonWidget, QuestionParamsWidget


class StartDisplay(QWidget):
    """Start screen containing the app title, start button and quiz parameter controls."""

    start_quiz_requested = Signal(dict)
    start_error_returned = Signal()

    def __init__(self) -> None:
        super().__init__()
        self._setup_layout()
        self._setup_widgets()
        self._add_widgets()

    def _setup_layout(self) -> None:
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

    def _setup_widgets(self) -> None:
        self.app_name = AppNameWidget()
        self.start_button = StartButtonWidget()
        # When start_button_pressed emit signal
        self.start_button.start_button_pressed.connect(self._start_quiz_requested)
        # When MainWindow emits error, pass signal to start_button
        self.start_error_returned.connect(self.start_button.start_error_returned.emit)
        self.question_params = QuestionParamsWidget()

    def _add_widgets(self) -> None:
        self.main_layout.addWidget(self.app_name)
        self.main_layout.addWidget(self.start_button)
        self.main_layout.addWidget(self.question_params)

    @Slot()
    def _start_quiz_requested(self) -> None:
        self.start_quiz_requested.emit(self.question_params.get_params())

