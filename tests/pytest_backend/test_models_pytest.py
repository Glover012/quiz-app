from unittest.mock import MagicMock

from collections import Counter

import html
import re 
import random

import pytest
from pytest_mock import MockerFixture

from tests.data.api_response_test_data import QUESTION_TEST_DATA
from modules.questions.models import Questions, Question
from modules.questions.opentdb_client import OpenTriviaClientError, OpenTriviaAPIResponseFormat


@pytest.fixture
def questions() -> Questions:
    """Questions instance."""
    return Questions(10, "", "", "")

@pytest.fixture
def test_data() -> OpenTriviaAPIResponseFormat:
    """Test response json data from OpenTDB API."""
    return QUESTION_TEST_DATA

@pytest.fixture
def test_data_properties() -> dict[str, int]:
    """Analyze QUESTION_TEST_DATA for test operations."""

    question_amount = len(QUESTION_TEST_DATA["results"])
    boolean_amount = sum(question["type"] == "boolean" for question in QUESTION_TEST_DATA["results"])
    multiple_amount = sum(question["type"] == "multiple" for question in QUESTION_TEST_DATA["results"])
    properties = {
        "question_amount": question_amount,
        "boolean_amount": boolean_amount,
        "multiple_amount": multiple_amount,
    }
    return properties

def test_success_get_question_data_from_api_client(questions: Questions, test_data: OpenTriviaAPIResponseFormat, mocker: MockerFixture) -> None:
    """Test success retrival of test data from mocked API client."""

    mock_api_client: MagicMock = mocker.patch("modules.questions.models.OpenTriviaClient").return_value
    mock_api_client.get_questions_data.return_value = test_data

    data = questions._get_question_data_from_api_client()

    assert data == test_data

    mock_api_client.get_questions_data.assert_called_once_with(10, "", "", "")

def test_get_question_data_from_api_client_raises_error(questions: Questions, mocker: MockerFixture) -> None:
    """Test mock api client raises error."""

    mock_api_client: MagicMock = mocker.patch("modules.questions.models.OpenTriviaClient").return_value
    mock_api_client.get_questions_data.side_effect = OpenTriviaClientError

    with pytest.raises(OpenTriviaClientError):
        questions._get_question_data_from_api_client()

    mock_api_client.get_questions_data.assert_called_once_with(10, "", "", "")

def test_questions_data_transition_to_question_objects(questions: Questions, test_data: OpenTriviaAPIResponseFormat) -> None:
    """Test that Question objects match the raw data from QUESTION_TEST_DATA."""

    questions._questions_data_to_question_objects(test_data)

    # zip function for paired data comparison, strict=True to make sure list length is equal
    for question_object, question_api_data in zip(questions.questions_list, test_data["results"], strict=True):
        assert  question_object.tp == question_api_data["type"]
        assert  question_object.difficulty == question_api_data["difficulty"]
        assert  question_object.category == html.unescape(question_api_data["category"])
        assert  question_object.question == html.unescape(question_api_data["question"])
        assert  question_object.correct_answer == html.unescape(question_api_data["correct_answer"])
        if question_object.tp == "multiple":
            for question_object_inc_ans, question_api_data_inc_ans in zip(question_object.incorrect_answers, question_api_data["incorrect_answers"], strict=True):
                assert question_object_inc_ans == html.unescape(question_api_data_inc_ans)
        elif question_object.tp == "boolean":
            assert question_object.incorrect_answers == [html.unescape(inc_ans) for inc_ans in question_api_data["incorrect_answers"]]

def test_if_question_amount_is_correct(questions: Questions, test_data: OpenTriviaAPIResponseFormat, test_data_properties: dict[str, int]) -> None:
    """Test that questions_list has the expected length. Test that every questions_list item is a Question instance."""

    questions._questions_data_to_question_objects(test_data)

    assert len(questions.questions_list) == test_data_properties["question_amount"]
    assert all(isinstance(question, Question) for question in questions.questions_list)

def test_random_shuffle(questions: Questions, test_data: OpenTriviaAPIResponseFormat, test_data_properties: dict[str, int], mocker: MockerFixture) -> None:
    """Test that random.shuffle is called once for each multiple-choice question."""

    random_shuffle_mock: MagicMock = mocker.patch("modules.questions.models.random.shuffle", wraps=random.shuffle)

    questions._questions_data_to_question_objects(test_data)

    assert random_shuffle_mock.call_count == test_data_properties["multiple_amount"]

def test_html_unescape(questions: Questions, test_data: OpenTriviaAPIResponseFormat, test_data_properties: dict[str, int], mocker: MockerFixture) -> None:
    """Test that HTML entities are decoded in Question objects. Test that html.unescape is called the expected number of times."""

    html_unescape_mock: MagicMock = mocker.patch("modules.questions.models.html.unescape", wraps=html.unescape)

    questions._questions_data_to_question_objects(test_data)

    # Checks that no encoded HTML entities remains in Question objects
    for question_object in questions.questions_list:
        for q_value in question_object.__dict__.values():
            if isinstance(q_value, list):
                for el in q_value:
                    assert not (re.findall(r"&[a-zA-Z0-9#]+;", el))
            else:
                if isinstance(q_value, str):
                    assert not (re.findall(r"&[a-zA-Z0-9#]+;", q_value))

    # Check if html.unescape call count match expected value
    expected_html_unescape_call_count = (test_data_properties["boolean_amount"]*4) + (test_data_properties["multiple_amount"]*6)
    assert html_unescape_mock.call_count == expected_html_unescape_call_count

def test_question_points_assignment(questions: Questions, test_data: OpenTriviaAPIResponseFormat) -> None:
    """Test point assignment based on question difficulty."""

    questions._questions_data_to_question_objects(test_data)

    for question in questions.questions_list:
        if question.difficulty == "hard":
            assert question.points == 3
        elif question.difficulty == "medium":
            assert question.points == 2
        elif question.difficulty == "easy":
            assert question.points == 1

def test_all_answers_structure(questions: Questions, test_data: OpenTriviaAPIResponseFormat) -> None:
    """Test that boolean questions have True/False answers. Test that multiple-choice questions include all expected answers."""

    questions._questions_data_to_question_objects(test_data)

    for question in questions.questions_list:
        if question.tp == "boolean":
            assert question.all_answers == ["True", "False"]
        elif question.tp == "multiple":
            expected_answers = question.incorrect_answers + [question.correct_answer]
            # replace assertCountEqual with Counter
            assert Counter(question.all_answers) == Counter(expected_answers)
