from unittest.mock import call

import pytest
from pytest_mock import MockerFixture
from pytestqt.qtbot import QtBot

from PySide6.QtWidgets import QFrame, QComboBox

from modules.gui.widgets.start_display.components import question_params_widget as qpw
from modules.questions import QUESTION_AMOUNT, DIFFICULTIES, CATEGORIES, QUESTION_TYPES
from modules.gui.widgets.start_display.components.question_params_widget import QuestionParamsWidget, QuestionParams, QuestionParamsField

@pytest.fixture
def question_params_widget(monkeypatch) -> QuestionParamsWidget:
    """
    Prepares QuestionParamsWidget fixture for testing. 
    Mock API params, for comparison purposes.
    """
    # Mock API params that are loaded in question_params_widget module
    monkeypatch.setattr(qpw, "QUESTION_AMOUNT", 3)
    monkeypatch.setattr(
        qpw,
        "DIFFICULTIES", 
        {"diff1": "diff1", "diff2": "diff2", "diff3": "diff3"}
        )
    monkeypatch.setattr(
        qpw, 
        "CATEGORIES", 
        {"cat1": "cat1", "cat2": "cat2", "cat3": "cat3"}
        )
    monkeypatch.setattr(
        qpw, 
        "QUESTION_TYPES", 
        {"type1": "type1", "type2": "type2", "type3": "type3"}
        )
    question_params_widget = QuestionParamsWidget()
    return question_params_widget

# Fixtures for some widget elements and fileds. 
# Do not change order.
@pytest.fixture
def comboboxes(question_params_widget) -> list[QComboBox]:
    """List of widget fixture comboboxes."""
    comboboxes = [
        question_params_widget._amount_cb,
        question_params_widget._difficulty_cb,
        question_params_widget._category_cb,
        question_params_widget._type_cb,
    ]
    return comboboxes

# Do not change order.
@pytest.fixture
def frames(question_params_widget) -> list[QFrame]:
    """
    List of widget fixture frames. 
    Same frames are also stored in _frame_list.
    """
    frames = [
        question_params_widget._amount_frame,
        question_params_widget._difficulty_frame,
        question_params_widget._category_frame,
        question_params_widget._type_frame,
    ]
    return frames

# Do not change order.
@pytest.fixture
def fields() -> list[QuestionParamsField]:
    """List of widget fields."""
    fields = [
        QuestionParamsField.AMOUNT,
        QuestionParamsField.DIFFICULTY,
        QuestionParamsField.CATEGORY,
        QuestionParamsField.QUESTION_TYPE,
    ]
    return fields

def test_api_params_data_loaded_into_all_comboboxes(qtbot: QtBot) -> None:
    """
    Test and confirms that all API params data, from api_params module, are properly loaded into comboboxes data.
    """
    question_params_w = QuestionParamsWidget()
    qtbot.addWidget(question_params_w)
    cbs = [
        question_params_w._amount_cb,
        question_params_w._difficulty_cb,
        question_params_w._category_cb,
        question_params_w._type_cb,
        ]

    # Amount param has to be synthesised, in order to achieve structure simillar to other params -> dict[str, str]
    amount = {str(i): str(i) for i in range(1, QUESTION_AMOUNT + 1)}
    api_params = [
        amount,
        DIFFICULTIES,
        CATEGORIES,
        QUESTION_TYPES,
    ]

    for cb, param in zip(cbs, api_params, strict=True):
        assert cb.count() == len(param)
        i = 0
        for text, data in param.items():
            assert cb.itemText(i) == text
            assert cb.itemData(i) == data
            i += 1

def test_all_params_are_in_frames(qtbot: QtBot) -> None:
    """
    Test that all question params frames in _frame_list are of QFrame instance.
    """
    question_params_widget = QuestionParamsWidget()
    qtbot.addWidget(question_params_widget)

    assert len(question_params_widget._frame_list) == 4
    assert all(isinstance(param, QFrame) for param in question_params_widget._frame_list)

def test_reset_error_frames(
        qtbot: QtBot, 
        question_params_widget: QuestionParamsWidget,
        frames,
        ) -> None:
    """
    Test _reset_error_frames method:
    - change frame paramState property back to None 
    for all frames in _frame_list.
    """
    qtbot.addWidget(question_params_widget)

    for frame in frames:
        frame.setProperty("paramState", "test")
        assert frame.property("paramState") == "test"

    # Reset frames
    question_params_widget._reset_error_frames()

    for frame in frames:
        assert frame.property("paramState") is None

def test_get_params(
        qtbot: QtBot,
        question_params_widget: QuestionParamsWidget,
        ) -> None:
    """
    Test get_params method: 
    - Returned params correspond to expected mocked values of API params
    """
    qtbot.addWidget(question_params_widget)

    params = question_params_widget.get_params()

    expected_params_returned: QuestionParams =  {
        "amount": "1",
        "difficulty": "diff1",
        "category": "cat1",
        "question_type": "type1",
    }

    assert expected_params_returned == params

def test_get_params_calls_reset(
        qtbot: QtBot, 
        question_params_widget: QuestionParamsWidget, 
        mocker: MockerFixture
        ) -> None:
    """
    Test get_params method: 
    - calls _reset_error_frames
    """
    qtbot.addWidget(question_params_widget)

    reset_error_frames = mocker.spy(question_params_widget, "_reset_error_frames")

    question_params_widget.get_params()

    reset_error_frames.assert_called_once()

def test_color_error_param_frame_in_all_frames(
    qtbot: QtBot, 
    question_params_widget: QuestionParamsWidget
    ) -> None:
    """
    Test _color_error_param_frame merthod:
    - change paramState property to error in all frames
    """
    qtbot.addWidget(question_params_widget)

    frame_list = question_params_widget._frame_list

    # Check defualt property
    for frame in frame_list:
        assert frame.property("paramState") is None

    for frame in frame_list:
        question_params_widget._color_error_param_frame(frame)
        assert frame.property("paramState") == "error"

def test_color_error_param_frame_in_selected_frame(
        qtbot: QtBot, 
        question_params_widget: QuestionParamsWidget,
        frames,
        ) -> None:
    """
    Test _color_error_param_frame merthod:
    - change paramState property to error only in selected frame
    """
    qtbot.addWidget(question_params_widget)

    # Check defualt property
    for frame in frames:
        assert frame.property("paramState") is None

    for selected_frame in frames:
        question_params_widget._reset_error_frames()

        question_params_widget._color_error_param_frame(selected_frame)

        for frame in frames:
            if frame is selected_frame:
                assert frame.property("paramState") == "error"
            else:
                assert frame.property("paramState") is None

def test_on_error_reset_combobox_to_default_values_reset_all_cb_indexes(
        qtbot: QtBot,
        question_params_widget: QuestionParamsWidget,
        ) -> None:
    """
    Test on_error_reset_combobox_to_default_values method: 
    - reset all comboboxes index to 0
    """
    qtbot.addWidget(question_params_widget)

    # Confirm that all CB are set to default values
    assert question_params_widget._amount_cb.currentData() == "1"
    assert question_params_widget._difficulty_cb.currentData() == "diff1"
    assert question_params_widget._category_cb.currentData() == "cat1"
    assert question_params_widget._type_cb.currentData() == "type1"

    # Set new indexes for all CB
    question_params_widget._amount_cb.setCurrentIndex(1)
    question_params_widget._difficulty_cb.setCurrentIndex(1)
    question_params_widget._category_cb.setCurrentIndex(1)
    question_params_widget._type_cb.setCurrentIndex(1)

    # Confirm new values in CB
    assert question_params_widget._amount_cb.currentData() == "2"
    assert question_params_widget._difficulty_cb.currentData() == "diff2"
    assert question_params_widget._category_cb.currentData() == "cat2"
    assert question_params_widget._type_cb.currentData() == "type2"

    # Reset
    question_params_widget.on_error_reset_combobox_to_default_values()
    # Confirm reset succesfull
    assert question_params_widget._amount_cb.currentData() == "1"
    assert question_params_widget._difficulty_cb.currentData() == "diff1"
    assert question_params_widget._category_cb.currentData() == "cat1"
    assert question_params_widget._type_cb.currentData() == "type1"

def test_on_error_reset_combobox_to_default_values_reset_selected_cb_index(
        qtbot: QtBot, 
        question_params_widget: QuestionParamsWidget,
        comboboxes,
        ) -> None:
    """
    Test on_error_reset_combobox_to_default_values method:
    - reset only one selected combobox index to 0
    """
    qtbot.addWidget(question_params_widget)

    # Set new indexes for all CB
    question_params_widget._amount_cb.setCurrentIndex(1)
    question_params_widget._difficulty_cb.setCurrentIndex(1)
    question_params_widget._category_cb.setCurrentIndex(1)
    question_params_widget._type_cb.setCurrentIndex(1)

    question_params_widget.on_error_reset_combobox_to_default_values(QuestionParamsField.AMOUNT)
    for cb in comboboxes:
        if cb is question_params_widget._amount_cb:
            assert cb.currentIndex() == 0
        else:
            assert cb.currentIndex() == 1

def test_on_error_reset_combobox_to_default_values_reset_two_selected_cb_indexes(
        qtbot: QtBot, 
        question_params_widget: QuestionParamsWidget,
        comboboxes,
        ) -> None:
    """
    Test on_error_reset_combobox_to_default_values method:
    - reset only two selected combobox index to 0
    """
    qtbot.addWidget(question_params_widget)

    # Set new indexes for all CB
    question_params_widget._amount_cb.setCurrentIndex(1)
    question_params_widget._difficulty_cb.setCurrentIndex(1)
    question_params_widget._category_cb.setCurrentIndex(1)
    question_params_widget._type_cb.setCurrentIndex(1)

    question_params_widget.on_error_reset_combobox_to_default_values(
        QuestionParamsField.DIFFICULTY,
        QuestionParamsField.QUESTION_TYPE,
        )
    for cb in comboboxes:
        if cb is question_params_widget._difficulty_cb:
            assert cb.currentIndex() == 0
        elif cb is question_params_widget._type_cb:
            assert cb.currentIndex() == 0
        else:
            assert cb.currentIndex() == 1

def test_on_error_reset_combobox_to_default_values_calls_color(
        qtbot: QtBot,
        question_params_widget: QuestionParamsWidget,
        mocker: MockerFixture,
        frames
        ) -> None:
    """
    Test on_error_reset_combobox_to_default_values method: 
    - calls _color_error_param_frame method on all frames
    """
    qtbot.addWidget(question_params_widget)

    color = mocker.spy(question_params_widget, "_color_error_param_frame")

    question_params_widget.on_error_reset_combobox_to_default_values()
    assert color.call_count == 4

    color.assert_has_calls(
        [call(frame) for frame in frames],
        any_order=True
    )

def test_on_error_color_all_param_frames(
        qtbot: QtBot, 
        question_params_widget: QuestionParamsWidget,
        frames,
        ) -> None:
    """
    Test on_error_reset_combobox_to_default_values method 
    - set error frame property to all frames.
    """
    qtbot.addWidget(question_params_widget)

    # Check defualt property
    for frame in frames:
        assert frame.property("paramState") is None

    # Uses _color_error_param_frame 
    question_params_widget.on_error_reset_combobox_to_default_values() 

    for frame in frames:
        assert frame.property("paramState") == "error"

def test_on_error_color_selected_param_frames(
        qtbot: QtBot, 
        question_params_widget: QuestionParamsWidget,
        frames,
        fields
        ) -> None:
    """
    Test on_error_reset_combobox_to_default_values method:
    - set error frame property only to selected frames.
    """
    qtbot.addWidget(question_params_widget)

    # Check defualt property
    for frame in frames:
        assert frame.property("paramState") is None

    for selected_frame, field in zip(frames, fields, strict=True):
        question_params_widget._reset_error_frames()

        question_params_widget.on_error_reset_combobox_to_default_values(field)

        for frame in frames:
            if frame is selected_frame:
                assert frame.property("paramState") == "error"
            else:
                assert frame.property("paramState") is None
