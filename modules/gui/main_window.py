from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from .widgets import WelcomeLabel
from .menu_bar import AppMenu

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__setWindowFeatures()
        self.__initLayout()
        self.__initAppMenu()
        self.displayWidget(WelcomeLabel())

    def __setWindowFeatures(self):
        """Set MainWindow features."""
        self.setWindowTitle('Quiz')
        self.resize(768, 512)

    def __initLayout(self):
        """Set MainWindow layout."""
        self.main_layout = QVBoxLayout()
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

    def __initAppMenu(self):
        self.setMenuBar(AppMenu(self))

    def displayWidget(self, widget : QWidget):
        """Display Widget in MainWindow."""
        self.clear()
        self.main_layout.addWidget(widget)

    def clear(self):
        """Delete all widgets from MainWindow."""
        widget_count = self.main_layout.count()
        if widget_count:
            for i in reversed(range(self.main_layout.count())):
                item = self.main_layout.itemAt(i)
                widget = item.widget() if item is not None else None
                if widget is not None:
                    self.main_layout.removeWidget(widget)
                    widget.deleteLater()
        print(f'{'Deleted ' if widget_count else ''}Widget Number: {widget_count}')