import logging

from PySide6.QtWidgets import QVBoxLayout, QWidget
from PySide6.QtCore import Qt, Signal, Slot

from .components import AppNameWidget, StartButtonWidget, QuestionParamsWidget, QuestionParamsField, QuestionParams
from ....questions import NoQuestionsFoundError, NotEnoughQuestionsError

logger = logging.getLogger(__name__)


class StartDisplay(QWidget):
    """Start screen containing the app title, start button and quiz parameter controls."""

    start_quiz_requested = Signal(QuestionParams)
    start_error_returned = Signal(Exception)

    def __init__(self) -> None:
        super().__init__()
        self._setup_layout()
        self._setup_widgets()
        self._add_widgets()

    def _setup_layout(self) -> None:
        self._main_layout = QVBoxLayout()
        self.setLayout(self._main_layout)

    def _setup_widgets(self) -> None:
        self._app_name = AppNameWidget()
        self._start_button = StartButtonWidget()
        # When start_button_pressed emit signal
        self._start_button.start_button_pressed.connect(self._start_quiz_requested)
        # When MainWindow emits error
        self.start_error_returned.connect(self._on_start_error_returned)
        self._question_params = QuestionParamsWidget()

    def _on_start_error_returned(self, error: Exception) -> None:
        """Re-enable the start button and mark invalid quiz parameters."""
        logger.debug("Start display handling error: %s", type(error).__name__)
        self._start_button.on_error_returned()
        # Color error params for particular error types
        if isinstance(error, NoQuestionsFoundError):
            self._question_params.on_error_reset_combobox_to_default_values()
        elif isinstance(error, NotEnoughQuestionsError):
            self._question_params.on_error_reset_combobox_to_default_values(QuestionParamsField.AMOUNT)

    def _add_widgets(self) -> None:
        self._main_layout.addWidget(self._app_name, alignment=Qt.AlignmentFlag.AlignCenter)
        self._main_layout.addWidget(self._start_button, alignment=Qt.AlignmentFlag.AlignCenter)
        self._main_layout.addWidget(self._question_params, alignment=Qt.AlignmentFlag.AlignCenter)

    @Slot()
    def _start_quiz_requested(self) -> None:
        self.start_quiz_requested.emit(self._question_params.get_params())
