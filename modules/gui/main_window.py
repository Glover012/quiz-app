import logging

from PySide6.QtWidgets import QMainWindow, QWidget, QFrame, QMessageBox, QStackedLayout
from PySide6.QtCore import Slot

from .widgets import WelcomeLabel, StartDisplay, QuestionDisplay, QuestionParams, LoadingOverlay, ErrorOverlay
from .menu_bar import MenuBar, MenuActions
from .workers import QuestionLoader, WorkerThreadController
from ..questions import Questions

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """
    Main application window and top-level GUI coordinator.

    MainWindow owns the central stacked layout, menu bar, loading/error overlays,
    and the question-loading worker controller. It coordinates navigation between
    the welcome screen, start screen, and question display.

    Question loading is delegated to a worker thread. The OpenTDB request timeout
    is configured in OpenTriviaClient.
    """

    def __init__(self) -> None:
        super().__init__()
        self._setup_window()
        self._setup_layout()
        self._init_default_variables()
        self._setup_menu_bar()
        self._setup_error_overlay()
        self._setup_loading_overlay()
        self._setup_initial_widget()

    def _setup_window(self) -> None:
        self.setObjectName("mainWindow")
        self.setWindowTitle('Quiz')
        self.resize(896, 512)

    def _setup_layout(self) -> None:
        self.main_layout = QStackedLayout()
        self.main_layout.setStackingMode(QStackedLayout.StackingMode.StackAll)
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)
    
    def _init_default_variables(self) -> None:
        # List of ignored widgets, from MainWindow clean method
        # Used for overlays
        self.ignored = []
        self._close_requested = False
        self.thread_controller = None
        self.question_loader = None

    def _setup_menu_bar(self) -> None:
        self.menu_bar = MenuBar()
        # Connects Signals from MenuBar to _handle method
        self.menu_bar.action_requested.connect(self._handle_menu_actions) 
        self.setMenuBar(self.menu_bar)

    def _setup_error_overlay(self):
        self.error_overlay = ErrorOverlay()
        self._add_overlay(self.error_overlay)

    def _setup_loading_overlay(self):
        self.loading_overlay = LoadingOverlay()
        self._add_overlay(self.loading_overlay)

    def _setup_initial_widget(self):
        self._display_widget(WelcomeLabel())

    @Slot(object)
    def _handle_menu_actions(self, action: MenuActions) -> None:
        match action:
            case MenuActions.SHOW_START_DISPLAY:
                self._start_display_requested()
            case MenuActions.EXIT_APP:
                self.close()
            case MenuActions.ABOUT_APP:
                QMessageBox.about(self, 'About app', '''Simple quiz app built with PySide6.''')

    @Slot()
    def _start_display_requested(self) -> None:
        logger.debug("Displaying start display.")
        self.start_display = StartDisplay()
        # Connect start_quiz_requested signal to _load_questions method
        self.start_display.start_quiz_requested.connect(self._load_questions)
        self._display_widget(self.start_display)

    @Slot(object)
    def _on_error(self, error: Exception) -> None:
        if self._close_requested:
            logger.debug("Ignoring error callback because close was requested.")
            return # Do nothing if _close_requested

        logger.warning("Displaying loading error: %s: %s", type(error).__name__, error)
        self.start_display.start_error_returned.emit(error)
        self.error_overlay.show_error(error, for_seconds=5)

    @Slot(dict)
    def _load_questions(self, question_params: QuestionParams) -> None:
        """Start a background worker that loads quiz questions. Use WorkerThreadController."""
        logger.info("Question loading requested with params: %s", question_params)
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
            self.thread_controller.thread_started.connect(self._show_loading_screen)
            self.thread_controller.thread_finished.connect(self._hide_loading_screen)
            self.thread_controller.thread_finished.connect(self._on_thread_finished)
            # Start thread
            self.thread_controller.run_thread()
        except Exception:
            logger.exception("Failed to start question loading.")
            self._on_error(RuntimeError("Unexpected application error. Please try again."))

    @Slot()
    def _show_loading_screen(self) -> None:
        """Display loading screen overlay. Disable menu_bar control."""
        self.menu_bar.setEnabled(False)
        self.loading_overlay.show_loading()

    @Slot()
    def _hide_loading_screen(self) -> None:
        """Hide loading screen overlay. Enable menu_bar control."""
        self.menu_bar.setEnabled(True)
        self.loading_overlay.hide_loading()

    @Slot()
    def _on_thread_finished(self):
        """
        Remove reference from thread_controller and question_loader. 
        Close app if _close_requested.
        """
        logger.debug("Question loading thread finished. close_requested=%s", self._close_requested)
        self.question_loader = None
        self.thread_controller = None

        if self._close_requested:
            self.close()

    @Slot(Questions)
    def _on_questions_loaded(self, questions: Questions) -> None:
        """Display questions in QuestionDisplay."""
        if self._close_requested:
            logger.debug("Ignoring loaded questions callback because close was requested.")
            return # Do nothing if _close_requested
        
        self.question_display = QuestionDisplay(questions.questions_list)
        self.question_display.repeat_button_clicked.connect(self._start_display_requested)
        self._display_widget(self.question_display)
        logger.debug("Questions loaded successfully. Number of questions: %s", len(questions.questions_list))

    def _add_overlay(self, overlay: ErrorOverlay | LoadingOverlay) -> None:
        """
        Method used to add overlay widgets. Automatically hide overlay.
        Widgets added by this method are ignored by MainWindow cleanup methods.
        """
        self.ignored.append(overlay)
        overlay.hide()
        self.main_layout.addWidget(overlay)

    def _hide_overlays(self) -> None:
        """
        Used when displaying new widgets. Due to QStackedLayout.StackingMode.StackAll
        some, previously hidden, widgets may be visible again.
        """
        self.loading_overlay.hide_loading()
        self.error_overlay.hide()

    def _display_widget(self, widget: QWidget | QFrame) -> None:
        """Display external Widget in MainWindow."""
        self._clear_window()
        self.main_layout.addWidget(widget)
        self.main_layout.setCurrentWidget(widget)
        self._hide_overlays()

    def _clear_window(self) -> None:
        """Delete all widgets from MainWindow."""
        deleted_widgets = 0
        widget_count = self.main_layout.count()
        if widget_count:
            for i in reversed(range(widget_count)):
                item = self.main_layout.itemAt(i)
                widget = item.widget() if item is not None else None
                if widget is not None and widget not in self.ignored:
                    self.main_layout.removeWidget(widget)
                    widget.deleteLater()
                    deleted_widgets +=1
        logger.debug("Deleted widget count: %s", deleted_widgets)

    def closeEvent(self, event):
        """
        Replaces MainWindow closeEvent. Function set _close_requested flag True.

        Delay closing while the question loader thread is still running.

        The first close request asks the thread to stop and ignores the event.
        When the thread emits finished, _on_thread_finished calls close() again.
        The second close request is accepted because the thread is no longer running.
        """
        if self.thread_controller is not None and self.thread_controller.is_running():
            logger.info("Close requested while question loader is running. Waiting for thread cleanup.")
            self._close_requested = True
            self.thread_controller.stop()
            # Cancel close event, it is required due to thread cleanup
            event.ignore() 
            return
        logger.debug("Close accepted. No running question loader thread.")
        super().closeEvent(event) # Use closeEvent from QMainWindow to close event=MainWindow
