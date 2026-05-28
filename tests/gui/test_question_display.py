import pytest
from pytest_mock import MockerFixture
from pytestqt.qtbot import QtBot

from modules.questions.models import Questions, Question
from tests.data.api_response_test_data import QUESTION_TEST_DATA
from modules.gui.widgets.question_display.components import QuestionWidget
from modules.gui.widgets.question_display import QuestionDisplay

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

@pytest.fixture
def questions_list(questions) -> list[Question]:
    """Returned questions_list."""
    questions_list = questions.questions_list
    return questions_list

@pytest.fixture
def question_display(questions_list) -> QuestionDisplay:
    """
    Return QuestionDisplay that uses questions_list
    with loaded and formatted questiosn from QUESTION_TEST_DATA.
    """
    question_display = QuestionDisplay(questions_list)
    return question_display

@pytest.fixture
def question_widget_list_formatted(questions_list) -> list[QuestionWidget]:
    """
    Return mocked QuestionWidget list 5/5
    true/false amount of _correct_answer flags.
    """
    question_widget_list_formatted = []
    for i, question in enumerate(questions_list, start=1):
        widget = QuestionWidget(question, i)
        if i % 2 == 0:
            widget._correct_answer = True
        else:
            widget._correct_answer = False
        question_widget_list_formatted.append(widget)

    return question_widget_list_formatted

def test_finish_button(
        qtbot: QtBot, 
        mocker: MockerFixture, 
        question_display: QuestionDisplay
        ) -> None:
    """
    Test _finish_quiz_button:
    - call _on_finish_quiz_button_clicked
    when clicked
    """
    qtbot.addWidget(question_display)

    on_finish = mocker.spy(question_display, "_on_finish_quiz_button_clicked")

    question_display._finish_quiz_button.click()

    on_finish.assert_called_once_with()

def test_on_finish_quiz_button_clicked(
        qtbot: QtBot, 
        mocker: MockerFixture, 
        question_display: QuestionDisplay
        ) -> None:
    """
    Test _on_finish_quiz_button_clicked method:
    - _finish_quiz_button is disabled
    - _result_widget is added to layout
    - _add_repeat_quiz_button is added to layout
    - called methods:
        _calculate_result_and_format_widgets
        _display_result_widget
        _add_repeat_quiz_button
    """ 
    qtbot.addWidget(question_display)

    calc_result = mocker.spy(question_display, "_calculate_result_and_format_widgets")
    display_result = mocker.spy(question_display, "_display_result_widget")
    add_repeat_button = mocker.spy(question_display, "_add_repeat_quiz_button")

    question_display._on_finish_quiz_button_clicked()

    assert question_display._finish_quiz_button.isEnabled() is False

    assert hasattr(question_display, "_result_widget")
    assert hasattr(question_display, "_repeat_quiz_button")

    calc_result.assert_called_once_with()
    display_result.assert_called_once_with()
    add_repeat_button.assert_called_once_with()


def test_calculate_result_and_format_widgets_calls_apply_on_widgets(
        qtbot: QtBot, 
        mocker: MockerFixture,
        question_display: QuestionDisplay,
        ) -> None:
    """
    Test _calculate_result_and_format_widgets method:
    - call apply_finish_styling for every widget
    """
    qtbot.addWidget(question_display)

    apply_finish_styling_spies = []

    for widget in question_display._widget_list:
        apply_finish_styling_spy = mocker.spy(widget, "apply_finish_styling")
        apply_finish_styling_spies.append(apply_finish_styling_spy)

    question_display._calculate_result_and_format_widgets()

    for mocked_widget in apply_finish_styling_spies:
        mocked_widget.assert_called_once_with()

def test_calculate_result_and_format_widgets(
        qtbot: QtBot,
        question_display: QuestionDisplay,
        question_widget_list_formatted,
        ) -> None:
    """
    Test _calculate_result_and_format_widgets method:
    - properly cauculates:
        _questions_total_points
        _user_correct_answer_amount
        _user_total_earned_points
    on known data.
    """
    qtbot.addWidget(question_display)

    questions_total_points = 0
    user_correct_answer_amount = 0
    user_total_earned_points = 0

    for widget in question_widget_list_formatted:
        qtbot.addWidget(widget)

    question_display._widget_list = question_widget_list_formatted
    for widget in question_widget_list_formatted:

        questions_total_points += widget._question.points
        if widget._correct_answer is True:
            user_correct_answer_amount += 1
            user_total_earned_points += widget._question.points

    question_display._calculate_result_and_format_widgets()

    assert question_display._questions_total_points == questions_total_points
    assert question_display._user_correct_answer_amount == user_correct_answer_amount
    assert question_display._user_total_earned_points == user_total_earned_points

def test_repeat_quiz_button(
        qtbot: QtBot, 
        question_display: QuestionDisplay
        ) -> None:
    """
    Test _repeat_quiz_button:
    - emit repeat_button_clicked signal
    """
    qtbot.addWidget(question_display)
    question_display._on_finish_quiz_button_clicked()

    repeat_button = question_display._repeat_quiz_button

    with qtbot.waitSignal(question_display.repeat_button_clicked, timeout=100):
        repeat_button.click()
