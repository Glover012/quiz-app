import unittest
from unittest.mock import patch, MagicMock

import html, re, random

from tests.api_response_test_data import QUESTION_TEST_DATA
from modules.questions.models import Questions, Question
from modules.questions.opentdb_client import OpenTriviaClientError


class TestQuestionsModels(unittest.TestCase):

    def setUp(self) -> None:
        """
        Prepare a Questions instance for testing its methods.
        Analyze QUESTION_TEST_DATA for test operations.
        """
        self.questions = Questions(10, "", "", "")

        # Count question types in QUESTION_TEST_DATA.
        self.question_amount = len(QUESTION_TEST_DATA["results"])
        self.boolean_amount = sum(
            question["type"] == "boolean"
            for question in QUESTION_TEST_DATA["results"]
            )
        self.multiple_amount = sum(
            question["type"] == "multiple"
            for question in QUESTION_TEST_DATA["results"]
            )
        
    @patch("modules.questions.models.OpenTriviaClient")
    def test_success_get_question_data_from_api_client(self, mock_api_client_class: MagicMock) -> None:
        """
        Test successful data retrieval from the API client.
        """
        mock_client = mock_api_client_class.return_value
        mock_client.get_questions_data.return_value = QUESTION_TEST_DATA

        self.assertEqual(self.questions._get_question_data_from_api_client(), QUESTION_TEST_DATA)

        mock_client.get_questions_data.assert_called_once_with(10, "", "", "")

    @patch("modules.questions.models.OpenTriviaClient")
    def test_get_question_data_from_api_client_raises_error(self, mock_api_client_class: MagicMock) -> None:
        """
        Test that an API client error is raised.
        """
        mock_client = mock_api_client_class.return_value
        mock_client.get_questions_data.side_effect = OpenTriviaClientError

        with self.assertRaises(OpenTriviaClientError):
            self.questions._get_question_data_from_api_client()

        mock_client.get_questions_data.assert_called_once_with(10, "", "", "")

    def test_questions_data_transition_to_question_objects(self) -> None:
        """
        Test that Question objects match the raw data from QUESTION_TEST_DATA.
        """
        self.questions._questions_data_to_question_objects(QUESTION_TEST_DATA)

        questions_api_test_data = QUESTION_TEST_DATA['results']

        for q_obj, q_api in zip(self.questions.questions_list, questions_api_test_data, strict=True):
            self.assertEqual(q_obj.tp, q_api["type"])
            self.assertEqual(q_obj.difficulty, q_api["difficulty"])
            self.assertEqual(q_obj.category, html.unescape(q_api["category"]))
            self.assertEqual(q_obj.question, html.unescape(q_api["question"]))
            self.assertEqual(q_obj.correct_answer, html.unescape(q_api["correct_answer"]))
            if q_obj.tp == "multiple":
                for q_obj_ia, q_api_ia in zip(q_obj.incorrect_answers, q_api["incorrect_answers"], strict=True):
                    self.assertEqual(q_obj_ia, html.unescape(q_api_ia))
            elif q_obj.tp == "boolean":
                self.assertEqual(
                    q_obj.incorrect_answers, 
                    [html.unescape(answer) for answer in q_api["incorrect_answers"]]
                    )

    def test_if_question_amount_is_correct(self) -> None:
        """
        Test that questions_list has the expected length.
        Test that every questions_list item is a Question instance.
        """
        self.questions._questions_data_to_question_objects(QUESTION_TEST_DATA)

        self.assertEqual(self.question_amount, len(self.questions.questions_list))
        self.assertTrue(
            all(isinstance(question, Question) for question in self.questions.questions_list)
            )

    @patch("modules.questions.models.random.shuffle", wraps=random.shuffle)
    def test_random_shuffle(self, mock_random_shuffle: MagicMock) -> None:
        """
        Test that random.shuffle is called once for each multiple-choice question.
        """
        self.questions._questions_data_to_question_objects(QUESTION_TEST_DATA)

        random_shuffle_call_count = mock_random_shuffle.call_count
        self.assertEqual(random_shuffle_call_count, self.multiple_amount)

    @patch("modules.questions.models.html.unescape", wraps=html.unescape)
    def test_html_unescape(self, mock_html_unescape: MagicMock) -> None:
        """
        Test that HTML entities are decoded in Question objects.
        Test that html.unescape is called the expected number of times.
        """
        self.questions._questions_data_to_question_objects(QUESTION_TEST_DATA)

        # Check that no encoded HTML entities remain in Question objects.
        for question in self.questions.questions_list:
            for q_key, q_value in question.__dict__.items():
                if isinstance(q_value, list):
                    for el in q_value:
                        self.assertFalse(re.findall(r"&[a-zA-Z0-9#]+;", el))
                else:
                    if isinstance(q_value, str):
                        self.assertFalse(re.findall(r"&[a-zA-Z0-9#]+;", q_value))

        # Check the html.unescape call count against the expected value.
        html_unescape_call_count = mock_html_unescape.call_count
        expeced_html_unescape_call_count = (self.boolean_amount*4) + (self.multiple_amount*6)
        self.assertEqual(html_unescape_call_count, expeced_html_unescape_call_count)

    def test_question_points_assignment(self) -> None:
        """
        Test point assignment based on question difficulty.
        """
        self.questions._questions_data_to_question_objects(QUESTION_TEST_DATA)

        for question in self.questions.questions_list:
            if question.difficulty == "hard":
                self.assertEqual(question.points, 3)
            elif question.difficulty == "medium":
                self.assertEqual(question.points, 2)
            elif question.difficulty == "easy":
                self.assertEqual(question.points, 1)
    
    def test_all_answers_structure(self) -> None:
        """
        Test that boolean questions have True/False answers.
        Test that multiple-choice questions include all expected answers.
        """
        self.questions._questions_data_to_question_objects(QUESTION_TEST_DATA)

        for question in self.questions.questions_list:
            if question.tp == "boolean":
                self.assertEqual(question.all_answers, ["True", "False"])
            elif question.tp == "multiple":
                expected_answers = question.incorrect_answers + [question.correct_answer]
                self.assertCountEqual(question.all_answers, expected_answers)
