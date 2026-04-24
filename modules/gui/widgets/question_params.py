from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QGridLayout, QWidget, QLabel,QPushButton, QComboBox
from PySide6.QtCore import Qt
from ...questions import Questions
from .question_display import QuestionDisplay

class QuestionParams(QWidget):
    def __init__(self, main_window : QMainWindow):
        super().__init__()
        self.main_window = main_window
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
        self.sb = QPushButton('Start')
        self.sb.setObjectName('startButton')
        sb_layout.addWidget(self.sb, alignment=Qt.AlignmentFlag.AlignCenter)
        self.sb.clicked.connect(self.startButtonClicked)
        self.main_layout.addWidget(sb_widget, alignment=Qt.AlignmentFlag.AlignCenter)
    
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

        # ComboBox data
        categories = {
            "Any Category": "",
            "General Knowledge": "9",
            "Entertainment: Books": "10",
            "Entertainment: Film": "11",
            "Entertainment: Music": "12",
            "Entertainment: Musicals & Theatres": "13",
            "Entertainment: Television": "14",
            "Entertainment: Video Games": "15",
            "Entertainment: Board Games": "16",
            "Science & Nature": "17",
            "Science: Computers": "18",
            "Science: Mathematics": "19",
            "Mythology": "20",
            "Sports": "21",
            "Geography": "22",
            "History": "23",
            "Politics": "24",
            "Art": "25",
            "Celebrities": "26",
            "Animals": "27",
            "Vehicles": "28",
            "Entertainment: Comics": "29",
            "Science: Gadgets": "30",
            "Entertainment: Japanese Anime & Manga": "31",
            "Entertainment: Cartoon & Animations": "32"}
        
        difficulties = {
            "Any dificulty": "", 
            "Easy": "easy", 
            "Medium": "medium", 
            "Hard": "hard"}
        
        types = {
            "Any type": "",
            "Multiple choice": "multiple",
            "True / False": "boolean"}
        
        numberList = [str(i) for i in range(2, 31)]
        self.amount_cb = QComboBox(); 
        self.amount_cb.addItems(numberList)

        self.cat_cb = QComboBox();
        for cat, id in categories.items():
            self.cat_cb.addItem(cat, id)

        self.diff_cb = QComboBox();
        for diff, id in difficulties.items():
            self.diff_cb.addItem(diff, id)

        self.tp_cb = QComboBox();
        for tp, id in types.items():
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
        print(f'Amount: {amount}, Difficulty: {diff}, Category: {cat}, Type: {tp}')

        # Init questions from API
        questions = Questions(qAmount=amount, qCategory=cat, qDifficulty=diff, qType=tp)
        q_list = questions.questionsList
        print(questions.questionsList)

        questionDisplay = QuestionDisplay(q_list)

        # Display questions
        self.main_window.displayWidget(questionDisplay)