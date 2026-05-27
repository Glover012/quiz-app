import html

import pytest
from pytest_mock import MockerFixture
from pytestqt.qtbot import QtBot

from modules.questions.models import Questions
from tests.data.api_response_test_data import QUESTION_TEST_DATA
from modules.gui.widgets.question_display.components import QuestionWidget

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
def question(questions):
    """Signle question from QUESTION_TEST_DATA."""
    question = questions.questions_list[0]
    return question

@pytest.fixture
def question_widget(question) -> QuestionWidget:
    """
    Single QuestionWidget, contain first question from QUESTION_TEST_DATA.
    QuestionWidget contain formatted Question object in _question.

    Question RAW data from API = {
      "type": "multiple",
      "difficulty": "hard",
      "category": "Entertainment: Video Games",
      "question": "In the Pok&eacute;mon series, what is Palkia&#039;s hidden ability?",
      "correct_answer": "Telepathy",
      "incorrect_answers": [
        "Pressure",
        "Water Bubble",
        "Hydration"
      ]
    }
    """
    return QuestionWidget(question, 1)

@pytest.fixture
def question_widget_list(questions) -> list[QuestionWidget]:
    """Single QuestionWidget."""
    question_widget_list = []
    for i, question in enumerate(questions.questions_list, start=1):
        question_widget = QuestionWidget(question, i)
        question_widget_list.append(question_widget)
    return question_widget_list

def test_question_widget_label_text(qtbot: QtBot, question_widget_list: list[QuestionWidget]) -> None:
    """
    Test QuestionWidget label:
    - question label contain correct question and proper assign number
    """
    # Tests related to Questions/Question classes are already covered
    # Additional comparison is redundant
    for i, question_widget in enumerate(question_widget_list):
        qtbot.addWidget(question_widget)
        expected_question = html.unescape(QUESTION_TEST_DATA["results"][i]["question"])
        assert question_widget._label.text() == f"{i+1}. {expected_question}"

def test_question_widget_radio_buttons_content(qtbot: QtBot, question_widget_list: list[QuestionWidget]) -> None:
    """
    Test QuestionWidget radio buttons content:
    - check default properties, containCorrectAnswer is None,
    answer == question_answer in all_answers
    - check button has expected text 
    """

    for question_widget in question_widget_list:
        qtbot.addWidget(question_widget)

        prefixes = ['a', 'b', 'c', 'd']
        question_type = question_widget._question.tp
        all_answers = question_widget._question.all_answers
        button_group = question_widget._answer_button_group.buttons()
        assert len(button_group) == len(all_answers)

        for prefix, (button, answer) in zip(prefixes, zip(button_group, all_answers, strict=True)):
            assert button.property("containCorrectAnswer") is None
            assert button.property("answer") == answer

            if question_type == "multiple":
                assert button.text() == f"{prefix}. {answer}"
            else:
                assert button.text() == f"{answer}"

def test_on_answer_button_clicked(qtbot: QtBot, mocker: MockerFixture, question_widget_list: list[QuestionWidget]):
    """
    Test QuestionWidget _on_answer_button_clicked method:
    - on mouse click _on_answer_button_clicked is called once
    with button as parameter
    - if button has correct answer inside, confirm
    that _correct_answer flag is True, else False
    """

    for question_widget in question_widget_list:
        qtbot.addWidget(question_widget)

        button_clicked_method = mocker.spy(question_widget, "_on_answer_button_clicked")

        button_group = question_widget._answer_button_group.buttons()
        correct_answer = question_widget._question.correct_answer

        for button in button_group:
            button_clicked_method.reset_mock() # Reset call count required

            button_answer = button.property("answer")
            expected = button_answer == correct_answer

            button.click()
            button_clicked_method.assert_called_once_with(button)

            assert question_widget._correct_answer is expected

def test_color_widget_frame_on_finish_correct(qtbot: QtBot, question_widget: QuestionWidget):
    """
    Test QuestionWidget _color_widget_frame_on_finish method.
    AnswerState property is correct when:
    - selected correct answer is True
    """
    qtbot.addWidget(question_widget)

    for button in question_widget._answer_button_group.buttons():
        button_answer = button.property("answer")
        correct_answer = question_widget._question.correct_answer
        if button_answer == correct_answer:
            button.click()
            break

    question_widget._color_widget_frame_on_finish()
    answer_state = question_widget.property("answerState")

    assert answer_state == "correct"

def test_color_widget_frame_on_finish_incorrect(qtbot: QtBot, question_widget: QuestionWidget):
    """
    Test QuestionWidget _color_widget_frame_on_finish method.
    AnswerState property is incorrect when:
    - answer not selected, button not clicked
    - with selected button that contains incorrect answer
    """
    qtbot.addWidget(question_widget)

    question_widget._color_widget_frame_on_finish()
    answer_state = question_widget.property("answerState")

    assert answer_state == "incorrect"

    for button in question_widget._answer_button_group.buttons():
        button_answer = button.property("answer")
        correct_answer = question_widget._question.correct_answer
        if button_answer != correct_answer:
            button.click()
            break

    question_widget._color_widget_frame_on_finish()
    answer_state = question_widget.property("answerState")

    assert answer_state == "incorrect"

def test_format_buttons_on_finish(qtbot: QtBot, question_widget_list: list[QuestionWidget]):
    """
    Test _format_buttons_on_finish method:
    - all buttons are disabled
    - containCorrectAnswer property is True/False
    based on _question.correct_answer
    """
    for question_widget in question_widget_list:
        qtbot.addWidget(question_widget)

        button_group = question_widget._answer_button_group.buttons()
        first_button = button_group[0]
        first_button.click()
        question_widget._format_buttons_on_finish()

        for button in button_group:
            button_have_correct_answer_inside = button.property("containCorrectAnswer")
            button_answer = button.property("answer")
            correct_answer = question_widget._question.correct_answer

            assert button.isEnabled() is False

            if button_answer == correct_answer:
                assert button_have_correct_answer_inside == "true"
            elif button_answer != correct_answer:
                assert button_have_correct_answer_inside == "false"

def test_apply_finish_styling(qtbot: QtBot, mocker: MockerFixture, question_widget: QuestionWidget):
    """
    Test apply_finish_styling method:
    - calls _color_widget_frame_on_finish and
    _format_buttons_on_finish methods
    """

    color_method = mocker.spy(question_widget, "_color_widget_frame_on_finish")
    format_button_method = mocker.spy(question_widget, "_format_buttons_on_finish")

    qtbot.addWidget(question_widget)

    question_widget.apply_finish_styling()

    color_method.assert_called_once_with()
    format_button_method.assert_called_once_with()
