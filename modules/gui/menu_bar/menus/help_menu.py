from PySide6.QtWidgets import QMainWindow, QMenu, QMessageBox
from PySide6.QtGui import QAction

class HelpMenu(QMenu):
    def __init__(self, main_window : QMainWindow):
        super().__init__()
        self.main_window = main_window
        self.__setFeatures()
        self.__initActions()

    def __setFeatures(self):
        self.setTitle('Help')

    def __initActions(self):
        about_app = QAction('About app', self)
        about_app.triggered.connect(self.pressedAboutApp)
        self.addAction(about_app)

    def pressedAboutApp(self):
        QMessageBox.about(self.main_window, 'About app', 'Simple Quiz App that utilise PySide6 GUI.')
