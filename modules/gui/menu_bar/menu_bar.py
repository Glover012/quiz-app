from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtWidgets import QMenuBar

if TYPE_CHECKING:
    from ..main_window import MainWindow

from .menus import QuizMenu, HelpMenu


class MenuBar(QMenuBar):
    """Class that describes MenuBar for MainWindow."""
    def __init__(self, main_window: MainWindow):
        super().__init__()
        self.main_window = main_window
        self._add_menus()

    def _add_menus(self):
        """Load menus to MenuBar."""
        self.addMenu(QuizMenu(self.main_window))
        self.addMenu(HelpMenu(self.main_window))
