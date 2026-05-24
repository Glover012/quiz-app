"""OpenTDB parameter values used by the quiz setup UI."""

MIN_QUESTION_AMOUNT: int = 2
MAX_QUESTION_AMOUNT: int = 100 # API can handle <= 50, 100 is for testing error routes

CATEGORIES: dict[str, str] = {
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

DIFFICULTIES: dict[str, str] = {
    "Any difficulty": "",
    "Easy": "easy",
    "Medium": "medium",
    "Hard": "hard"}

QUESTION_TYPES: dict[str, str] = {
    "Any type": "",
    "Multiple choice": "multiple",
    "True / False": "boolean"}
