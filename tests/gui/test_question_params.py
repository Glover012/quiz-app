from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture
from pytestqt.qtbot import QtBot

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton

from modules.gui.widgets.start_display.components.question_params_widget import QuestionParamsWidget, QuestionParams

def test_get_params(qtbot: QtBot, mocker: MockerFixture):
    question_params = QuestionParamsWidget()
    qtbot.add_widget(question_params)

    mocker.patch.object(question_params._amount_cb, "currentText", return_value="10")
    mocker.patch.object(question_params._difficulty_cb, "currentData", return_value="easy")
    mocker.patch.object(question_params._category_cb, "currentData", return_value="9")
    mocker.patch.object(question_params._type_cb, "currentData", return_value="boolean")

    expected_params_returned: QuestionParams =  {
            "amount": "10",
            "difficulty": "easy",
            "category": "9",
            "question_type": "boolean",
        }
    
    params = question_params.get_params()
    
    assert expected_params_returned == params

def test_get_get_params(qtbot: QtBot, mocker: MockerFixture):

    mocker.patch("modules.gui.widgets.start_display.components.question_params_widget.MIN_QUESTION_AMOUNT", new=1)
    mocker.patch("modules.gui.widgets.start_display.components.question_params_widget.MAX_QUESTION_AMOUNT", new=10)
    mocker.patch("modules.gui.widgets.start_display.components.question_params_widget.DIFFICULTIES", new={"easy": "easy"})
    mocker.patch("modules.gui.widgets.start_display.components.question_params_widget.CATEGORIES", new={"category": "category"})
    mocker.patch("modules.gui.widgets.start_display.components.question_params_widget.QUESTION_TYPES", new={"type": "type"})

    question_params = QuestionParamsWidget()
    qtbot.add_widget(question_params)

    params = question_params.get_params()

    expected_params_returned: QuestionParams =  {
        "amount": "1",
        "difficulty": "easy",
        "category": "category",
        "question_type": "type",
    }
    
    assert expected_params_returned == params
