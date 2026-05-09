# 🎯 Quiz App
A simple quiz application built in Python with a PySide6 GUI.

## 🚀 Table of contents
- [🎯 Quiz App](#-quiz-app)
  - [🚀 Table of contents](#-table-of-contents)
  - [✨ Features](#-features)
  - [🎬 Demo](#-demo)
  - [📘 About the project](#-about-the-project)
  - [📋 Requirements](#-requirements)
  - [⚙️ Installation](#️-installation)
      - [💻 Windows PowerShell](#-windows-powershell)
  - [🔧 Configuration](#-configuration)
      - [💻 Logging level in Windows PowerShell](#-logging-level-in-windows-powershell)
  - [▶️ Running app](#️-running-app)
  - [🗂️ Project structure](#️-project-structure)
  - [📌 Project status](#-project-status)
  - [🛣 Roadmap](#-roadmap)
  - [🧪 Tests](#-tests)
      - [💻 Running tests in Windows PowerShell](#-running-tests-in-windows-powershell)
  - [📄 License](#-license)
  - [👤 Author contact](#-author-contact)
  - [⭐ Support](#-support)

## ✨ Features
- GUI built with PySide6
- Questions loaded from the Open Trivia Database API
- Selectable number of questions, category, difficulty and question type
- Score calculation based on question difficulty
- Visual feedback based on the user's answer

## 🎬 Demo
![Quiz App Demo](docs/quiz-app-demo.gif)

## 📘 About the project
This project was created as a learning exercise and my first complete desktop GUI application in Python.

It started as a simple console quiz made during a Python course. Later, I expanded it with a graphical interface, API integration, logging, error handling, stylesheets, type hints and a cleaner project structure.

During development, I focused on:
- Building a GUI with PySide6
- Working with external API data
- Improving code organization
- Replacing debug prints with logging
- Following PEP 8 standards
- Adding type hints and docstrings

## 📋 Requirements
- Python 3.10+
- Internet connection for loading questions from the API

## ⚙️ Installation
Clone the repository and install the required dependencies in a virtual environment.

#### 💻 Windows PowerShell
```powershell
git clone https://github.com/Glover012/quiz-app.git
cd quiz-app
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## 🔧 Configuration
The project uses an environment variable to control the logging level.

Supported values:

- `DEBUG`
- `INFO`
- `WARNING`

#### 💻 Logging level in Windows PowerShell
```powershell
$env:QUIZ_APP_LOG_LEVEL="DEBUG"
```

## ▶️ Running app
```powershell
python main.py
```

## 🗂️ Project structure
    quiz-app/
    ├── docs/
    │   └── quiz-app-demo.gif
    ├── modules/
    │   ├── gui/ # GUI elements and styles
    │   └── questions/ # API data handling
    ├── main.py
    ├── requirements.txt
    ├── LICENSE
    └── README.md

## 📌 Project status
The application is functional. The main planned improvement is adding unit tests.

## 🛣 Roadmap
Planned improvements:
- [x] Initial basic version
- [x] Unit tests

## 🧪 Tests
The application includes unit tests for the question models, the OpenTDB API client, and API error handling.

#### 💻 Running tests in Windows PowerShell
```powershell
cd quiz-app
python -m unittest discover -s tests
```

## 📄 License
This project is licensed under the MIT License. See the `LICENSE` file for more information.

## 👤 Author contact
- GitHub: https://github.com/Glover012
- E-mail: glover012-git@protonmail.com

## ⭐ Support
If you like this project, you can:
- Leave a star on GitHub
- Report an issue
- Suggest a new feature