import requests, html, random

# Questions
class Question:
    def __init__(self, tp, difficulty, category, question, correct_answer, incorrect_answers, all_answers, points):
        self.tp = tp
        self.difficulty = difficulty
        self.category = category
        self.question = question
        self.correct_answer = correct_answer
        self.incorrect_answers = incorrect_answers
        self.points = points
        self.all_answers = all_answers

class Questions:
    questionsList = []

    def __init__(self, qAmount="1", qCategory="", qDifficulty="", qType="" ):
        # https://opentdb.com/api.php?amount=10&category=9&difficulty=easy&type=boolean
        self.qAmount = str(qAmount)
        self.qCategory = str(qCategory)
        self.qDifficulty = str(qDifficulty).lower()
        self.qType = str(qType).lower()
        self.url = f"https://opentdb.com/api.php?amount={self.qAmount}{f"&category={self.qCategory}" if self.qCategory != "" else ""}{f"&difficulty={self.qDifficulty}" if self.qDifficulty != "" else ""}{f"&type={self.qType}" if self.qType != "" else ""}"
        print(self.url)
        # Methods
        self.questionsData = self.getQuestionsDataFromApi(self.url)
        self.questionsDataToObjects(self.questionsData)

    def getQuestionsDataFromApi(self, url):
        "Get questions JSON data from API"
        response = requests.get(url)
        if response.ok == True:
            questionsData = response.json()
        return questionsData

    def questionsDataToObjects(self, questionsData):
        "Question JSON data from API to Question objects. Add q objects to questionsList"
        for questionParams in questionsData["results"]:
            # Question parameters to variables - possibly good, in case of further modyfications
            tp = questionParams["type"]
            difficulty = questionParams["difficulty"]
            category = questionParams["category"]
            question = html.unescape(questionParams["question"])
            correct_answer = html.unescape(questionParams["correct_answer"])
            incorrect_answers = [html.unescape(x) for x in questionParams["incorrect_answers"]]

            # Such thing is required to avoid cosmetic issue, when some answers display True, then False, and some False, then True due to random.shuffle
            if tp == "boolean":
                all_answers = ["True", "False"]
            else:
                all_answers = incorrect_answers.copy()
                all_answers.append(correct_answer)
                random.shuffle(all_answers)

            # Assign points for question, based on difficulty
            if difficulty == "hard": points = 3
            elif  difficulty == "medium": points = 2
            elif  difficulty == "easy": points = 1

            # Add Question object, to questionsList
            self.questionsList.append(Question(tp, difficulty, category, question, correct_answer, incorrect_answers, all_answers, points))
