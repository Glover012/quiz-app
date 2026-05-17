# Quiz App - Data Flow

## Diagram
```mermaid
flowchart TD
    Main["main.py"]
    Window["MainWindow"]
    Start["StartDisplay"]
    Params["QuestionParamsWidget"]
    WorkerController["WorkerThreadController"]
    Loader["QuestionLoader"]
    Questions["Questions"]
    Client["OpenTriviaClient"]
    API["OpenTDB API"]
    Display["QuestionDisplay"]
    QuestionWidgets["QuestionWidget list"]
    Result["ResultWidget"]
    Loading["LoadingOverlay"]
    Error["ErrorOverlay"]

    Main -->|"creates QApplication<br/>configures logging<br/>loads styles"| Window

    Window -->|"shows setup screen"| Start
    Start -->|"reads selected params"| Params
    Params -->|"QuestionParams"| Start
    Start -->|"start_quiz_requested"| Window

    Window -->|"creates worker and thread controller"| WorkerController
    WorkerController -->|"runs in QThread"| Loader
    WorkerController -->|"thread_started / thread_finished"| Loading

    Loader -->|"creates"| Questions
    Questions -->|"uses"| Client
    Client -->|"HTTP request"| API
    API -->|"JSON response"| Client
    Client -->|"parsed API data"| Questions
    Questions -->|"Question objects"| Loader

    Loader -->|"loaded(Questions)"| Window
    Window -->|"passes questions_list"| Display
    Display -->|"creates"| QuestionWidgets
    QuestionWidgets -->|"selected answers"| Display
    Display -->|"calculates score"| Result

    Loader -->|"error(Exception)"| Window
    WorkerController -->|"thread_error(Exception)"| Window
    Window -->|"shows user message"| Error
    Window -->|"returns error to setup screen"| Start
```

## Description
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
