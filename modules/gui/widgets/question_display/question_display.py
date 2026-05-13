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
        self.widget_list: list[QuestionWidget] = []
        self.questions_list: list[Question] = questions_list
        self._setup_layout()
        self._add_scrollable_widget()

        # Default result values
        self.total_question_points = 0
        self.user_points = 0
        self.user_good_answers = 0

        # Widget display
        self._display_questions(self.scrollable_widget_layout)
        self._add_finish_quiz_button()

    def _setup_layout(self) -> None:
        """Initialize main widget layout."""
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

    def _add_scrollable_widget(self) -> None:
        """Initialize scrollable widget to display questions."""
        self.scrollable_widget = QWidget()
        self.scrollable_widget_layout = QVBoxLayout()
        self.scrollable_widget.setLayout(self.scrollable_widget_layout)

        scroll = QScrollArea()
        scroll.setFrameShape(QScrollArea.Shape.NoFrame) # Remove scroll area default frame
        scroll.setWidget(self.scrollable_widget)
        scroll.setWidgetResizable(True)
        self.main_layout.addWidget(scroll)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def _display_questions(self, scrollable_widget_layout: QVBoxLayout) -> None:
        """Display questions in scrollable widget."""
        for question in self.questions_list:
            question_widget = QuestionWidget(question)
            self.widget_list.append(question_widget)
            # Numbering questions
            question_widget.label.setText(
                f"{len(self.widget_list)}. {question_widget.label.text()}")
            scrollable_widget_layout.addWidget(question_widget)

    def _calculate_score(self) -> None:
        """Calculate total points, user points and good answers."""
        for widget in self.widget_list:
            self.total_question_points += widget.question.points
            if widget.correct_answer:
                self.user_points += widget.question.points
                self.user_good_answers += 1

    def _format_question_widget_style_post_finish(self) -> None:
        """Format QuestionWidgets frame and button text based on correct/incorrect answer."""
        for widget in self.widget_list:
            # Color widget frames based on user_answer
            if widget.correct_answer:
                widget.setProperty('answerState', 'correct')
            else:
                widget.setProperty('answerState', 'incorrect')
            # Color button text based on which contain correct answer
            for button in widget.a_button_group.buttons():
                if widget.question.correct_answer in button.text():
                    button.setProperty('containAnswer', 'correct')
                else:
                    button.setProperty('containAnswer', 'incorrect')
                button.style().polish(button) # Refresh button style
                button.setEnabled(False) # Disable all button from manipulation
            # Refresh widget style to apply new properties
            widget.style().polish(widget)

    def _add_finish_quiz_button(self) -> None:
        """Add button to finish quiz."""
        self.finish_quiz_button = QPushButton('Finish Quiz')
        self.finish_quiz_button.setObjectName('finishQuizButton')
        self.finish_quiz_button.clicked.connect(self._on_finish_quiz_button_clicked)
        self.main_layout.addWidget(self.finish_quiz_button)

    @Slot()
    def _on_finish_quiz_button_clicked(self) -> None:
        """Handle finish quiz button click, calculate score, format question widgets and display results."""
        logger.debug("Finish quiz button clicked.")
        self.finish_quiz_button.deleteLater()
        self._calculate_score()
        self._format_question_widget_style_post_finish()
        self._display_result_widget()
        self._add_repeat_quiz_button()

        logger.info(
            "Quiz finished: good_answers=%s/%s, points=%s/%s",
            self.user_good_answers, len(self.widget_list),
            self.user_points, self.total_question_points,
            )

    def _display_result_widget(self) -> None:
        self.result_widget = ResultWidget(
            len(self.widget_list), 
            self.total_question_points, 
            self.user_points, 
            self.user_good_answers
            )
        self.main_layout.addWidget(self.result_widget)

    def _add_repeat_quiz_button(self) -> None:
        self.repeat_quiz_button = QPushButton('Repeat Quiz')
        self.repeat_quiz_button.setObjectName('repeatQuizButton')
        self.repeat_quiz_button.clicked.connect(self.repeat_button_clicked.emit)
        self.main_layout.addWidget(self.repeat_quiz_button)
