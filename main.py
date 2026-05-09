import logging
import os
import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont

from modules import MainWindow

logger = logging.getLogger(__name__)

def configure_logging() -> None:
    log_level = os.getenv("QUIZ_APP_LOG_LEVEL", "INFO").upper()

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )

def main() -> None:
    """Start Qt based application."""
    # Set up logging
    configure_logging()
    logger.info("Starting Quiz-App")
    
    app = QApplication(sys.argv)
    # Set global font
    font = QFont("Inter", 12)
    app.setFont(font)
    # Set CWD, so that relative paths work correctly
    os.chdir(os.path.dirname(__file__))
    logger.debug("Set CWD to %s", os.getcwd())

    # Load and apply styles from styles.css to the entire application
    stylesheet_path = "modules/gui/styles/styles.css"
    with open(stylesheet_path, "r") as file:
        app.setStyleSheet(file.read())
    logger.debug("App stylesheet loaded from: %s", stylesheet_path)

    # Create and show main window
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
