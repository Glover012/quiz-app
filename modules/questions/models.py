from typing import Any
import html, random
from .opentdb_client import OpenTriviaClient, OpenTriviaClientError

class Question:
    def __init__(
            self, tp: str, 
            difficulty: str, 
            category: str, 
            question: str, 
            correct_answer: str, 
            incorrect_answers: list, 
            all_answers: list, 
            points: int) -> None:
        self.tp = tp
        self.difficulty = difficulty
        self.category = category
        self.question = question
        self.correct_answer = correct_answer
        self.incorrect_answers = incorrect_answers
        self.points = points
        self.all_answers = all_answers

class Questions:
    questions_list = []

    def __init__(
            self, 
            amount: str | int = 1, 
            category: str = '', 
            difficulty: str = '', 
            question_type: str = ''
            ) -> None:
        self.questions_list.clear() # Clear questions_list before adding new questions
        self.amount = amount
        self.category = category
        self.difficulty = difficulty
        self.question_type = question_type
        # Methods
        questions_data = self.get_question_data_from_api_client()
        self.questions_data_to_question_objects(questions_data)

    def get_question_data_from_api_client(self) -> dict[str, Any]:
        api_client = OpenTriviaClient()
        try:
            questions_data = api_client.get_questions_data(
                self.amount,
                self.category,
                self.difficulty,
                self.question_type
                )
            return questions_data
        except OpenTriviaClientError as error:
            raise error

    def questions_data_to_question_objects(self, questions_data: dict[str, Any]) -> None:
        "Question JSON data from API to Question objects. Add Question objects to questions_list"
        for question_params in questions_data["results"]:
            # Question parameters to variables, html.unescape to format html symbols
            tp = question_params["type"]
            difficulty = question_params["difficulty"]
            category = question_params["category"]
            question = html.unescape(question_params["question"])
            correct_answer = html.unescape(question_params["correct_answer"])
            incorrect_answers = [html.unescape(answer) for answer in question_params["incorrect_answers"]]

            # Set all_answers, mix answers for multiple choice
            all_answers = []
            if tp == 'boolean':
                all_answers = ["True", "False"]
            elif tp == 'multiple':
                all_answers = incorrect_answers.copy()
                all_answers.append(correct_answer)
                random.shuffle(all_answers)

            # Assign points, based on question difficulty
            points = 0
            if difficulty == "hard": points = 3
            elif  difficulty == "medium": points = 2
            elif  difficulty == "easy": points = 1

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
