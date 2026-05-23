from pytestqt.qtbot import QtBot

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton

from modules.gui.widgets.start_display.components.start_button_widget import StartButtonWidget

def test_start_button_click_disables_button_and_emits_signal(qtbot: QtBot) -> None:
    widget = StartButtonWidget() 
    qtbot.addWidget(widget)

    button = widget.findChild(QPushButton, "startButton")
    assert button is not None

    with qtbot.waitSignal(widget.start_button_pressed, timeout=100):
        qtbot.mouseClick(button, Qt.MouseButton.LeftButton)

    assert button.isEnabled() is False
