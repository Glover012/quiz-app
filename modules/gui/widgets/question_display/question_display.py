import logging

from PySide6.QtWidgets import QVBoxLayout, QWidget, QScrollArea, QPushButton
from PySide6.QtCore import Qt, Signal, Slot

from .components import QuestionWidget, ResultWidget
from ....questions import Question

logger = logging.getLogger(__name__)


class QuestionDisplay(QWidget):
    """Display quiz questions, evaluate answers, and show the final result."""

    repeat_button_clicked = Signal()

    def __init__(self, questions_list: list[Question]) -> None:
        super().__init__()
        self._widget_list: list[QuestionWidget] = []
        self._questions_list: list[Question] = questions_list
        self._questions_amount: int = len(questions_list)
        self._questions_total_points: int = 0
        self._user_total_earned_points: int = 0
        self._user_correct_answer_amount: int = 0
        self._setup_layout()
        self._add_scrollable_widget()

        # Widget display
        self._display_questions(self._scrollable_widget_layout)
        self._add_finish_quiz_button()

    def _setup_layout(self) -> None:
        """Initialize main widget layout."""
        self._main_layout = QVBoxLayout()
        self.setLayout(self._main_layout)

    def _add_scrollable_widget(self) -> None:
        """Initialize scrollable widget to display questions."""
        self._scrollable_widget = QWidget()
        self._scrollable_widget_layout = QVBoxLayout()
        self._scrollable_widget.setLayout(self._scrollable_widget_layout)

        scroll = QScrollArea()
        scroll.setFrameShape(QScrollArea.Shape.NoFrame) # Remove scroll area default frame
        scroll.setWidget(self._scrollable_widget)
        scroll.setWidgetResizable(True)
        self._main_layout.addWidget(scroll)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def _display_questions(self, scrollable_widget_layout: QVBoxLayout) -> None:
        """Display questions in scrollable widget."""
        for i, question in enumerate(self._questions_list, start=1):
            question_widget = QuestionWidget(question, i)
            self._widget_list.append(question_widget)
            scrollable_widget_layout.addWidget(question_widget)

    def _add_finish_quiz_button(self) -> None:
        """Add button to finish quiz."""
        self._finish_quiz_button = QPushButton('Finish Quiz')
        self._finish_quiz_button.setObjectName('finishQuizButton')
        self._finish_quiz_button.clicked.connect(self._on_finish_quiz_button_clicked)
        self._main_layout.addWidget(self._finish_quiz_button)

    @Slot()
    def _on_finish_quiz_button_clicked(self) -> None:
        """Handle finish quiz button click, calculate score, format question widgets and display results."""
        logger.debug("Finish quiz button clicked.")
        self._finish_quiz_button.setEnabled(False)
        self._finish_quiz_button.deleteLater()

        self._calculate_result_and_format_widgets()
        self._display_result_widget()
        self._add_repeat_quiz_button()

        logger.info(
            "Quiz finished: good_answers=%s/%s, points=%s/%s",
            self._user_correct_answer_amount, len(self._widget_list),
            self._user_total_earned_points, self._questions_total_points,
            )

    def _calculate_result_and_format_widgets(self):
        for widget in self._widget_list:
            self._questions_total_points += widget.question_points
            widget.apply_finish_styling()
            if widget.is_user_answer_correct:
                self._user_correct_answer_amount += 1
                self._user_total_earned_points += widget.question_points

    def _display_result_widget(self) -> None:
        self._result_widget = ResultWidget(
            self._questions_amount,
            self._questions_total_points,
            self._user_total_earned_points,
            self._user_correct_answer_amount,
        )
        self._main_layout.addWidget(self._result_widget)

    def _add_repeat_quiz_button(self) -> None:
        self._repeat_quiz_button = QPushButton('Repeat Quiz')
        self._repeat_quiz_button.setObjectName('repeatQuizButton')
        self._repeat_quiz_button.clicked.connect(self.repeat_button_clicked.emit)
        self._main_layout.addWidget(self._repeat_quiz_button)
