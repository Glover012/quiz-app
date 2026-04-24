from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ...main_window import MainWindow

from PySide6.QtWidgets import QMenu, QMessageBox
from PySide6.QtGui import QAction

class HelpMenu(QMenu):
    def __init__(self, main_window: MainWindow):
        super().__init__()
        self.main_window = main_window
        self.__setFeatures()
        self.__initAboutAppAction()

    def __setFeatures(self):
        self.setTitle('Help')

    def __initAboutAppAction(self):
        about_app = QAction('About app', self.main_window)
        about_app.triggered.connect(self.pressedAboutApp)
        self.addAction(about_app)

    def pressedAboutApp(self):
        QMessageBox.about(self.main_window, 'About app', '''Simple Quiz App that utilise PySide6 GUI.''')
