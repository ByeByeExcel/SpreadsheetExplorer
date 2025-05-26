from unittest.mock import Mock

import pytest

from model.domain_model.spreadsheet.range_reference import RangeReference, RangeReferenceType
from model.domain_model.spreadsheet.range_with_context import RangeWithContext
from model.services.features.context_generation.selection_context_observer import SelectionContextObserver


@pytest.fixture
def mock_workbook():
    wb = Mock()
    wb.name = 'testworkbook'
    return wb


@pytest.fixture
def mock_callback():
    return Mock()


def test_call_with_none_reference(mock_workbook, mock_callback):
    observer = SelectionContextObserver(mock_workbook, mock_callback)
    observer(None, None)
    mock_callback.assert_called_once_with(None)


def test_call_with_mismatched_workbook(mock_workbook, mock_callback):
    observer = SelectionContextObserver(mock_workbook, mock_callback)
    mismatched_ref = RangeReference('otherworkbook', 'Sheet1', 'A1', RangeReferenceType.CELL)
    observer(mismatched_ref, None)
    mock_callback.assert_not_called()


def test_call_with_valid_reference(mock_workbook, mock_callback):
    observer = SelectionContextObserver(mock_workbook, mock_callback)
    valid_ref = RangeReference('testworkbook', 'Sheet1', 'A1', RangeReferenceType.CELL)

    # Setup workbook mock responses
    mock_workbook.get_precedents.return_value = []
    mock_workbook.get_range.return_value = Mock(value='val', formula='=1+1')

    observer(valid_ref, None)

    mock_callback.assert_called_once()
    called_arg = mock_callback.call_args[0][0]
    assert isinstance(called_arg, RangeWithContext)
    assert called_arg.reference == valid_ref
    assert called_arg.value == 'val'
    assert called_arg.formula == '=1+1'
    assert called_arg.precedents == []


def test_call_with_valid_reference_with_precedents(mock_workbook, mock_callback):
    observer = SelectionContextObserver(mock_workbook, mock_callback)
    valid_ref = RangeReference('testworkbook', 'Sheet1', 'A1', RangeReferenceType.CELL)
    precedent_ref = RangeReference('testworkbook', 'Sheet1', 'B1', RangeReferenceType.CELL)

    # Setup workbook mock responses
    mock_workbook.get_precedents.side_effect = lambda ref: [precedent_ref] if ref == valid_ref else []
    mock_workbook.get_range.side_effect = lambda ref: Mock(value='val', formula='=1+1') if ref == valid_ref else Mock(
        value='valB', formula='=2+2')

    observer(valid_ref, None)

    mock_callback.assert_called_once()
    called_arg = mock_callback.call_args[0][0]
    assert isinstance(called_arg, RangeWithContext)
    assert called_arg.reference == valid_ref
    assert called_arg.value == 'val'
    assert called_arg.formula == '=1+1'
    assert len(called_arg.precedents) == 1
    assert called_arg.precedents[0].reference == precedent_ref
    assert called_arg.precedents[0].value == 'valB'
    assert called_arg.precedents[0].formula == '=2+2'


def test_stop(mock_workbook, mock_callback):
    observer = SelectionContextObserver(mock_workbook, mock_callback)
    observer.stop()
    mock_callback.assert_called_once_with(None)


def test_initialize_calls_call(mock_workbook, mock_callback):
    observer = SelectionContextObserver(mock_workbook, mock_callback)
    init_ref = RangeReference('testworkbook', 'Sheet1', 'A1', RangeReferenceType.CELL)

    mock_workbook.get_precedents.return_value = []
    mock_workbook.get_range.return_value = Mock(value='val', formula='=1+1')

    observer.initialize(init_ref)

    mock_callback.assert_called_once()
    called_arg = mock_callback.call_args[0][0]
    assert isinstance(called_arg, RangeWithContext)
    assert called_arg.reference == init_ref
