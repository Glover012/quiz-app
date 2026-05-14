from PySide6.QtWidgets import QVBoxLayout, QWidget
from PySide6.QtCore import Signal, Slot

from .components import AppNameWidget, StartButtonWidget, QuestionParamsWidget, QuestionParamsField
from ....questions import NoQuestionsFoundError, NotEnoughQuestionsError


class StartDisplay(QWidget):
    """Start screen containing the app title, start button and quiz parameter controls."""

    start_quiz_requested = Signal(dict)
    start_error_returned = Signal(Exception)

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
        # When MainWindow emits error
        self.start_error_returned.connect(self._on_start_error_returned)
        self.question_params = QuestionParamsWidget()

    def _on_start_error_returned(self, error: Exception) -> None:
        """Re-enable the start button and mark invalid quiz parameters."""
        self.start_button.on_error_returned()
        # Color error params for particular error types
        if isinstance(error, NoQuestionsFoundError):
            self.question_params.on_error_reset_combobox_to_default_values()
        elif isinstance(error, NotEnoughQuestionsError):
            self.question_params.on_error_reset_combobox_to_default_values(QuestionParamsField.AMOUNT)

    def _add_widgets(self) -> None:
        self.main_layout.addWidget(self.app_name)
        self.main_layout.addWidget(self.start_button)
        self.main_layout.addWidget(self.question_params)

    @Slot()
    def _start_quiz_requested(self) -> None:
        self.start_quiz_requested.emit(self.question_params.get_params())

