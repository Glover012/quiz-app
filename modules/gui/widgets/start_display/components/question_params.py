from __future__ import annotations

import logging

from typing import TYPE_CHECKING

from PySide6.QtWidgets import QVBoxLayout, QGridLayout, QWidget, QLabel, QPushButton, QComboBox
from PySide6.QtCore import Qt, QTimer

from .....questions import Questions, OpenTriviaClientError, CATEGORIES, DIFFICULTIES, QUESTION_TYPES
from ...question_display import QuestionDisplay

if TYPE_CHECKING:
    from ....main_window import MainWindow

logger = logging.getLogger(__name__)


class QuestionParams(QWidget):
    """Widget for selecting quiz parameters and starting a new quiz."""
    
    def __init__(self, main_window: MainWindow) -> None:
        super().__init__()
        self.main_window = main_window
        self._setup_layout()
        self._add_start_button_widget()
        self._add_error_label()
        self._add_params_widget()

    def _setup_layout(self) -> None:
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

    def _add_start_button_widget(self) -> None:
        sb_widget = QWidget()
        sb_layout = QVBoxLayout()
        sb_widget.setLayout(sb_layout)
        self.sb = QPushButton('Start')
        self.sb.setObjectName('startButton')
        sb_layout.addWidget(self.sb, alignment=Qt.AlignmentFlag.AlignCenter)
        self.sb.clicked.connect(self._on_start_button_clicked)
        self.main_layout.addWidget(sb_widget, alignment=Qt.AlignmentFlag.AlignCenter)

    def _add_error_label(self) -> None:
        self.error_label = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)
        self.error_label.setObjectName('errorLabel')
        # Set size policy, to avoid widets movement on the screen when error label shows up
        size_policy = self.error_label.sizePolicy()
        size_policy.setRetainSizeWhenHidden(True)
        self.error_label.setSizePolicy(size_policy)
        self.error_label.setWordWrap(True)
        self.error_label.hide()
        self.main_layout.addWidget(self.error_label)

    def _show_error(self, error: OpenTriviaClientError) -> None:
        self.error_label.setText(f'API Error - {error}')
        self.error_label.show()
        # Hide label after 5 seconds
        QTimer.singleShot(5000, self.error_label.hide)

    def _add_params_widget(self) -> None:
        #select_params_label = QLabel('Select Quiz parameters:')
        #select_params_label.setObjectName('selectParamsLabel')
        #self.main_layout.addWidget(select_params_label, alignment=Qt.AlignmentFlag.AlignCenter)

        params_widget = QWidget()
        params_layout = QGridLayout()
        params_widget.setLayout(params_layout)

        params_layout.addWidget(
            QLabel('Amount')
            , 0, 0, alignment=Qt.AlignmentFlag.AlignCenter
            )
        params_layout.addWidget(
            QLabel('Difficulty')
            , 0, 1, alignment=Qt.AlignmentFlag.AlignCenter
            )
        params_layout.addWidget(
            QLabel('Category')
            , 0, 2, alignment=Qt.AlignmentFlag.AlignCenter
            )
        params_layout.addWidget(
            QLabel('Type')
            , 0, 3, alignment=Qt.AlignmentFlag.AlignCenter
            )

        min_amount = 2
        max_amount = 30
        question_amount_list = [str(i) for i in range(min_amount, max_amount + 1)]
        self.question_amount_cb = QComboBox()
        self.question_amount_cb.addItems(question_amount_list)

        self.question_category_cb = QComboBox()
        for category, category_id in CATEGORIES.items():
            self.question_category_cb.addItem(category, category_id)

        self.question_difficulty_cb = QComboBox()
        for difficulty, difficulty_id in DIFFICULTIES.items():
            self.question_difficulty_cb.addItem(difficulty, difficulty_id)

        self.question_type_cb = QComboBox()
        for question_type, question_type_id in QUESTION_TYPES.items():
            self.question_type_cb.addItem(question_type, question_type_id)

        params_layout.addWidget(self.question_amount_cb, 1, 0)
        params_layout.addWidget(self.question_difficulty_cb, 1, 1)
        params_layout.addWidget(self.question_category_cb, 1, 2)
        params_layout.addWidget(self.question_type_cb, 1, 3)

        self.main_layout.addWidget(params_widget, alignment=Qt.AlignmentFlag.AlignCenter)

    def _on_start_button_clicked(self) -> None:
        amount = self.question_amount_cb.currentText()
        diff = self.question_difficulty_cb.currentData()
        cat = self.question_category_cb.currentData()
        tp = self.question_type_cb.currentData()

        logger.debug(
            "Question params selected: amount=%s, difficulty=%s, category=%s, type=%s",
            amount,
            diff,
            cat,
            tp,
            )

        # Load questions from API client
        try:
            questions = Questions(amount=amount, category=cat, difficulty=diff, question_type=tp)
            logger.debug("Questions loaded successfully. Number of questions: %s", len(questions.questions_list))
            self.main_window.display_widget(QuestionDisplay(questions.questions_list))
        except OpenTriviaClientError as error:
            logger.warning("Failed to load questions: %s", error)
            self._show_error(error)
