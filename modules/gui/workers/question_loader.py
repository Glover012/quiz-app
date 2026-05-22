import logging

from PySide6.QtCore import QObject, Signal, Slot

from ..widgets import QuestionParams
from ...questions import Questions, OpenTriviaClientError

logger = logging.getLogger(__name__)


class QuestionLoader(QObject):
    """Worker object that loads questions and emits success or error signals."""

    loaded = Signal(Questions)
    error = Signal(Exception)
    finished = Signal()

    def __init__(self, params: QuestionParams) -> None:
        super().__init__()
        self._amount = params["amount"]
        self._category = params["category"]
        self._difficulty = params["difficulty"]
        self._question_type = params["question_type"]

    @Slot()
    def run(self) -> None:
        """
        Load questions in a worker thread and emit the result through Qt signals.

        Emits:
            loaded: With a Questions instance when loading succeeds.
            error: With the raised exception when loading fails.
            finished: Always emitted after success or failure.
        """
        try:
            logger.info(
                "QuestionLoader started: amount=%s, category=%s, difficulty=%s, type=%s",
                self._amount,
                self._category or "any",
                self._difficulty or "any",
                self._question_type or "any",
                )
            questions = self._load_questions()
            logger.info("QuestionLoader loaded %s questions.", len(questions.questions_list))
            self.loaded.emit(questions)

        except OpenTriviaClientError as error:
            logger.warning("Question loading failed: %s: %s", type(error).__name__, error, exc_info=True)
            self.error.emit(error)

        except Exception as error:
            logger.exception("Unexpected question loading error.")
            self.error.emit(error)

        finally:
            self.finished.emit()

    def _load_questions(self) -> Questions:
        questions = Questions(self._amount, self._category, self._difficulty, self._question_type)
        questions.load()
        return questions
