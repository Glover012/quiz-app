from PySide6.QtWidgets import QVBoxLayout, QFrame, QLabel
from PySide6.QtCore import Qt


class ResultWidget(QFrame):
    """Widget to display quiz results."""

    def __init__(
            self, 
            question_amount: int, 
            total_question_points: int, 
            user_points: int, 
            user_good_answers: int
            ) -> None:
        super().__init__()
        self.setObjectName('resultWidgetFrame')
        self._setup_layout()
        self._question_amount = question_amount
        self._total_question_points = total_question_points
        self._user_points = user_points
        self._user_good_answers = user_good_answers
        self._display_results()

    def _setup_layout(self) -> None:
        self._main_layout = QVBoxLayout()
        self._main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self._main_layout)
    
    def _display_results(self) -> None:
        """Display quiz results."""
        quiz_result_label = QLabel("Results", alignment=Qt.AlignmentFlag.AlignCenter)
        quiz_result_label.setObjectName('quizResultLabel')

        user_good_answers_label = QLabel(
            f'Good answers - {self._user_good_answers}/{self._question_amount}',
            alignment=Qt.AlignmentFlag.AlignCenter
            )
        user_good_answers_label.setObjectName('userGoodAnswersLabel')
        
        score = (
            f'Score - {self._user_points}/{self._total_question_points} points. '
            f'{(self._user_points/float(self._total_question_points*0.01)):.2f}%'
            )
        quiz_score_label = QLabel(score, alignment=Qt.AlignmentFlag.AlignCenter)
        quiz_score_label.setObjectName('quizScoreLabel')

        self._main_layout.addWidget(quiz_result_label)
        self._main_layout.addWidget(quiz_score_label)
        self._main_layout.addWidget(user_good_answers_label)
