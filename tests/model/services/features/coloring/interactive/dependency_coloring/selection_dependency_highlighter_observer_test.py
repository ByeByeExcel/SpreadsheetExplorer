from unittest.mock import Mock

import pytest

from model.domain_model.spreadsheet.range_reference import RangeReference, RangeReferenceType
from model.services.features.coloring.interactive.dependency_coloring.selection_dependency_highligher_observer import \
    SelectionDependencyHighlighterObserver
from model.settings.color_scheme import ColorScheme, ColorRole


@pytest.fixture
def mock_workbook():
    wb = Mock()
    wb.name = 'testworkbook'
    wb.resolve_precedents_to_cell_level = Mock(
        return_value={RangeReference('testworkbook', 'Sheet1', 'A1', RangeReferenceType.CELL)})
    wb.resolve_dependents_to_cell_level = Mock(
        return_value={RangeReference('testworkbook', 'Sheet1', 'B1', RangeReferenceType.CELL)})
    wb.get_range_color = Mock(return_value='#ffffff')
    wb.set_colors_from_dict = Mock()
    wb.set_ranges_color = Mock()
    return wb


def test_call_with_cell_reference(mock_workbook):
    observer = SelectionDependencyHighlighterObserver(mock_workbook)
    new_ref = RangeReference('testworkbook', 'Sheet1', 'A1', RangeReferenceType.CELL)

    observer(new_ref, None)

    mock_workbook.set_colors_from_dict.assert_called_once()
    assert len(observer.original_colors) == 2
    mock_workbook.set_ranges_color.assert_any_call(
        {RangeReference('testworkbook', 'Sheet1', 'A1', RangeReferenceType.CELL)}, ColorScheme[ColorRole.PRECEDENT])
    mock_workbook.set_ranges_color.assert_any_call(
        {RangeReference('testworkbook', 'Sheet1', 'B1', RangeReferenceType.CELL)}, ColorScheme[ColorRole.DEPENDENT])


def test_call_with_none_reference(mock_workbook):
    observer = SelectionDependencyHighlighterObserver(mock_workbook)
    observer.original_colors = {RangeReference('testworkbook', 'Sheet1', 'A1', RangeReferenceType.CELL): '#ffffff'}

    observer(None, None)

    mock_workbook.set_colors_from_dict.assert_called_once_with(observer.original_colors)
    assert observer.original_colors == {}


def test_stop_clears_colors(mock_workbook):
    observer = SelectionDependencyHighlighterObserver(mock_workbook)
    observer.original_colors = {RangeReference('testworkbook', 'Sheet1', 'A1', RangeReferenceType.CELL): '#ffffff'}

    observer.stop()

    mock_workbook.set_colors_from_dict.assert_called_once_with(observer.original_colors)
    assert observer.original_colors == {}
