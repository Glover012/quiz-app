import pytest
from pytest_mock import MockerFixture
from pytestqt.qtbot import QtBot

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton

from modules.gui.widgets.start_display import StartDisplay
from modules.gui.widgets.start_display.components import QuestionParamsField
from modules.questions import NoQuestionsFoundError, NotEnoughQuestionsError

@pytest.fixture
def start_display(mocker: MockerFixture) -> StartDisplay:
    return StartDisplay()

def test_start_button_pressed(
        qtbot: QtBot,
        mocker: MockerFixture,
        start_display: StartDisplay,
        ) -> None:
    """
    Test on _start_button click:
    - emits start_button_pressed signal
    - calls _start_quiz_requested method
    """
    qtbot.addWidget(start_display)
    button = start_display.findChild(QPushButton, "startButton")
    assert button is not None

    start_display_start_quiz_requested_method = mocker.spy(start_display, "_start_quiz_requested")

    with qtbot.waitSignal(start_display._start_button.start_button_pressed, timeout=100):
        qtbot.mouseClick(button, Qt.MouseButton.LeftButton)
        start_display_start_quiz_requested_method.assert_called_once()

def test_start_quiz_requested(
        qtbot: QtBot,
        mocker: MockerFixture,
        start_display: StartDisplay,
        ) -> None:
    """
    Test on _start_button click:
    - emits start_quiz_requested signal
    - emits question params as signal argument
    - check emitted params
    """
    qtbot.addWidget(start_display)
    button = start_display.findChild(QPushButton, "startButton")
    assert button is not None

    with qtbot.waitSignal(start_display.start_quiz_requested, timeout=100) as signal_blocker:
        qtbot.mouseClick(button, Qt.MouseButton.LeftButton)

    expected_params = start_display._question_params.get_params()
    # Checks that question params has been returned
    assert signal_blocker.args == [expected_params]

def test_start_error_returned_emit_error(
        qtbot: QtBot,
        mocker: MockerFixture,
        start_display: StartDisplay,
        ) -> None:
    """
    Test generic error emitted through start_error_returned:
    - calls _on_start_error_returned with error
    - calls on_error_returned on _start_button
    - does not call on_error_reset_combobox_to_default_values
    """
    qtbot.addWidget(start_display)

    error = Exception("test")

    start_display_on_error = mocker.spy(
        start_display, 
        "_on_start_error_returned"
        )

    start_button_on_error = mocker.spy(
        start_display._start_button, 
        "on_error_returned"
        )

    question_params_on_error = mocker.spy(
        start_display._question_params, 
        "on_error_reset_combobox_to_default_values"
        )

    start_display.start_error_returned.emit(error)

    start_display_on_error.assert_called_once_with(error)

    start_button_on_error.assert_called_once_with()

    question_params_on_error.assert_not_called()

def test_start_error_returned_emit_no_questions_error(
        qtbot: QtBot,
        mocker: MockerFixture,
        start_display: StartDisplay,
        ) -> None:
    """
    Test NoQuestionsFoundError emitted through start_error_returned:
    - calls _on_start_error_returned with error
    - calls on_error_reset_combobox_to_default_values on question_params
    without parameters
    """
    qtbot.addWidget(start_display)

    error = NoQuestionsFoundError("test")

    start_display_on_error = mocker.spy(start_display, "_on_start_error_returned")

    question_params_on_error = mocker.spy(
        start_display._question_params, 
        "on_error_reset_combobox_to_default_values"
        )

    start_display.start_error_returned.emit(error)

    start_display_on_error.assert_called_once_with(error)

    question_params_on_error.assert_called_once_with()

def test_start_error_returned_emit_not_enough_questions_error(
        qtbot: QtBot,
        mocker: MockerFixture,
        start_display: StartDisplay,
        ) -> None:
    """
    Test NotEnoughQuestionsError emitted through start_error_returned:
    - calls _on_start_error_returned with error
    - calls on_error_reset_combobox_to_default_values with AMOUNT field
    """
    qtbot.addWidget(start_display)

    error = NotEnoughQuestionsError("test")

    start_display_on_error = mocker.spy(start_display, "_on_start_error_returned")

    question_params_on_error = mocker.spy(
        start_display._question_params, 
        "on_error_reset_combobox_to_default_values"
        )

    start_display.start_error_returned.emit(error)

    start_display_on_error.assert_called_once_with(error)

    question_params_on_error.assert_called_once_with(QuestionParamsField.AMOUNT)
