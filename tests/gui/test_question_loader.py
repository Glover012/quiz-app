import pytest
from pytest_mock import MockerFixture
from pytestqt.qtbot import QtBot

from modules.gui.widgets.start_display import QuestionParams
from modules.gui.workers.question_loader import QuestionLoader
from modules.questions import Questions, OpenTriviaClientError
from tests.data.api_response_test_data import QUESTION_TEST_DATA

@pytest.fixture
def question_params() -> QuestionParams:
    question_params: QuestionParams = {
            "amount": "10",
            "difficulty": "",
            "category": "",
            "question_type": "",
        }
    return question_params

@pytest.fixture
def question_loader(question_params) -> QuestionLoader:
    question_loader = QuestionLoader(question_params)
    return question_loader

@pytest.fixture
def questions(mocker: MockerFixture) -> Questions:
    """
    Mock _get_question_data_from_api_client method on Questions class.
    Uses static and known QUESTION_TEST_DATA as api response and 
    forms question object with known data.
    """
    questions = Questions(10, "", "", "")
    mocker.patch.object(
        questions, 
        "_get_question_data_from_api_client", 
        return_value=QUESTION_TEST_DATA
        )
    return questions

def test_loader_run(
        mocker: MockerFixture, 
        question_params: QuestionParams,
        questions: Questions,
        ) -> None:
    """
    Test run method + _load_questions:
    - calls _load_questions method
    - calls Questions class with proper params
    - calls Questions.load method
    """
    questions_cls = mocker.patch(
        "modules.gui.workers.question_loader.Questions",
        return_value = questions,
        )

    questions_load = mocker.spy(questions, "load")

    question_loader = QuestionLoader(question_params)

    load_questions = mocker.spy(question_loader, "_load_questions")

    question_loader.run()

    load_questions.assert_called_once_with()

    questions_cls.assert_called_once_with(
        question_params["amount"],
        question_params["category"],
        question_params["difficulty"],
        question_params["question_type"],
    )

    questions_load.assert_called_once_with()

def test_loader_run_loaded_finished_signal(
        qtbot: QtBot, 
        mocker: MockerFixture, 
        question_params: QuestionParams,
        questions: Questions,
        ) -> None:
    """
    Test loader signals on run method:
    - loaded
    - finished
    """
    question_loader = QuestionLoader(question_params)

    load_questions = mocker.patch.object(
        question_loader,
        "_load_questions",
        return_value=questions,
    )

    with qtbot.waitSignal(question_loader.loaded, timeout=100) as loaded_blocker:
        with qtbot.waitSignal(question_loader.finished, timeout=100):
            question_loader.run()

    load_questions.assert_called_once_with()

    assert loaded_blocker.args == [questions]

def test_loader_run_error_finished_signal(
        qtbot: QtBot, 
        mocker: MockerFixture, 
        question_params: QuestionParams,
        ) -> None:
    """
    Test loader error signal on run method.
    - error signal emit error
    - finished signal emitted
    """
    question_loader = QuestionLoader(question_params)

    error = OpenTriviaClientError("Test")

    load_questions = mocker.patch.object(
        question_loader,
        "_load_questions",
        side_effect=error,
        )

    with qtbot.waitSignal(question_loader.error, timeout=100) as error_blocker:
        with qtbot.waitSignal(question_loader.finished, timeout=100):
            question_loader.run()

    load_questions.assert_called_once_with()

    assert error_blocker.args == [error]
