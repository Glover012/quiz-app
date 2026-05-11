from PySide6.QtCore import QObject, Signal, Slot

from ...questions.models import Questions
from ...questions.opentdb_client import OpenTriviaClientError


class QuestionLoader(QObject):
    """
    Object responsible for loading questions. Emit signal, based on load_questions result.
    Object shall be run by designated WorkerThreadController.
    """

    loaded = Signal(Questions)
    error = Signal(OpenTriviaClientError)
    finished = Signal()

    def __init__(self, params: dict[str, str]) -> None:
        super().__init__()
        self.amount = params["amount"]
        self.category = params["category"]
        self.difficulty = params["difficulty"]
        self.question_type = params["question_type"]

    @Slot()
    def run(self) -> Signal | None:
        try:
            questions = self._load_questions()
            self.loaded.emit(questions)
        except OpenTriviaClientError as api_error:
            self.error.emit(api_error)
        finally:
            self.finished.emit()

    def _load_questions(self) -> Questions:
        questions = Questions(self.amount, self.category, self.difficulty, self.question_type)
        return questions
