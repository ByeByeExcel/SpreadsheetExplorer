from unittest.mock import Mock

import pytest

from model.domain_model.spreadsheet.range_reference import RangeReference, RangeReferenceType
from model.services.current_range_selection.selection_monitoring import SelectionMonitoring


@pytest.fixture
def mock_root():
    root = Mock()
    root.after = Mock(return_value='after_id')
    root.after_cancel = Mock()
    return root


@pytest.fixture
def mock_workbook():
    workbook = Mock()
    workbook.name = 'testworkbook'
    workbook.get_selected_range_ref = Mock(
        return_value=RangeReference('testworkbook', 'Sheet1', 'A1', RangeReferenceType.CELL))
    return workbook


def test_start_and_stop(mock_root, mock_workbook):
    callback = Mock()
    monitor = SelectionMonitoring(mock_root, mock_workbook, callback)

    monitor.start()
    assert monitor._active is True
    assert monitor._after_id == 'after_id'

    monitor.stop()
    assert monitor._active is False
    mock_root.after_cancel.assert_called_with('after_id')
    callback.assert_called_with(None)


def test_poll_selection_triggers_callback(mock_root, mock_workbook):
    callback = Mock()
    monitor = SelectionMonitoring(mock_root, mock_workbook, callback)
    monitor._active = True

    monitor._poll_selection()
    callback.assert_called_with(mock_workbook.get_selected_range_ref())


def test_poll_selection_excel_busy(mock_root, mock_workbook, capsys):
    callback = Mock()
    mock_workbook.get_selected_range_ref.side_effect = Exception('0x800ac472')  # Excel busy code
    monitor = SelectionMonitoring(mock_root, mock_workbook, callback)
    monitor._active = True

    # Should not raise
    monitor._poll_selection()
    captured = capsys.readouterr()
    assert '[WorkbookClickWatcher]' not in captured.out


def test_poll_selection_other_exception(mock_root, mock_workbook):
    callback = Mock()
    mock_workbook.get_selected_range_ref.side_effect = Exception('Some other error')
    monitor = SelectionMonitoring(mock_root, mock_workbook, callback)
    monitor._active = True

    with pytest.raises(Exception):
        monitor._poll_selection()
