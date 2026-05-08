import unittest
from unittest.mock import Mock, patch, MagicMock

import requests

from modules.questions.opentdb_client import OpenTriviaClient, OpenTriviaClientError


class TestOpenTriviaClient(unittest.TestCase):

    # Run before every test method
    def setUp(self) -> None:
        """Prepare API client instance."""
        self.client = OpenTriviaClient()

    @patch("modules.questions.opentdb_client.requests.get")
    def test_success_get_questions_data_with_default_params(self, mock_requests_get: MagicMock) -> None:
        """Test successful data retrieval with default request parameters."""
        # Mock response data
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "response_code": 0,
            "results": [
                {"q": 1}
            ]
        }
        mock_requests_get.return_value = mock_response

        # Call function with mocked requests.get and response
        data = self.client.get_questions_data()

        # Check if question data is not empty
        self.assertTrue(data['results'])
        # Check question amount = 1
        self.assertEqual(len(data['results']), 1)

        # Checks whether mock_requests_get has been called with proper parameters
        mock_requests_get.assert_called_once_with(
            OpenTriviaClient.BASE_URL,
            params={"amount": 1},
            timeout=10,
        )

        # Check whether raise_for_status has been called on mocked response
        mock_response.raise_for_status.assert_called_once()

    @patch("modules.questions.opentdb_client.requests.get")
    def test_success_get_questions_data_with_all_params(self, mock_requests_get: MagicMock) -> None:
        """Test successful data retrieval with all request parameters."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "response_code": 0,
            "results": [
                {"q": 1}, {"q": 2}
            ]
        }
        mock_requests_get.return_value = mock_response

        data = self.client.get_questions_data(
            amount=2,
            category="9",
            difficulty="easy",
            question_type="boolean",
        )

        self.assertTrue(data['results'])
        self.assertEqual(len(data['results']), 2)

        mock_requests_get.assert_called_once_with(
            OpenTriviaClient.BASE_URL,
            params={
                "amount": 2,
                "category": "9",
                "difficulty": "easy",
                "type": "boolean",
                },
            timeout=10,
        )

        mock_response.raise_for_status.assert_called_once()

    @patch("modules.questions.opentdb_client.requests.get")
    def test_get_questions_data_raises_error_when_no_questions(self, mock_requests_get: MagicMock) -> None:
        """Test that an empty results list raises OpenTriviaClientError."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "response_code": 0,
            "results": []
        }
        mock_requests_get.return_value = mock_response

        with self.assertRaises(OpenTriviaClientError) as error_context:
            self.client.get_questions_data()

        self.assertEqual(
            str(error_context.exception),
            "No questions found for selected parameters. Try different category, difficulty or type."
            )

    @patch("modules.questions.opentdb_client.requests.get")
    def test_get_questions_data_raises_error_when_not_enough_questions(self, mock_requests_get: MagicMock) -> None:
        """Test that too few questions raises OpenTriviaClientError."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "response_code": 0,
            "results": [
                {"q": 1}, {"q": 2}
            ]
        }
        mock_requests_get.return_value = mock_response

        with self.assertRaises(OpenTriviaClientError) as error_context:
            self.client.get_questions_data(amount=5)

        self.assertEqual(
            str(error_context.exception),
            "Not enough questions found for the selected parameters. Try lower number."
            )

    @patch("modules.questions.opentdb_client.requests.get")
    def test_get_questions_data_raises_timeout_error(self, mock_requests_get: MagicMock) -> None:
        """Test OpenTriviaClientError timeout error."""
        mock_requests_get.side_effect = requests.exceptions.Timeout

        with self.assertRaises(OpenTriviaClientError) as error_context:
            self.client.get_questions_data()

        self.assertEqual(
            str(error_context.exception),
            "Request to OpenTDB timed out."
            )

    @patch("modules.questions.opentdb_client.requests.get")
    def test_get_questions_data_raises_connection_error(self, mock_requests_get: MagicMock) -> None:
        """Test OpenTriviaClientError connection error."""
        mock_requests_get.side_effect = requests.exceptions.ConnectionError

        with self.assertRaises(OpenTriviaClientError) as error_context:
            self.client.get_questions_data()

        self.assertEqual(
            str(error_context.exception),
            "Could not connect to OpenTDB."
            )

    @patch("modules.questions.opentdb_client.requests.get")
    def test_get_questions_data_raises_http_error(self, mock_requests_get: MagicMock) -> None:
        """Test OpenTriviaClientError HTTP error."""
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError

        mock_requests_get.return_value = mock_response

        with self.assertRaises(OpenTriviaClientError) as error_context:
            self.client.get_questions_data()

        self.assertEqual(
            str(error_context.exception),
            "OpenTDB returned HTTP error."
            )

        mock_response.raise_for_status.assert_called_once()

    @patch("modules.questions.opentdb_client.requests.get")
    def test_get_questions_data_raises_value_error(self, mock_requests_get: MagicMock) -> None:
        """Test that invalid JSON responses raise OpenTriviaClientError."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError

        mock_requests_get.return_value = mock_response

        with self.assertRaises(OpenTriviaClientError) as error_context:
            self.client.get_questions_data()

        self.assertEqual(
            str(error_context.exception),
            "OpenTDB returned invalid JSON."
            )

    @patch("modules.questions.opentdb_client.requests.get")
    def test_get_questions_data_raises_key_error(self, mock_requests_get: MagicMock) -> None:
        """Test that missing response keys raise OpenTriviaClientError."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}

        mock_requests_get.return_value = mock_response

        with self.assertRaises(OpenTriviaClientError) as error_context:
            self.client.get_questions_data()

        self.assertEqual(
            str(error_context.exception),
            "OpenTDB returned unexpected format."
            )

    @patch("modules.questions.opentdb_client.requests.get")
    def test_get_questions_data_raises_type_error(self, mock_requests_get: MagicMock) -> None:
        """Test that invalid response types raise OpenTriviaClientError."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = 0

        mock_requests_get.return_value = mock_response

        with self.assertRaises(OpenTriviaClientError) as error_context:
            self.client.get_questions_data()

        self.assertEqual(
            str(error_context.exception),
            "OpenTDB returned unexpected format."
            )

    @patch("modules.questions.opentdb_client.requests.get")
    def test_get_questions_data_raises_unexpected_error(self, mock_requests_get: MagicMock) -> None:
        """Test OpenTriviaClientError unexpected error."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ZeroDivisionError

        mock_requests_get.return_value = mock_response

        with self.assertRaises(OpenTriviaClientError) as error_context:
            self.client.get_questions_data()

        self.assertEqual(
            str(error_context.exception),
            "Unexpected error occurred."
            )
