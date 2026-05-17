# 🔄 Quiz App - Data Flow

This document shows how data moves through the application. `MainWindow` acts as the central coordinator: it owns the main layout, switches between screens, starts background loading, and routes success or error signals back to the GUI.

## 🚀 Table of Contents
- [🔄 Quiz App - Data Flow](#-quiz-app---data-flow)
  - [🚀 Table of Contents](#-table-of-contents)
  - [🔎 Simplified Application Flow](#-simplified-application-flow)
  - [🧩 Detailed Application Flow](#-detailed-application-flow)
  - [📘 Description](#-description)

## 🔎 Simplified Application Flow
```mermaid
flowchart LR
    Main["main.py"]
    Window["MainWindow"]
    Start["StartDisplay"]
    Loader["QuestionLoader"]
    Data["Questions + OpenTriviaClient"]
    API["OpenTDB API"]
    Display["QuestionDisplay"]
    Result["ResultWidget"]
    Error["ErrorOverlay"]

    Main --> Window
    Window --> Start
    Start -->|"QuestionParams"| Window
    Window -->|"starts background loading"| Loader
    Loader --> Data
    Data --> API
    API --> Data
    Data --> Loader
    Loader -->|"loaded questions"| Window
    Window --> Display
    Display --> Result
    Loader -->|"error"| Window
    Window --> Error
    Window -->|"returns to setup"| Start
```

## 🧩 Detailed Application Flow
```mermaid
flowchart LR
    subgraph Startup["Application startup"]
        Main["main.py"]
        App["QApplication"]
        Logging["Logging config"]
        Styles["styles.css"]
        Window["MainWindow"]
    end

    subgraph Navigation["Navigation and layout"]
        MenuBar["MenuBar"]
        QuizMenu["QuizMenu"]
        HelpMenu["HelpMenu"]
        Welcome["WelcomeLabel"]
        Stack["QStackedLayout"]
    end

    subgraph Setup["Quiz setup"]
        Start["StartDisplay"]
        StartButton["StartButtonWidget"]
        Params["QuestionParamsWidget"]
        ParamFrames["ParamFrame widgets"]
        QuestionParams["QuestionParams"]
    end

    subgraph Loading["Background question loading"]
        Controller["WorkerThreadController"]
        Thread["QThread"]
        Loader["QuestionLoader"]
        LoadingOverlay["LoadingOverlay"]
    end

    subgraph Data["Question data layer"]
        Questions["Questions"]
        Question["Question objects"]
        Client["OpenTriviaClient"]
        ApiParams["api_params.py"]
        API["OpenTDB API"]
    end

    subgraph Quiz["Quiz display and scoring"]
        Display["QuestionDisplay"]
        QuestionWidgets["QuestionWidget list"]
        AnswerButtons["QRadioButton answers"]
        Result["ResultWidget"]
        Repeat["Repeat Quiz"]
    end

    subgraph Errors["Error handling"]
        ErrorOverlay["ErrorOverlay"]
        NoQuestions["NoQuestionsFoundError"]
        NotEnough["NotEnoughQuestionsError"]
        ClientError["OpenTriviaClientError"]
    end

    Main --> App
    Main --> Logging
    Main --> Styles
    Main --> Window

    Window --> Stack
    Window --> MenuBar
    Window --> Welcome
    MenuBar --> QuizMenu
    MenuBar --> HelpMenu
    QuizMenu -->|"Start Quiz"| Window
    QuizMenu -->|"Exit"| Window
    HelpMenu -->|"About"| Window

    Window -->|"shows setup"| Start
    Start --> StartButton
    Start --> Params
    Params --> ParamFrames
    Params --> ApiParams
    StartButton -->|"clicked"| Start
    Start -->|"reads selected values"| Params
    Params -->|"returns"| QuestionParams
    Start -->|"start_quiz_requested"| Window

    Window -->|"creates"| Loader
    Window -->|"creates"| Controller
    Controller --> Thread
    Thread -->|"runs"| Loader
    Controller -->|"started / finished"| LoadingOverlay

    Loader -->|"creates"| Questions
    Questions -->|"uses"| Client
    Client -->|"HTTP request"| API
    API -->|"JSON response"| Client
    Client -->|"API response"| Questions
    Questions -->|"builds"| Question
    Questions -->|"stores questions_list"| Loader

    Loader -->|"loaded"| Window
    Window -->|"passes questions_list"| Display
    Display -->|"creates"| QuestionWidgets
    QuestionWidgets --> AnswerButtons
    AnswerButtons -->|"selected answer"| QuestionWidgets
    QuestionWidgets -->|"answer state"| Display
    Display -->|"calculates score"| Result
    Display -->|"repeat_button_clicked"| Repeat
    Repeat --> Window

    Client --> NoQuestions
    Client --> NotEnough
    Client --> ClientError
    Loader -->|"error"| Window
    Controller -->|"thread_error"| Window
    Window -->|"shows"| ErrorOverlay
    Window -->|"returns error"| Start
    Start -->|"marks or resets params"| Params
```

## 📘 Description
The application data flow is organized around `MainWindow`:

1. `main.py`
   - creates the `QApplication`,
   - configures logging,
   - loads the stylesheet,
   - creates and displays `MainWindow`.

2. `MainWindow`
   - owns the main stacked layout,
   - displays the welcome screen and `StartDisplay`,
   - creates loading and error overlays,
   - coordinates question loading and screen changes.

3. `StartDisplay`
   - contains the start button and `QuestionParamsWidget`,
   - reads selected quiz parameters from `QuestionParamsWidget`,
   - emits `start_quiz_requested` with `QuestionParams`.

4. Question loading
   - `MainWindow` receives `QuestionParams`,
   - creates `QuestionLoader`,
   - starts it in a background `QThread` through `WorkerThreadController`,
   - shows `LoadingOverlay` while questions are loading.

5. Data fetching and conversion
   - `QuestionLoader` creates `Questions`,
   - `Questions` calls `OpenTriviaClient`,
   - `OpenTriviaClient` requests data from the OpenTDB API,
   - API response data is converted into `Question` objects.

6. Question display and scoring
   - `QuestionLoader` emits loaded `Questions`,
   - `MainWindow` creates `QuestionDisplay`,
   - `QuestionDisplay` creates one `QuestionWidget` per question,
   - user answers are stored in each `QuestionWidget`,
   - after finishing the quiz, `QuestionDisplay` calculates the score,
   - `ResultWidget` displays the final result.

7. Error handling
   - loading or API errors are emitted back to `MainWindow`,
   - `MainWindow` shows `ErrorOverlay`,
   - `StartDisplay` receives the error and marks or resets invalid parameters when possible.
