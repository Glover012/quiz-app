from typing import TypedDict

from enum import StrEnum

from PySide6.QtWidgets import QWidget, QLabel, QComboBox, QHBoxLayout, QVBoxLayout, QFrame
from PySide6.QtCore import Qt, Slot


from .....questions import CATEGORIES, DIFFICULTIES, QUESTION_TYPES

class QuestionParams(TypedDict):
    amount: str
    difficulty: str
    category: str
    question_type: str


class QuestionParamsField(StrEnum):
    """Quiz parameter fields that can be reset and marked as invalid."""

    AMOUNT = "amount"
    DIFFICULTY = "difficulty"
    CATEGORY = "category"
    QUESTION_TYPE = "question_type"


class ParamFrame(QFrame):
    """Frame that groups a parameter label with its combo box."""
    def __init__(self, label_text: str) -> None:
        super().__init__()
        self.label_text = label_text
        self.setObjectName("paramFrame")
        self.setProperty("paramState", None)
        self._setup_layout()
        self._add_label()

    def _setup_layout(self) -> None:
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.main_layout)

    def _add_label(self) -> None:
        param_label = QLabel(self.label_text)
        self.main_layout.addWidget(
            param_label,
            alignment=Qt.AlignmentFlag.AlignBottom,
            )

    def add_combobox(self, combobox: QComboBox) -> None:
        self.main_layout.addWidget(
            combobox,
            alignment=Qt.AlignmentFlag.AlignTop,
            )


class QuestionParamsWidget(QWidget):
    """Widget for selecting OpenTDB quiz parameters."""

    def __init__(self) -> None:
        super().__init__()
        self.frame_list: list[ParamFrame] = []
        self._setup_layout()
        self._setup_question_params_comboboxes()
        self._add_question_param_frames()

    def _setup_layout(self) -> None:
        self.main_layout = QHBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.main_layout)

    def _setup_question_params_comboboxes(self) -> None:
        min_question_amount = 2
        max_question_amount = 100
        question_amount_list = [str(i) for i in range(min_question_amount, max_question_amount + 1)]
        self.amount_cb = QComboBox()
        self.amount_cb.addItems(question_amount_list)

        # Add values to comboboxes from static variables in API params
        self.category_cb = QComboBox()
        for category, category_id in CATEGORIES.items():
            self.category_cb.addItem(category, category_id)

        self.difficulty_cb = QComboBox()
        for difficulty, difficulty_id in DIFFICULTIES.items():
            self.difficulty_cb.addItem(difficulty, difficulty_id)

        self.type_cb = QComboBox()
        for question_type, question_type_id in QUESTION_TYPES.items():
            self.type_cb.addItem(question_type, question_type_id)

    def _add_question_param_frames(self) -> None:
        self.amount_frame = ParamFrame("Amount")
        self.frame_list.append(self.amount_frame)
        self.amount_frame.add_combobox(self.amount_cb)
        self.main_layout.addWidget(self.amount_frame)

        self.difficulty_frame = ParamFrame("Difficulty")
        self.frame_list.append(self.difficulty_frame)
        self.difficulty_frame.add_combobox(self.difficulty_cb)
        self.main_layout.addWidget(self.difficulty_frame)

        self.category_frame = ParamFrame("Category")
        self.frame_list.append(self.category_frame)
        self.category_frame.add_combobox(self.category_cb)
        self.main_layout.addWidget(self.category_frame)

        self.type_frame = ParamFrame("Type")
        self.frame_list.append(self.type_frame)
        self.type_frame.add_combobox(self.type_cb)
        self.main_layout.addWidget(self.type_frame)

    def get_params(self) -> QuestionParams:
        """Return selected question params in comboboxes."""
        self._reset_error_frames() # Reset frame colors before another load attempt.
        params: QuestionParams = {
            "amount": str(self.amount_cb.currentText()),
            "difficulty": str(self.difficulty_cb.currentData()),
            "category": str(self.category_cb.currentData()),
            "question_type": str(self.type_cb.currentData()),
        }
        return params

    @Slot()
    def on_error_reset_combobox_to_default_values(
        self, *fields: QuestionParamsField
        ) -> None:
        """
        Reset selected combo boxes to default values.

        If no fields are provided, reset all fields. Mark reset fields as invalid
        to show which parameters caused the loading error.
        """
        fields_to_reset = list(fields) if fields else list(QuestionParamsField)

        for field in fields_to_reset:
            match field:
                case QuestionParamsField.AMOUNT:
                    self.amount_cb.setCurrentIndex(0)
                    self._color_error_param_frame(self.amount_frame)
                case QuestionParamsField.DIFFICULTY:
                    self.difficulty_cb.setCurrentIndex(0)
                    self._color_error_param_frame(self.difficulty_frame)
                case QuestionParamsField.CATEGORY:
                    self.category_cb.setCurrentIndex(0)
                    self._color_error_param_frame(self.category_frame)
                case QuestionParamsField.QUESTION_TYPE:
                    self.type_cb.setCurrentIndex(0)
                    self._color_error_param_frame(self.type_frame)

    def _color_error_param_frame(self, frame: QFrame) -> None:
        """Mark a parameter frame as invalid."""
        frame.setProperty("paramState", "error")
        frame.style().unpolish(frame)
        frame.style().polish(frame)
        frame.update()

    def _reset_error_frames(self) -> None:
        for frame in self.frame_list:
            frame.setProperty("paramState", None)
            frame.style().unpolish(frame)
            frame.style().polish(frame)
            frame.update()
