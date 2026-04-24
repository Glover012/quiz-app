from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..main_window import MainWindow

from PySide6.QtWidgets import QMenuBar
from .menus import QuizMenu, HelpMenu

class AppMenu(QMenuBar):
    """"Class that describes AppMenu for MainWindow."""
    def __init__(self, main_window: MainWindow):
        super().__init__()
        self.main_window = main_window
        self.__init_menus()

    def __init_menus(self):
        """Load all classes based on QMenu to AppMenu."""
        self.addMenu(QuizMenu(self.main_window))
        self.addMenu(HelpMenu(self.main_window))
