import pytest
from pytest_mock import MockerFixture
from pytestqt.qtbot import QtBot

from PySide6.QtWidgets import QMainWindow

from modules.gui import MainWindow
from modules.gui.menu_bar import MenuActions
from modules.gui.widgets.overlays import ErrorOverlay
from modules.gui.widgets.start_display import StartDisplay
from modules.questions.models import Questions
from tests.data.api_response_test_data import QUESTION_TEST_DATA

@pytest.fixture
def main_window() -> MainWindow:
    """Standard MainWindow object."""
    main_window = MainWindow()
    return main_window

@pytest.fixture
def new_main_window() -> MainWindow:
    """
    MainWindow Object without pre-loaded overlays, 
    initial widget and menu-bar. Used for cleanup
    method testing.
    """
    new_main_window = MainWindow.__new__(MainWindow)
    # Run raw QMainWindow constructor on main_window object
    QMainWindow.__init__(new_main_window)

    new_main_window._setup_window()
    new_main_window._setup_layout()
    new_main_window._init_default_variables()
    return new_main_window

@pytest.fixture
def questions(mocker: MockerFixture) -> Questions:
    """
    Mock _get_question_data_from_api_client method on Questions class.
    Uses static and known QUESTION_TEST_DATA as api response and 
    forms question object with known data.
    """
    questions = Questions(10, "", "", "")
    mocker.patch.object(questions, "_get_question_data_from_api_client", return_value=QUESTION_TEST_DATA )
    questions.load()
    return questions

def test_handle_menu_actions(
        qtbot: QtBot, 
        mocker: MockerFixture, 
        main_window: MainWindow
        ) -> None:
    """
    Test _handle_menu_actions slot method, that handles 
    actions from MenuBar:
    - on SHOW_START_DISPLAY signal emitted calls
        _start_display_requested method
    - on EXIT_APP signal emitted calls self.close
    - on ABOUT_APP signal emitted shows about
        QMessageBox with proper app info
    """
    qtbot.addWidget(main_window)

    start_display_requested = mocker.spy(main_window, "_start_display_requested")
    main_window._handle_menu_actions(MenuActions.SHOW_START_DISPLAY)
    start_display_requested.assert_called_once_with()

    close = mocker.patch.object(main_window, "close")
    main_window._handle_menu_actions(MenuActions.EXIT_APP)
    close.assert_called_once_with()

    mock_about = mocker.patch("modules.gui.main_window.QMessageBox.about")
    main_window._handle_menu_actions(MenuActions.ABOUT_APP)
    mock_about.assert_called_once_with(
    main_window,
    "About app",
    "Simple quiz app built with PySide6.",
    )

def test_start_display_requested(
        qtbot: QtBot, 
        mocker: MockerFixture, 
        main_window: MainWindow
        ) -> None:
    """
    Test _start_display_requested slot method:
    - init start display
    - displays start_display
    """
    qtbot.addWidget(main_window)

    display_widget = mocker.patch.object(main_window, "_display_widget")

    main_window._start_display_requested()
    assert main_window._start_display is not None

    display_widget.assert_called_once_with(main_window._start_display)

def test_on_error(
        qtbot: QtBot, 
        mocker: MockerFixture, 
        main_window: MainWindow
        ) -> None:
    """
    Test _on_error slot method:
    - Emit start_error_returned signal
    - Calls _error_overlay.show_error with error
    """
    qtbot.addWidget(main_window)

    show_error = mocker.patch.object(main_window._error_overlay, "show_error")
    error = mocker.Mock()

    main_window._start_display_requested()

    with qtbot.waitSignal(main_window._start_display.start_error_returned, timeout=100):
        main_window._on_error(error)
        show_error.assert_called_once_with(error, for_seconds=5)

def test_on_error_close_requested(
        qtbot: QtBot, 
        mocker: MockerFixture, 
        main_window: MainWindow
        ) -> None:
    """
    Test _on_error slot method:
    - Do nothing and return when
        _close_requested is True
    """
    qtbot.addWidget(main_window)
    main_window._close_requested = True

    show_error = mocker.patch.object(main_window._error_overlay, "show_error")
    error = mocker.Mock()

    main_window._start_display_requested()

    with qtbot.assertNotEmitted(main_window._start_display.start_error_returned):
        main_window._on_error(error)
        show_error.assert_not_called()

def test_show_loading_screen(
        qtbot: QtBot, 
        mocker: MockerFixture, 
        main_window: MainWindow
        ) -> None:
    """
    Test _show_loading_screen slot method:
    - disable menu bar
    - calls _loading_overlay.show_loading
    """
    qtbot.addWidget(main_window)

    show_loading = mocker.patch.object(main_window._loading_overlay, "show_loading")

    main_window._show_loading_screen()
    assert main_window._menu_bar.isEnabled() is False

    show_loading.assert_called_once_with()

def test_hide_loading_screen(
        qtbot: QtBot, 
        mocker: MockerFixture, 
        main_window: MainWindow
        ) -> None:
    """
    Test _hide_loading_screen slot method:
    - enable menu bar
    - calls _loading_overlay.hide_loading
    """
    qtbot.addWidget(main_window)

    hide_loading = mocker.patch.object(main_window._loading_overlay, "hide_loading")

    main_window._hide_loading_screen()
    assert main_window._menu_bar.isEnabled() is True

    hide_loading.assert_called_once_with()

def test_on_thread_finished(
        qtbot: QtBot, 
        mocker: MockerFixture, 
        main_window: MainWindow
        ) -> None:
    """
    Test _on_thread_finished slot method:
    - remove reference from:
        _question_loader
        _thread_controller
    - if _close_requested is True:
        calls close method
    """
    qtbot.addWidget(main_window)
    main_window._question_loader = mocker.Mock()
    main_window._thread_controller = mocker.Mock()

    assert main_window._question_loader is not None
    assert main_window._thread_controller is not None

    close = mocker.patch.object(main_window, "close")
    main_window._close_requested = True

    main_window._on_thread_finished()

    assert main_window._question_loader is None
    assert main_window._thread_controller is None

    close.assert_called_once_with()

def test_on_questions_loaded(
        qtbot: QtBot, 
        mocker: MockerFixture, 
        main_window: MainWindow,
        questions: Questions,
        ) -> None:
    """
    Test _on_questions_loaded slot method:
    - init _question_display
    - _display_widget method called with _question_display
    - on repeat_button_clicked signal emitted
    calls _start_display_requested method
    """
    qtbot.addWidget(main_window)

    display_widget = mocker.patch.object(main_window, "_display_widget")
    start_display_requested = mocker.patch.object(main_window, "_start_display_requested")

    main_window._on_questions_loaded(questions)

    question_display = main_window._question_display
    assert question_display is not None

    display_widget.assert_called_once_with(question_display)

    question_display.repeat_button_clicked.emit()
    start_display_requested.assert_called_once_with()

def test_on_questions_loaded_close_requested(
        qtbot: QtBot, 
        mocker: MockerFixture, 
        main_window: MainWindow,
        questions: Questions,
        ) -> None:
    """
    Test _on_questions_loaded slot method 
    when _close_requested is True:
    - Not call _display_widget method
    """
    qtbot.addWidget(main_window)
    main_window._close_requested = True

    display_widget = mocker.patch.object(main_window, "_display_widget")

    main_window._on_questions_loaded(questions)

    display_widget.assert_not_called()

def test_add_overlay(
        qtbot: QtBot, 
        mocker: MockerFixture, 
        main_window: MainWindow,
        ) -> None:
    """
    Test _add_overlay method:
    - Add overlay to ignored widgets:
    - Hide overlay
    - Add widget
    """
    qtbot.addWidget(main_window)

    add_widget = mocker.patch.object(main_window._main_layout, "addWidget")
    mock_overlay = mocker.Mock()
    hide = mocker.patch.object(mock_overlay, "hide")

    main_window._add_overlay(mock_overlay)

    assert mock_overlay in main_window._ignored
    add_widget.assert_called_once_with(mock_overlay)
    hide.assert_called_once_with()

def test_hide_overlays(
        qtbot: QtBot, 
        mocker: MockerFixture, 
        main_window: MainWindow,
        ) -> None:
    """
    Test _hide_overlays method:
    - calls hide on error_overlay
    - calls hide_loading on loading_overlay 
    """
    qtbot.addWidget(main_window)

    hide_loading = mocker.patch.object(main_window._loading_overlay, "hide_loading")
    hide_error = mocker.patch.object(main_window._error_overlay, "hide")

    main_window._hide_overlays()

    hide_loading.assert_called_once_with()
    hide_error.assert_called_once_with()

def test_clear_window(
        qtbot: QtBot, 
        new_main_window: MainWindow,
        ) -> None:
    """
    Test _clear_window cleanup method:
    - ignore widgets in _ignored from 
    cleanup
    - delete all widgets
    """
    qtbot.addWidget(new_main_window)    
    ignored = new_main_window._ignored

    error_overlay = ErrorOverlay()
    start_display = StartDisplay()

    # layout.count() returns the current count
    # Re-read layout.count() after each widget add/remove.
    assert new_main_window._main_layout.count() == 0

    new_main_window._add_overlay(error_overlay)
    new_main_window._main_layout.addWidget(start_display)
    assert new_main_window._main_layout.count() == 2

    new_main_window._clear_window()

    assert new_main_window._main_layout.count() == 1
    assert error_overlay in ignored

def test_display_widget(
        qtbot: QtBot, 
        mocker: MockerFixture, 
        main_window: MainWindow,
        ) -> None:
    """
    Test _display_widget method:
    - calls _clear_window
    - add widget
    - set widget as current
    - calls _hide_overlays
    """
    qtbot.addWidget(main_window)

    clear_window = mocker.patch.object(main_window, "_clear_window")
    hide_overlays = mocker.patch.object(main_window, "_hide_overlays")

    mock_widget = mocker.Mock()
    add_widget = mocker.patch.object(main_window._main_layout, "addWidget")
    set_current_widget = mocker.patch.object(main_window._main_layout, "setCurrentWidget")

    main_window._display_widget(mock_widget)

    clear_window.assert_called_once_with()

    add_widget.assert_called_once_with(mock_widget)
    set_current_widget.assert_called_once_with(mock_widget)

    hide_overlays.assert_called_once_with()
