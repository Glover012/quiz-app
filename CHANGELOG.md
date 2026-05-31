# Changelog

## Unreleased

### Added
- Pytest-cov dependency for local test coverage reporting

### Changed
- Updated README project overview, learning notes and technical presentation
- Updated test coverage badge
- Documented the PowerShell command for running tests with coverage
- Added generated coverage artifacts to `.gitignore`

## v1.2.0

### Added
- GitHub Actions workflow for running unit tests
- README badge and project presentation updates
- Changelog file
- Widget screenshots and presentation page
- Pytest backend tests for question models and the OpenTDB client
- Pytest-qt GUI tests for core widgets, signal wiring, loading states, error handling, quiz flow and MainWindow coordination
- Pytest configuration for the main backend and GUI test suites
- Pytest, pytest-mock and pytest-qt test dependencies

### Changed
- Updated README project presentation and structure
- Refactored `Questions` to load question data explicitly with `load()` and updated app flow documentation
- Simplified model tests now Questions can be initialized normally
- Improved encapsulation in GUI modules
- Updated GitHub Actions workflow to run pytest-based tests
- Reorganized test files into backend, GUI and shared static API response data directories

## v1.1.0

### Added
- Threaded question loading with QuestionLoader, WorkerThreadController and QThread
- Loading and error overlays
- Per-session file logging
- Application data flow documentation with Mermaid diagrams
- Additional and updated unit tests for question models and the OpenTDB client

### Changed
- Refactored GUI flow to use Qt signals
- Improved OpenTDB error handling and invalid quiz parameter feedback
- Improved application shutdown handling while question loading is running
- Improved answer checking and answer highlighting
- Improved type hints and docstrings across the application
- Updated README, demo GIF and project structure documentation
- Pinned dependency versions in requirements.txt

## v1.0.0

### Added
- Initial PySide6 desktop GUI
- OpenTDB API question loading
- Quiz setup screen
- Question display screen
- Result screen
- Visual feedback based on the user's answer
- Basic documentation and MIT license
