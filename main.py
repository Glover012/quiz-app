import sys, os
from PySide6.QtWidgets import QApplication
from modules import MainWindow

def main():
    """Main function to run the application."""
    app = QApplication(sys.argv)
    # Set CWD, so that relateive paths work correctly
    os.chdir(os.path.dirname(__file__)) 
    # Load and apply styles from styles.css to the entire application
    with open("modules/gui/styles/styles.css", "r") as file:
        app.setStyleSheet(file.read())
    # Create and show main window
    window = MainWindow()
    window.show() 
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
