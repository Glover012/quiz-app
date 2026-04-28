from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtWidgets import QMenu
from PySide6.QtGui import QAction

from ...widgets import StartDisplay

if TYPE_CHECKING:
    from ...main_window import MainWindow


class QuizMenu(QMenu):
    def __init__(self, main_window: MainWindow) -> None:
        super().__init__()
        self.main_window = main_window
        self._setup_menu()
        self._add_start_quiz_action()
        self._add_exit_action()

    def _setup_menu(self) -> None:
        self.setTitle('Quiz')

    def _add_start_quiz_action(self) -> None:
        start_quiz = QAction('Start Quiz', self.main_window)
        start_quiz.setShortcut('Ctrl+N')
        start_quiz.triggered.connect(self._on_start_quiz_action_triggered)
        self.addAction(start_quiz)

    def _add_exit_action(self) -> None:
        exit = QAction('Exit', self.main_window)
        exit.setShortcut('Ctrl+Q')
        exit.triggered.connect(self._on_exit_action_triggered)
        self.addAction(exit)
    
    def _on_start_quiz_action_triggered(self) -> None:
        print('pressedStartQuiz')
        self.main_window.display_widget(StartDisplay(self.main_window))
    
    def _on_exit_action_triggered(self) -> None:
        print('Exit')
        self.main_window.close()
