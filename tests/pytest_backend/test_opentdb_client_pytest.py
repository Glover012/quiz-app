import re

from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture
import requests

from modules.questions.opentdb_client import OpenTriviaClient, OpenTriviaClientError, NoQuestionsFoundError, NotEnoughQuestionsError

@pytest.fixture
def client() -> OpenTriviaClient:
    """Prepare a OpenTriviaClient instance for testing."""
    return OpenTriviaClient()

def test_success_get_questions_data_with_default_params(client: OpenTriviaClient, mocker: MockerFixture) -> None:
    """Test successfull call get_questions_data with default params."""

    mock_requests_get = mocker.patch("modules.questions.opentdb_client.requests.get")

    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "response_code": 0,
        "results": [{"q": 1}],
    }
    mock_requests_get.return_value = mock_response

    data = client.get_questions_data()

    assert data["results"]
    assert len(data["results"]) == 1

    mock_requests_get.assert_called_once_with(
        OpenTriviaClient.BASE_URL,
        params={"amount": 1},
        timeout=3,
    )
    mock_response.raise_for_status.assert_called_once()

def test_success_get_questions_data_with_all_params(client: OpenTriviaClient, mocker: MockerFixture) -> None:
    """Test successfull call get_questions_data with all params provided."""

    mock_requests_get: MagicMock = mocker.patch("modules.questions.opentdb_client.requests.get")

    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "response_code": 0,
        "results": [{"q": 1}],
    }
    mock_requests_get.return_value = mock_response

    data = client.get_questions_data(1, "9", "easy", "boolean")

    assert data["results"]
    assert len(data["results"]) == 1

    mock_requests_get.assert_called_once_with(
        OpenTriviaClient.BASE_URL,
        params={
            "amount": 1,
            "category": "9",
            "difficulty": "easy",
            "type": "boolean",
            },
        timeout=3,
    )
    mock_response.raise_for_status.assert_called_once()

def test_get_questions_data_raises_error_when_no_questions(client: OpenTriviaClient, mocker: MockerFixture) -> None:
    """Test get_questions_data raises NoQuestionsFoundError."""

    mock_requests_get: MagicMock = mocker.patch("modules.questions.opentdb_client.requests.get")

    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "response_code": 0,
        "results": [],
        }
    mock_requests_get.return_value = mock_response

    with pytest.raises(NoQuestionsFoundError, match=re.escape("No questions found")): # match uses regex
        client.get_questions_data()

    mock_requests_get.assert_called_once_with(
        OpenTriviaClient.BASE_URL,
        params={"amount": 1},
        timeout=3,
    )

def test_get_questions_data_raises_error_when_not_enought_questions(client: OpenTriviaClient, mocker: MockerFixture) -> None:
    """Test get_questions_data raises NotEnoughQuestionsError."""

    mock_requests_get: MagicMock = mocker.patch("modules.questions.opentdb_client.requests.get")

    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "response_code": 0,
        "results": [{"q":1}],
        }
    mock_requests_get.return_value = mock_response

    with pytest.raises(NotEnoughQuestionsError, match=re.escape("Not enough questions found")): # match uses regex
        client.get_questions_data(amount=2)

    mock_requests_get.assert_called_once_with(
        OpenTriviaClient.BASE_URL,
        params={"amount": 2},
        timeout=3,
    )

def test_get_questions_data_raises_timeout_error(client: OpenTriviaClient, mocker: MockerFixture) -> None:
    """Test get_questions_data raises proper OpenTriviaClientError for requests.exceptions.Timeout."""

    mock_requests_get: MagicMock = mocker.patch("modules.questions.opentdb_client.requests.get")
    mock_requests_get.side_effect = requests.exceptions.Timeout

    with pytest.raises(OpenTriviaClientError, match=re.escape("Request to OpenTDB timed out.")) as exc_info:
        client.get_questions_data()

    # Confirm traceback error type
    assert type(exc_info.value.__cause__) is requests.exceptions.Timeout

def test_get_questions_data_raises_connection_error(client: OpenTriviaClient, mocker: MockerFixture) -> None:
    """Test get_questions_data raises proper OpenTriviaClientError for requests.exceptions.ConnectionError."""

    mock_requests_get: MagicMock = mocker.patch("modules.questions.opentdb_client.requests.get")
    mock_requests_get.side_effect = requests.exceptions.ConnectionError

    with pytest.raises(OpenTriviaClientError, match=re.escape("Could not connect to OpenTDB.")) as exc_info:
        client.get_questions_data()

    # Confirm traceback error type
    assert type(exc_info.value.__cause__) is requests.exceptions.ConnectionError


def test_get_questions_data_raises_http_error(client: OpenTriviaClient, mocker: MockerFixture) -> None:
    """Test get_questions_data raises proper OpenTriviaClientError for requests.exceptions.HTTPError."""

    mock_requests_get: MagicMock = mocker.patch("modules.questions.opentdb_client.requests.get")

    mock_response = mocker.Mock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError

    mock_requests_get.return_value = mock_response

    with pytest.raises(OpenTriviaClientError, match=re.escape("OpenTDB returned HTTP error.")) as exc_info:
        client.get_questions_data()

    mock_response.raise_for_status.assert_called_once()

    # Confirm traceback error type
    assert type(exc_info.value.__cause__) is requests.exceptions.HTTPError

def test_get_questions_data_raises_value_error(client: OpenTriviaClient, mocker: MockerFixture) -> None:
    """Test get_questions_data raises proper OpenTriviaClientError for ValueError."""

    mock_requests_get: MagicMock = mocker.patch("modules.questions.opentdb_client.requests.get")

    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.side_effect = ValueError
    mock_requests_get.return_value = mock_response

    with pytest.raises(OpenTriviaClientError, match=re.escape("OpenTDB returned invalid JSON.")) as exc_info:
        client.get_questions_data()

    # Confirm traceback error type
    assert type(exc_info.value.__cause__) is ValueError

def test_get_questions_data_raises_key_error(client: OpenTriviaClient, mocker: MockerFixture) -> None:
    """Test get_questions_data raises proper OpenTriviaClientError for KeyError."""

    mock_requests_get: MagicMock = mocker.patch("modules.questions.opentdb_client.requests.get")

    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "response_code": 0,
        }
    mock_requests_get.return_value = mock_response

    with pytest.raises(OpenTriviaClientError, match=re.escape("OpenTDB returned unexpected format.")) as exc_info:
        client.get_questions_data()

    # Confirm traceback error type
    assert type(exc_info.value.__cause__) is KeyError

def test_get_questions_data_raises_type_error(client: OpenTriviaClient, mocker: MockerFixture) -> None:
    """Test get_questions_data raises proper OpenTriviaClientError for TypeError."""

    mock_requests_get: MagicMock = mocker.patch("modules.questions.opentdb_client.requests.get")

    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = 0
    mock_requests_get.return_value = mock_response

    with pytest.raises(OpenTriviaClientError, match=re.escape("OpenTDB returned unexpected format.")) as exc_info:
        client.get_questions_data()

    # Confirm traceback error type
    assert type(exc_info.value.__cause__) is TypeError

def test_get_questions_data_raises_unexpected_error(client: OpenTriviaClient, mocker: MockerFixture) -> None:
    """Test get_questions_data raises proper OpenTriviaClientError for unexpected Exception."""

    mock_requests_get: MagicMock = mocker.patch("modules.questions.opentdb_client.requests.get")
    mock_requests_get.side_effect = Exception

    with pytest.raises(OpenTriviaClientError, match=re.escape("Unexpected error occurred.")) as exc_info:
        client.get_questions_data()

    # Confirm traceback error type
    assert type(exc_info.value.__cause__) is Exception
