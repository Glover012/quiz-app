from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtWidgets import QVBoxLayout, QFrame, QLabel, QRadioButton, QButtonGroup

if TYPE_CHECKING:
    from .....questions import Question


class QuestionWidget(QFrame):
    """Widget that displays one question and tracks the selected answer."""

    def __init__(self, question: Question) -> None:
        super().__init__()
        self.question: Question = question
        self.setObjectName('questionWidgetFrame')
        self._setup_layout()
        self._add_question_label()
        self._add_question_answers_radio_buttons()
        self._add_question_info_label()
        # Default values
        self.correct_answer: bool = False
        self.user_answer: str | None = None

    def _setup_layout(self) -> None:
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

    def _add_question_label(self) -> None:
        self.label = QLabel(self.question.question)
        self.label.setWordWrap(True)
        self.main_layout.addWidget(self.label)

    def _add_question_answers_radio_buttons(self) -> None:
        index = ['a', 'b', 'c', 'd']
        self.a_button_group = QButtonGroup()
        for i, answer in enumerate(self.question.all_answers):
            button = QRadioButton(
                f'{f'{index[i]}. ' if self.question.tp == "multiple" else ""}{answer}'
                )
            button.setObjectName('questionAnswerRadioButton')
            button.setProperty("answer", answer)
            self.a_button_group.addButton(button)
            self.main_layout.addWidget(button)
        self.a_button_group.buttonClicked.connect(self._on_answer_button_clicked)

    def _add_question_info_label(self) -> None:
        info_label = QLabel(
            f'Category: {self.question.category} |'
            f'Difficulty: {self.question.difficulty} |'
            f'Points: {self.question.points}'
            )
        info_label.setObjectName('questionInfoLabel')
        self.main_layout.addWidget(info_label)

    def _on_answer_button_clicked(self, button: QRadioButton) -> None:
        self.user_answer = str(button.property("answer"))
        if self.question.correct_answer == self.user_answer:
            self.correct_answer = True
        else:
            self.correct_answer = False