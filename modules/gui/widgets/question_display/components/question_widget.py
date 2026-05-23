from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtWidgets import QVBoxLayout, QFrame, QLabel, QRadioButton, QButtonGroup
from PySide6.QtCore import Slot

if TYPE_CHECKING:
    from .....questions import Question


class QuestionWidget(QFrame):
    """Widget that displays one question and tracks the selected answer."""

    def __init__(self, question: Question, question_number: int) -> None:
        super().__init__()
        self._question: Question = question
        self._question_number = question_number
        self.setObjectName('questionWidgetFrame')
        self.setProperty("answerState", None)
        self._setup_layout()
        self._add_question_label()
        self._add_question_answers_radio_buttons()
        self._add_question_info_label()
        # Default values
        self._correct_answer: bool = False

    def _setup_layout(self) -> None:
        self._main_layout = QVBoxLayout()
        self.setLayout(self._main_layout)

    def _add_question_label(self) -> None:
        self._label = QLabel(f"{self._question_number}. {self._question.question}")
        self._label.setWordWrap(True)
        self._main_layout.addWidget(self._label)

    def _add_question_answers_radio_buttons(self) -> None:
        index = ['a', 'b', 'c', 'd']
        self._answer_button_group = QButtonGroup()
        for i, answer in enumerate(self._question.all_answers):
            prefix = f"{index[i]}. " if self._question.tp == "multiple" else ""
            button = QRadioButton(f"{prefix}{answer}")
            button.setObjectName('questionAnswerRadioButton')
            button.setProperty("containCorrectAnswer", None)
            button.setProperty("answer", answer)
            self._answer_button_group.addButton(button)
            self._main_layout.addWidget(button)
        self._answer_button_group.buttonClicked.connect(self._on_answer_button_clicked)

    def _add_question_info_label(self) -> None:
        info_label = QLabel(
            f'Category: {self._question.category} |'
            f'Difficulty: {self._question.difficulty} |'
            f'Points: {self._question.points}'
            )
        info_label.setObjectName('questionInfoLabel')
        self._main_layout.addWidget(info_label)

    def _on_answer_button_clicked(self, button: QRadioButton) -> None:
        user_answer = str(button.property("answer"))
        if self._question.correct_answer == user_answer:
            self._correct_answer = True
        else:
            self._correct_answer = False

    def _color_widget_frame_on_finish(self) -> None:
        """Color widget frame green/red, based on user correct/incorrect answer."""
        if self._correct_answer:
            self.setProperty("answerState", "correct")
        else:
            self.setProperty("answerState", "incorrect")
        self.style().polish(self)

    def _format_buttons_on_finish(self):
        """Color button text green/red, based if contain correct answer. Disable buttons."""
        for button in self._answer_button_group.buttons():
            button.setEnabled(False)
            if self._question.correct_answer == str(button.property("answer")):
                button.setProperty("containCorrectAnswer", True)
            else:
                button.setProperty("containCorrectAnswer", False)
            button.style().polish(button)

    @Slot()
    def apply_finish_styling(self) -> None:
        """Color frame and buttons, on finish."""
        self._color_widget_frame_on_finish()
        self._format_buttons_on_finish()

    @property
    def question_points(self) -> int:
        return self._question.points

    @property
    def is_user_answer_correct(self) -> bool:
        return self._correct_answer
