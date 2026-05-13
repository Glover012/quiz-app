import logging

from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QFrame, QMessageBox
from PySide6.QtCore import Slot

from .widgets import WelcomeLabel, ErrorLabel, StartDisplay, QuestionDisplay, QuestionParams
from .menu_bar import MenuBar, MenuActions
from .workers import QuestionLoader, WorkerThreadController, WorkerThreadControllerError
from ..questions import OpenTriviaClientError, Questions

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """
    MainWindow is a central application point. Responsible for application 
    control, navigation, question loading, and quiz display.
    """

    def __init__(self) -> None:
        super().__init__()
        self._setup_window()
        self._setup_layout()
        self._set_menu_bar()
        self._display_widget(WelcomeLabel())

    def _setup_window(self) -> None:
        self.setWindowTitle('Quiz')
        self.resize(768, 512)

    def _setup_layout(self) -> None:
        self.main_layout = QVBoxLayout()
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

    def _set_menu_bar(self) -> None:
        self.menu_bar = MenuBar()
        # Connects Signals from MenuBar
        self.menu_bar.action_requested.connect(self._handle_menu_actions) 
        self.setMenuBar(self.menu_bar)

    @Slot(object)
    def _handle_menu_actions(self, action: MenuActions) -> None:
        match action:
            case MenuActions.SHOW_START_DISPLAY:
                self._start_display_requested()
            case MenuActions.EXIT_APP:
                self.close()
            case MenuActions.ABOUT_APP:
                QMessageBox.about(self, 'About app', '''Simple Quiz App that utilise PySide6 GUI.''')

    @Slot()
    def _start_display_requested(self) -> None:
        self.start_display = StartDisplay()
        # Connect start_quiz_requested signal from start_display
        self.start_display.start_quiz_requested.connect(self._load_questions)
        self._display_widget(self.start_display)

    @Slot(object)
    def _on_error(self, error: OpenTriviaClientError | WorkerThreadControllerError) -> None:
        self.start_display.start_error_returned.emit()
        self._display_error(error)

    def _display_error(self, error: OpenTriviaClientError | WorkerThreadControllerError) -> None:
        """Show a temporary floating error message over the main window."""
        self.error_label = ErrorLabel(self.central_widget, error)
        self.error_label.setGeometry(20, 20, self.central_widget.width() - 40, 50)
        self.error_label.show_error()
        self.error_label.raise_()

    @Slot()
    def _display_loading_screen(self) -> None:
        pass

    @Slot()
    def _hide_loading_screen(self) -> None:
        pass

    @Slot(dict)
    def _load_questions(self, question_params: QuestionParams) -> None:
        """Start a background worker that loads quiz questions. Use WorkerThreadController."""
        # Connect worker signals before starting the thread
        try:
            # Connect worker error signal
            self.question_loader = QuestionLoader(question_params)
            self.question_loader.error.connect(self._on_error)
            self.question_loader.loaded.connect(self._on_questions_loaded)
            self.thread_controller = WorkerThreadController(self.question_loader)
            # Connect thread controller error signal
            self.thread_controller.thread_error.connect(self._on_error)
            # Connect loading screen signals
            self.thread_controller.thread_started.connect(self._display_loading_screen)
            self.thread_controller.thread_finished.connect(self._hide_loading_screen)
            # Start thread
            self.thread_controller.run_thread()
        except (OpenTriviaClientError, WorkerThreadControllerError) as error:
            self._on_error(error)

    @Slot(Questions)
    def _on_questions_loaded(self, questions: Questions) -> None:
        """Display questions in QuestionDisplay."""
        self.question_display = QuestionDisplay(questions.questions_list)
        self.question_display.repeat_button_clicked.connect(self._start_display_requested)
        self._display_widget(self.question_display)
        logger.debug("Questions loaded successfully. Number of questions: %s", len(questions.questions_list))

    def _display_widget(self, widget: QWidget | QFrame) -> None:
        """Display external Widget in MainWindow."""
        if self._is_widget_type_displayed(widget):
            logger.debug("Widget is already displayed: %s", type(widget).__name__)
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
        
    def _clear_window(self) -> None:
        """Delete all widgets from MainWindow."""
        widget_count = self.main_layout.count()
        if widget_count:
            for i in reversed(range(self.main_layout.count())):
                item = self.main_layout.itemAt(i)
                widget = item.widget() if item is not None else None
                if widget is not None:
                    self.main_layout.removeWidget(widget)
                    widget.deleteLater()
        logger.debug("Deleted widget count: %s", widget_count)
