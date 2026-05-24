import pytest
from pytestqt.qtbot import QtBot

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton

from modules.gui.widgets.start_display.components.start_button_widget import StartButtonWidget

@pytest.fixture
def start_button() -> StartButtonWidget:
    return StartButtonWidget()

def test_start_button_click_disables_button_and_emits_signal(qtbot: QtBot, start_button: StartButtonWidget) -> None:
    qtbot.addWidget(start_button)

    button = start_button.findChild(QPushButton, "startButton")
    assert button is not None

    with qtbot.waitSignal(start_button.start_button_pressed, timeout=100):
        qtbot.mouseClick(button, Qt.MouseButton.LeftButton)

    assert button.isEnabled() is False

def test_start_button_reenable_on_error(qtbot: QtBot, start_button: StartButtonWidget) -> None:
    qtbot.addWidget(start_button)

    button = start_button.findChild(QPushButton, "startButton")
    assert button is not None

    qtbot.mouseClick(button, Qt.MouseButton.LeftButton)
    assert button.isEnabled() is False

    start_button.on_error_returned()
    assert button.isEnabled() is True
