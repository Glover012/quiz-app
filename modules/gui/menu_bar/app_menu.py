from PySide6.QtWidgets import QMainWindow, QMenuBar
from .menus import QuizMenu, HelpMenu

class AppMenu(QMenuBar):
    """"Class that describes AppMenu for MainWindow."""
    def __init__(self, main_window : QMainWindow):
        super().__init__()
        self.main_window = main_window
        self.__init_menus()

    def __init_menus(self):
        """Load all classes based on QMenu to AppMenu."""
        self.addMenu(QuizMenu(self.main_window))
        self.addMenu(HelpMenu(self.main_window))
