import logging

from PySide6.QtWidgets import QMenu
from PySide6.QtGui import QAction
from PySide6.QtCore import Signal, Slot

from ..menu_actions_signals import MenuActionsSignals

logger = logging.getLogger(__name__)


class QuizMenu(QMenu):
    """Quiz Menu in MenuBar."""

    action_requested = Signal(object)

    def __init__(self) -> None:
        super().__init__()
        self._setup_menu()
        self._add_start_quiz_action()
        self._add_exit_action()

    def _setup_menu(self) -> None:
        self.setTitle('Quiz')

    def _add_start_quiz_action(self) -> None:
        start_quiz = QAction('Start Quiz', self)
        start_quiz.setShortcut('Ctrl+N')
        start_quiz.triggered.connect(self._on_start_quiz_action_triggered)
        self.addAction(start_quiz)

    @Slot()
    def _on_start_quiz_action_triggered(self) -> None:
        self.action_requested.emit(MenuActionsSignals.SHOW_START_DISPLAY)
        logger.debug("Start quiz action triggered.")

    def _add_exit_action(self) -> None:
        exit = QAction('Exit', self)
        exit.setShortcut('Ctrl+Q')
        exit.triggered.connect(self._on_exit_action_triggered)
        self.addAction(exit)
    
    @Slot()
    def _on_exit_action_triggered(self) -> None:
        self.action_requested.emit(MenuActionsSignals.EXIT_APP)
        logger.info("Exit action triggered.")
