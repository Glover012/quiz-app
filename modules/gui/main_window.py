from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QFrame

from .widgets import WelcomeLabel
from .menu_bar import MenuBar


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._setup_window()
        self._setup_layout()
        self._set_menu_bar()
        self.display_widget(WelcomeLabel())

    def _setup_window(self):
        self.setWindowTitle('Quiz')
        self.resize(768, 512)

    def _setup_layout(self):
        self.main_layout = QVBoxLayout()
        central_widget = QWidget()
        central_widget.setLayout(self.main_layout)
        self.setCentralWidget(central_widget)

    def _set_menu_bar(self):
        self.setMenuBar(MenuBar(self))

    def display_widget(self, widget: QWidget | QFrame):
        """Display Widget in MainWindow."""
        if self._is_widget_type_displayed(widget):
            print('Widget is already displayed.')
        else:
            self._clear_window()
            self.main_layout.addWidget(widget)

    def _is_widget_type_displayed(self, widget: QWidget) -> bool:
        """Checks if widget type is already displayed in MainWindow."""
        if self.main_layout.count() == 0:
            return False
        current_item = self.main_layout.itemAt(0)
        current_widget = current_item.widget() if current_item is not None else None
        return type(current_widget) == type(widget)
        
    def _clear_window(self):
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