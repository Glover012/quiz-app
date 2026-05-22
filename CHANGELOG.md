# Changelog

## Unreleased

### Added
- GitHub Actions workflow for running unit tests
- README badges and project presentation updates
- Changelog file
- Widget screenshots and presentation page

### Changed
- Updated README project presentation and structure
- Refactored `Questions` to load question data explicitly with `load()` and updated app flow documentation
- Simplified model tests now Questions can be initialized normally
- Improve encapsulation in GUI modules

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