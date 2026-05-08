"""OpenTDB API test response data. https://opentdb.com/api.php?amount=10"""

from typing import Any

QUESTION_TEST_DATA: dict[str, Any] = {
  "response_code": 0,
  "results": [
    {
      "type": "multiple",
      "difficulty": "hard",
      "category": "Entertainment: Video Games",
      "question": "In the Pok&eacute;mon series, what is Palkia&#039;s hidden ability?",
      "correct_answer": "Telepathy",
      "incorrect_answers": [
        "Pressure",
        "Water Bubble",
        "Hydration"
      ]
    },
    {
      "type": "multiple",
      "difficulty": "easy",
      "category": "General Knowledge",
      "question": "What is the profession of Elon Musk&#039;s mom, Maye Musk?",
      "correct_answer": "Model",
      "incorrect_answers": [
        "Professor",
        "Biologist",
        "Musician"
      ]
    },
    {
      "type": "multiple",
      "difficulty": "medium",
      "category": "Sports",
      "question": "What was Sir Donald Bradman&#039;s batting average in test matches?",
      "correct_answer": "99.94",
      "incorrect_answers": [
        "100",
        "69.51",
        "44.78"
      ]
    },
    {
      "type": "boolean",
      "difficulty": "easy",
      "category": "Politics",
      "question": "The 2016 United States Presidential Election is the first time Hillary Clinton has run for President.",
      "correct_answer": "False",
      "incorrect_answers": [
        "True"
      ]
    },
    {
      "type": "multiple",
      "difficulty": "easy",
      "category": "Animals",
      "question": "What is the name of a rabbit&#039;s abode?",
      "correct_answer": "Burrow",
      "incorrect_answers": [
        "Nest",
        "Den",
        "Dray"
      ]
    },
    {
      "type": "multiple",
      "difficulty": "hard",
      "category": "Science &amp; Nature",
      "question": "What is the most potent toxin known?",
      "correct_answer": "Botulinum toxin",
      "incorrect_answers": [
        "Ricin",
        "Cyanide",
        "Asbestos"
      ]
    },
    {
      "type": "multiple",
      "difficulty": "easy",
      "category": "Geography",
      "question": "Which US state is also known as the &quot;Lone Star State&quot;?",
      "correct_answer": "Texas",
      "incorrect_answers": [
        "Alabama",
        "Tennessee",
        "Kentucky"
      ]
    },
    {
      "type": "multiple",
      "difficulty": "medium",
      "category": "Entertainment: Comics",
      "question": "What is the real name of the &quot;Master Of Magnetism&quot; Magneto?",
      "correct_answer": "Max Eisenhardt",
      "incorrect_answers": [
        "Charles Xavier",
        "Pietro Maximoff",
        "Johann Schmidt"
      ]
    },
    {
      "type": "multiple",
      "difficulty": "medium",
      "category": "Geography",
      "question": "What is the capital of the US state Nevada?",
      "correct_answer": "Carson City",
      "incorrect_answers": [
        "Las Vegas",
        "Henderson",
        "Reno"
      ]
    },
    {
      "type": "multiple",
      "difficulty": "medium",
      "category": "Entertainment: Japanese Anime &amp; Manga",
      "question": "Which of these is not a world in the anime &quot;Buddyfight&quot;?",
      "correct_answer": "Ancient Dragon World",
      "incorrect_answers": [
        "Dragon World",
        "Star Dragon World",
        "Darkness Dragon World"
      ]
    }
  ]
}