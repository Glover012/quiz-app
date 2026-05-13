from PySide6.QtWidgets import QVBoxLayout, QWidget, QPushButton
from PySide6.QtCore import Qt, Signal, Slot


class StartButtonWidget(QWidget):
    """Start button widget that disables itself while questions load."""

    start_button_pressed = Signal()
    start_error_returned = Signal()

    def __init__(self) -> None:
        super().__init__()
        self._setup_layout()
        self._add_start_button()
        self._setup_button()

    def _setup_layout(self) -> None:
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

    def _add_start_button(self) -> None:
        self.start_button = QPushButton('Start')
        self.main_layout.addWidget(self.start_button, alignment=Qt.AlignmentFlag.AlignCenter)
    
    def _setup_button(self) -> None:
        self.start_button.setObjectName('startButton')
        self.start_button.clicked.connect(self._on_start_button_clicked)
        self.start_error_returned.connect(self.on_error_returned)

    @Slot()
    def _on_start_button_clicked(self) -> None:
        self.start_button.setEnabled(False)
        self.start_button_pressed.emit()

    @Slot()
    def on_error_returned(self) -> None:
        self.start_button.setEnabled(True)
