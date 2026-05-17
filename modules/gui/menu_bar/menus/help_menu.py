import logging

from PySide6.QtWidgets import QMenu
from PySide6.QtGui import QAction
from PySide6.QtCore import Signal, Slot

from ..menu_actions import MenuActions

logger = logging.getLogger(__name__)


class HelpMenu(QMenu):
    """Help menu that emits action requests for help commands."""

    action_requested = Signal(object)

    def __init__(self) -> None:
        super().__init__()
        self._setup_menu()
        self._add_action_about_app()

    def _setup_menu(self) -> None:
        self.setTitle('Help')

    def _add_action_about_app(self) -> None:
        about_app = QAction('About app', self)
        about_app.triggered.connect(self._on_about_app_action_triggered)
        self.addAction(about_app)

    @Slot()
    def _on_about_app_action_triggered(self) -> None:
        self.action_requested.emit(MenuActions.ABOUT_APP)
        logger.debug("About app action triggered.")
