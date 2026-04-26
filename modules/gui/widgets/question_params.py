from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..main_window import MainWindow

from PySide6.QtWidgets import QVBoxLayout, QGridLayout, QWidget, QLabel,QPushButton, QComboBox
from PySide6.QtCore import Qt, QTimer
from ...questions import Questions, CATEGORIES, DIFFICULTIES, QUESTION_TYPES, OpenTriviaClientError
from .question_display import QuestionDisplay

class QuestionParams(QWidget):
    def __init__(self, main_window: MainWindow):
        super().__init__()
        self.main_window = main_window
        self.__initLayout()
        self.startButtonWidget()
        self.add_error_label()
        self.paramsWidget()

    def __initLayout(self):
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

    def startButtonWidget(self):
        sb_widget = QWidget()
        sb_layout = QVBoxLayout()
        sb_widget.setLayout(sb_layout)
        self.sb = QPushButton('Start')
        self.sb.setObjectName('startButton')
        sb_layout.addWidget(self.sb, alignment=Qt.AlignmentFlag.AlignCenter)
        self.sb.clicked.connect(self.startButtonClicked)
        self.main_layout.addWidget(sb_widget, alignment=Qt.AlignmentFlag.AlignCenter)

    def add_error_label(self):
        self.error_label = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)
        self.error_label.setObjectName('errorLabel')
        # Set size policy, to avoid widets movement on the screen when error label shows up
        size_policy = self.error_label.sizePolicy()
        size_policy.setRetainSizeWhenHidden(True)
        self.error_label.setSizePolicy(size_policy)
        self.error_label.hide()
        self.main_layout.addWidget(self.error_label)

    def show_error(self, error: OpenTriviaClientError):
        self.error_label.setText(f'API Error - {error}')
        self.error_label.show()
        # Hide label after 3 seconds
        QTimer.singleShot(3000, self.error_label.hide)
    
    def paramsWidget(self):
        select_params_label = QLabel('Select quiz parameters')
        select_params_label.setObjectName('selectParamsLabel')
        self.main_layout.addWidget(select_params_label, alignment=Qt.AlignmentFlag.AlignCenter)

        params_widget = QWidget()
        params_layout = QGridLayout()
        params_widget.setLayout(params_layout)

        params_layout.addWidget(QLabel('Amount'), 0, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        params_layout.addWidget(QLabel('Difficulty'), 0, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        params_layout.addWidget(QLabel('Category'), 0, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        params_layout.addWidget(QLabel('Type'), 0, 3, alignment=Qt.AlignmentFlag.AlignCenter)

        min_amout = 2
        max_amount = 30
        questionAmountList = [str(i) for i in range(min_amout, max_amount + 1)]
        self.amount_cb = QComboBox(); 
        self.amount_cb.addItems(questionAmountList)

        self.cat_cb = QComboBox();
        for cat, id in CATEGORIES.items():
            self.cat_cb.addItem(cat, id)

        self.diff_cb = QComboBox();
        for diff, id in DIFFICULTIES.items():
            self.diff_cb.addItem(diff, id)

        self.tp_cb = QComboBox();
        for tp, id in QUESTION_TYPES.items():
            self.tp_cb.addItem(tp, id)

        params_layout.addWidget(self.amount_cb, 1, 0)
        params_layout.addWidget(self.diff_cb, 1, 1)
        params_layout.addWidget(self.cat_cb, 1, 2)
        params_layout.addWidget(self.tp_cb, 1, 3)

        self.main_layout.addWidget(params_widget, alignment=Qt.AlignmentFlag.AlignCenter)

    def startButtonClicked(self):
        amount = self.amount_cb.currentText()
        diff = self.diff_cb.currentData()
        cat = self.cat_cb.currentData()
        tp = self.tp_cb.currentData()
        # print(f'Amount: {amount}, Difficulty: {diff}, Category: {cat}, Type: {tp}')

        # Load questions from API client
        try:
            questions = Questions(amount=amount, category=cat, difficulty=diff, question_type=tp)
            self.main_window.displayWidget(QuestionDisplay(questions.questions_list))
        except OpenTriviaClientError as error:
            self.show_error(error)
