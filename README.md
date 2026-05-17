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
  - [🔄 Application data flow](#-application-data-flow)
  - [📌 Project status](#-project-status)
  - [🛣 Roadmap](#-roadmap)
  - [🧪 Tests](#-tests)
      - [💻 Running tests in Windows PowerShell](#-running-tests-in-windows-powershell)
  - [⚠️ Error triggers](#️-error-triggers)
    - [🚨 Error Trigger Table](#-error-trigger-table)
  - [📄 License](#-license)
  - [👤 Author contact](#-author-contact)
  - [⭐ Support](#-support)

## ✨ Features
- GUI built with PySide6
- Threaded question loading from the Open Trivia Database API
- Selectable number of questions, category, difficulty and question type
- Score calculation based on question difficulty
- Visual feedback based on the user's answer
- Loading overlay while questions are being fetched
- Error overlay with user-facing error messages
- Visual feedback when a particular question parameter causes an error
- Per-session file logging

## 🎬 Demo
![Quiz App Demo](docs/quiz-app-demo.gif)

## 📘 About the project
This project was created as a learning exercise and my first complete desktop GUI application in Python.

It started as a simple console quiz made during a Python course. Later, I expanded it with a graphical interface, API integration, logging, error handling, stylesheets, type hints and a cleaner project structure.

During development, I focused on:
- Building a GUI with PySide6
- Working with external API data
- Improving code organization
- Maintaining clean internal documentation
- Following PEP 8 standards

The application allows selecting up to 100 questions, even though the Open Trivia Database API documentation states that up to 50 questions can be requested at once. This is intentional and is used to trigger error handling paths.

## 📋 Requirements
- Python 3.11+
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

Supported logging level values:

- `DEBUG`
- `INFO`
- `WARNING`

The application also writes per-session log files to the `logs/` directory and keeps the most recent log files.

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
    ├── docs/                         # Demo and application data flow
    ├── modules/                      # Application source code
    │   ├── gui/                      # PySide6 GUI layer
    │   │   ├── menu_bar/             # Application menu bar
    │   │   │   └── menus/
    │   │   ├── styles/               # Qt stylesheet file
    │   │   ├── widgets/              # GUI widgets
    │   │   │   ├── overlays/         # Loading and error overlays
    │   │   │   ├── question_display/ # Quiz question display screen
    │   │   │   │   └── components/
    │   │   │   └── start_display/    # Quiz setup/start screen
    │   │   │       └── components/
    │   │   └── workers/              # Background worker and thread controller
    │   └── questions/                # Quiz data, API parameters and OpenTDB client
    ├── tests/                        # Unit tests and test API data
    ├── main.py                       # Application entry point
    ├── requirements.txt
    ├── README.md
    └── LICENSE

## 🔄 Application data flow
The application data flow is described in [docs/application-data-flow.md](docs/application-data-flow.md).

## 📌 Project status
The application is functional. The main planned improvement is adding GUI logic tests.

## 🛣 Roadmap
Planned improvements:
- [x] Initial basic version
- [x] Unit tests
- [x] Refactor application flow to use Qt signals
- [x] Move question loading out of the GUI layer into a dedicated thread
- [x] Add loading overlay
- [x] Add file logging
- [ ] Refactor the Questions model so its constructor does not immediately load questions from the API
- [ ] Add GUI logic tests

## 🧪 Tests
The application includes unit tests for the question models, the OpenTDB API client, and API error handling.

#### 💻 Running tests in Windows PowerShell
```powershell
cd quiz-app
python -m unittest discover -s tests
```

## ⚠️ Error triggers
Some OpenTDB parameter combinations may return too few questions or no questions at all, which may be used to exercise the application's error handling flow.

### 🚨 Error Trigger Table
| Amount | Difficulty | Category | Type | Expected error |
| --- | --- | --- | --- | --- |
| 51-100 | Any difficulty | Any Category | Any type | Not enough questions found |
| 2 | Hard | Entertainment: Musicals & Theatres | True / False | No questions found |

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
