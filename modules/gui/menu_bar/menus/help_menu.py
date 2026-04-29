from __future__ import annotations

import logging

from typing import TYPE_CHECKING

from PySide6.QtWidgets import QMenu, QMessageBox
from PySide6.QtGui import QAction

if TYPE_CHECKING:
    from ...main_window import MainWindow

logger = logging.getLogger(__name__)

class HelpMenu(QMenu):
    def __init__(self, main_window: MainWindow) -> None:
        super().__init__()
        self.main_window = main_window
        self._setup_menu()
        self._add_action_about_app()

    def _setup_menu(self) -> None:
        self.setTitle('Help')

    def _add_action_about_app(self) -> None:
        about_app = QAction('About app', self.main_window)
        about_app.triggered.connect(self._on_about_app_action_triggered)
        self.addAction(about_app)

    def _on_about_app_action_triggered(self) -> None:
        logger.debug("About app action triggered.")
        QMessageBox.about(self.main_window, 'About app', '''Simple Quiz App that utilise PySide6 GUI.''')
