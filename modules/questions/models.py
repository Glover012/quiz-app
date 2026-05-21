import logging
import html
import random

from .opentdb_client import OpenTriviaClient, OpenTriviaAPIResponseFormat

logger = logging.getLogger(__name__)


class Question:
    """Data object for one quiz question and its scoring data."""
    
    def __init__(
            self, tp: str,
            difficulty: str,
            category: str,
            question: str,
            correct_answer: str,
            incorrect_answers: list[str],
            all_answers: list[str],
            points: int,
            ) -> None:
        self.tp = tp
        self.difficulty = difficulty
        self.category = category
        self.question = question
        self.correct_answer = correct_answer
        self.incorrect_answers = incorrect_answers
        self.points = points
        self.all_answers = all_answers


class Questions:
    """
    Store quiz loading parameters and loaded Question objects.

    Creating an instance only stores the selected quiz parameters.
    Call load() to fetch question data from OpenTDB through OpenTriviaClient
    and convert the response into Question objects stored in questions_list.

    Raises:
        OpenTriviaClientError: If load() fails because the API request fails
            or the response cannot be converted into valid quiz questions.
    """

    def __init__(
            self,
            amount: str | int = 1,
            category: str = '',
            difficulty: str = '',
            question_type: str = '',
            ) -> None:
        """
        Initialize quiz question parameters.

        Args:
            amount: Number of questions requested from OpenTDB.

            category: OpenTDB category id, or an empty string for any category.

            difficulty: OpenTDB difficulty value, or an empty string for any difficulty.

            question_type: OpenTDB question type, or an empty string for any type.
        """
        self.questions_list: list[Question] = []
        self.amount = amount
        self.category = category
        self.difficulty = difficulty
        self.question_type = question_type

    def _get_question_data_from_api_client(self) -> OpenTriviaAPIResponseFormat:
        api_client = OpenTriviaClient()
        questions_data = api_client.get_questions_data(
            self.amount,
            self.category,
            self.difficulty,
            self.question_type,
            )
        return questions_data

    def _questions_data_to_question_objects(self, questions_data: OpenTriviaAPIResponseFormat) -> None:
        """Convert raw API question data into Question objects."""

        for question_params in questions_data["results"]:
            # Question parameters to variables, 
            # html.unescape to decode HTML entities from fields
            tp = question_params["type"]
            difficulty = question_params["difficulty"]
            category = html.unescape(question_params["category"])
            question = html.unescape(question_params["question"])
            correct_answer = html.unescape(question_params["correct_answer"])
            incorrect_answers = [html.unescape(answer) for answer in question_params["incorrect_answers"]]

            # Set all_answers, mix answers for multiple choice
            all_answers: list[str] = []
            if tp == 'boolean':
                all_answers = ["True", "False"]
            elif tp == 'multiple':
                all_answers = incorrect_answers.copy()
                all_answers.append(correct_answer)
                random.shuffle(all_answers)

            # Assign points, based on question difficulty
            points = 0
            if difficulty == "hard":
                points = 3
            elif  difficulty == "medium":
                points = 2
            elif  difficulty == "easy":
                points = 1

            # Add Question object, to questions_list
            self.questions_list.append(Question(
                tp, 
                difficulty, 
                category, 
                question, 
                correct_answer, 
                incorrect_answers, 
                all_answers, 
                points))
    
        logger.debug("Converted %s questions into Question objects.", len(self.questions_list))

    def load(self) -> None:
        """Fetch question data, build Question objects and store them into questions_list."""
        logger.info("Questions load initialized.")
        questions_data = self._get_question_data_from_api_client()
        self._questions_data_to_question_objects(questions_data)
