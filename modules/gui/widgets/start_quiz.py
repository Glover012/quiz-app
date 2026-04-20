from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QGridLayout, QWidget, QLabel,QPushButton, QComboBox
from PySide6.QtCore import Qt
from numpy import number

class StartQuiz(QWidget):
    def __init__(self):
        super().__init__()
        self.__initLayout()
        self.displayWidgets()

    def __initLayout(self):
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

    def displayWidgets(self):
        self.main_layout.addWidget(AppName())
        self.main_layout.addWidget(QuestionParams())

class AppName(QWidget):
    def __init__(self):
        super().__init__()
        self.__initLayout()
        self.displayAppName()

    def __initLayout(self):
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

    def displayAppName(self):
        app_name = QLabel('Quiz App')
        app_name.setStyleSheet('''
                        font-size: 40px;
                        font-weight: bold;
                        font-family: Arial;
                        border-radius: 10px;
                        ''')
        self.main_layout.addWidget(app_name, alignment=Qt.AlignmentFlag.AlignCenter)

class QuestionParams(QWidget):
    def __init__(self):
        super().__init__()
        self.__initLayout()
        self.startButtonWidget()
        self.paramsWidget()

    def __initLayout(self):
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

    def startButtonWidget(self):
        sb_widget = QWidget()
        sb_layout = QVBoxLayout()
        sb_widget.setLayout(sb_layout)
        sb = QPushButton('Start')
        sb.setStyleSheet('''
                         font-size: 30px;
                         font-family: Arial;
                         ''')
        sb_layout.addWidget(sb, alignment=Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(sb_widget, alignment=Qt.AlignmentFlag.AlignCenter)
    
    def paramsWidget(self):
        params_widget = QWidget()
        params_layout = QGridLayout()
        params_widget.setLayout(params_layout)

        # questionAmount = QLabel('Amount')
        # questionDifficulty = QLabel('Difficulty')
        # questionCategory = QLabel('Category')
        # questionType = QLabel('Type')

        params_layout.addWidget(QLabel('Amount'), 0, 0)
        params_layout.addWidget(QLabel('Difficulty'), 0, 1)
        params_layout.addWidget(QLabel('Category'), 0, 2)
        params_layout.addWidget(QLabel('Type'), 0, 3)

        numberList = [str(i+1) for i in range(20)]
        amount_cb = QComboBox(); amount_cb.addItems(numberList)
        diff_cb = QComboBox(); diff_cb.addItems(['Easy', 'Medium', 'Hard'])
        cat_cb = QComboBox(); cat_cb.addItems(['General', 'Cars', 'Football'])
        tp_cb = QComboBox(); tp_cb.addItems(['Multiple-choice', 'True/False'])

        params_layout.addWidget(amount_cb, 1, 0)
        params_layout.addWidget(diff_cb, 1, 1)
        params_layout.addWidget(cat_cb, 1, 2)
        params_layout.addWidget(tp_cb, 1, 3)

        self.main_layout.addWidget(params_widget, alignment=Qt.AlignmentFlag.AlignCenter)