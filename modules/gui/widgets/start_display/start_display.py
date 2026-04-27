from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtWidgets import QVBoxLayout, QWidget

from .components import QuestionParams, AppName

if TYPE_CHECKING:
    from ...main_window import MainWindow


class StartDisplay(QWidget):
    def __init__(self, main_window: MainWindow):
        super().__init__()
        self.main_window = main_window
        self._setup_layout()
        self._add_widgets()

    def _setup_layout(self):
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

    def _add_widgets(self):
        self.main_layout.addWidget(AppName())
        self.main_layout.addWidget(QuestionParams(self.main_window))
