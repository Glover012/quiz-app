from PySide6.QtWidgets import QMenuBar
from PySide6.QtCore import Signal

from .menus import QuizMenu, HelpMenu


class MenuBar(QMenuBar):
    """Class that describes MenuBar for MainWindow."""

    action_requested = Signal(object)

    def __init__(self) -> None:
        super().__init__()
        self._add_quiz_menu()
        self._add_help_menu()

    def _add_quiz_menu(self) -> None:
        self.quiz_menu = QuizMenu()
        self.quiz_menu.action_requested.connect(self.action_requested.emit)
        self.addMenu(self.quiz_menu)

    def _add_help_menu(self) -> None:
        self.help_menu = HelpMenu()
        self.help_menu.action_requested.connect(self.action_requested.emit)
        self.addMenu(self.help_menu)
