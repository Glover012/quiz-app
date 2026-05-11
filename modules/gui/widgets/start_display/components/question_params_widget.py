from PySide6.QtWidgets import QGridLayout, QWidget, QLabel, QComboBox
from PySide6.QtCore import Qt

from .....questions import CATEGORIES, DIFFICULTIES, QUESTION_TYPES


class QuestionParamsWidget(QWidget):
    """Widget for selecting quiz parameters and starting a new quiz."""

    def __init__(self) -> None:
        super().__init__()
        self._setup_layout()
        self._add_question_params_labels()
        self._add_question_params_comboboxes()

    def _setup_layout(self) -> None:
        self.main_layout = QGridLayout()
        self.setLayout(self.main_layout)

    def _add_question_params_labels(self) -> None:
        self.main_layout.addWidget(
            QLabel('Amount')
            , 0, 0, alignment=Qt.AlignmentFlag.AlignCenter
            )
        self.main_layout.addWidget(
            QLabel('Difficulty')
            , 0, 1, alignment=Qt.AlignmentFlag.AlignCenter
            )
        self.main_layout.addWidget(
            QLabel('Category')
            , 0, 2, alignment=Qt.AlignmentFlag.AlignCenter
            )
        self.main_layout.addWidget(
            QLabel('Type')
            , 0, 3, alignment=Qt.AlignmentFlag.AlignCenter
            )

    def _add_question_params_comboboxes(self) -> None:
        min_question_amount = 2
        max_question_amount = 30
        question_amount_list = [str(i) for i in range(min_question_amount, max_question_amount + 1)]
        self.question_amount_cb = QComboBox()
        self.question_amount_cb.addItems(question_amount_list)

        # Add values to comboboxes from static variables in API params
        self.question_category_cb = QComboBox()
        for category, category_id in CATEGORIES.items():
            self.question_category_cb.addItem(category, category_id)

        self.question_difficulty_cb = QComboBox()
        for difficulty, difficulty_id in DIFFICULTIES.items():
            self.question_difficulty_cb.addItem(difficulty, difficulty_id)

        self.question_type_cb = QComboBox()
        for question_type, question_type_id in QUESTION_TYPES.items():
            self.question_type_cb.addItem(question_type, question_type_id)

        self.main_layout.addWidget(self.question_amount_cb, 1, 0)
        self.main_layout.addWidget(self.question_difficulty_cb, 1, 1)
        self.main_layout.addWidget(self.question_category_cb, 1, 2)
        self.main_layout.addWidget(self.question_type_cb, 1, 3)

    def get_params(self) -> dict[str, str]:
        params = {
            "amount" : self.question_amount_cb.currentText(),
            "difficulty" : self.question_difficulty_cb.currentData(),
            "category" : self.question_category_cb.currentData(),
            "question_type" : self.question_type_cb.currentData(),
        }
        return params

    def _reset_comboboxes_to_default_values(self) -> None:
        """Rest values on recieved error."""
        