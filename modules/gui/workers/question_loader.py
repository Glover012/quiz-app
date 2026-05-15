import logging

from PySide6.QtCore import QObject, Signal, Slot

from ..widgets import QuestionParams
from ...questions.models import Questions

logger = logging.getLogger(__name__)


class QuestionLoader(QObject):
    """Worker object that loads questions and emits success or error signals."""

    loaded = Signal(Questions)
    error = Signal(Exception)
    finished = Signal()

    def __init__(self, params: QuestionParams) -> None:
        super().__init__()
        self.amount = params["amount"]
        self.category = params["category"]
        self.difficulty = params["difficulty"]
        self.question_type = params["question_type"]

    @Slot()
    def run(self) -> None:
        try:
            questions = self._load_questions()
            self.loaded.emit(questions)
        except Exception as error:
            logger.exception("Question loading failed.")
            self.error.emit(error)
        finally:
            self.finished.emit()

    def _load_questions(self) -> Questions:
        questions = Questions(self.amount, self.category, self.difficulty, self.question_type)
        return questions
