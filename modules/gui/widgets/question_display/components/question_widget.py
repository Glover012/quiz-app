from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtWidgets import QVBoxLayout, QFrame, QLabel, QRadioButton, QButtonGroup

if TYPE_CHECKING:
    from .....questions import Question


class QuestionWidget(QFrame):
    def __init__(self, question: Question):
        super().__init__()
        self.question = question
        self.setObjectName('questionWidgetFrame')
        self._setup_layout()
        self._add_question_label()
        self._add_question_answers_radio_buttons()
        self._add_question_info_label()
        # Default values
        self.correct_answer = False
        self.user_answer = None

    def _setup_layout(self):
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

    def _add_question_label(self):
        self.label = QLabel(self.question.question)
        self.label.setWordWrap(True)
        self.main_layout.addWidget(self.label)

    def _add_question_answers_radio_buttons(self):
        index = ['a', 'b', 'c', 'd']
        self.a_button_group = QButtonGroup()
        for i, answer in enumerate(self.question.all_answers):
            button = QRadioButton(
                f'{f'{index[i]}. ' if self.question.tp == "multiple" else ""}{answer}')
            button.setObjectName('questionAnswerRadioButton')
            self.a_button_group.addButton(button)
            self.main_layout.addWidget(button)
        self.a_button_group.buttonClicked.connect(self._on_answer_button_clicked)

    def _add_question_info_label(self):
        infoLabel = QLabel(
            f'Category: {self.question.category} |'
            f'Difficulty: {self.question.difficulty} |'
            f'Points: {self.question.points}'
            )
        infoLabel.setObjectName('questionInfoLabel')
        self.main_layout.addWidget(infoLabel)

    def _on_answer_button_clicked(self, button):
        self.user_answer = button.text()
        if self.question.correct_answer in self.user_answer:
            self.correct_answer = True
        else:
            self.correct_answer = False