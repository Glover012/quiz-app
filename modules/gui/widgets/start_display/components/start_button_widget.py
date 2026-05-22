from PySide6.QtWidgets import QVBoxLayout, QWidget, QPushButton
from PySide6.QtCore import Qt, Signal, Slot


class StartButtonWidget(QWidget):
    """Start button widget that disables itself while questions load."""

    start_button_pressed = Signal()

    def __init__(self) -> None:
        super().__init__()
        self._setup_layout()
        self._add_start_button()
        self._setup_button()

    def _setup_layout(self) -> None:
        self._main_layout = QVBoxLayout()
        self._main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self._main_layout)

    def _add_start_button(self) -> None:
        self._start_button = QPushButton('Start')
        self._main_layout.addWidget(self._start_button)
    
    def _setup_button(self) -> None:
        self._start_button.setObjectName('startButton')
        self._start_button.clicked.connect(self._on_start_button_clicked)

    @Slot()
    def _on_start_button_clicked(self) -> None:
        self._start_button.setEnabled(False)
        self.start_button_pressed.emit()

    @Slot()
    def on_error_returned(self) -> None:
        self._start_button.setEnabled(True)
