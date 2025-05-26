from unittest.mock import Mock

import pytest

from model.domain_model.spreadsheet.cell_range import CellRange
from model.domain_model.spreadsheet.range_reference import RangeReference, RangeReferenceType
from model.services.features.coloring.static.color_strategies.root_node_coloring import RootNodeColoring
from model.settings.color_scheme import ColorScheme, ColorRole


@pytest.fixture
def mock_workbook():
    wb = Mock()
    return wb


def test_convert_with_no_cell_range(mock_workbook):
    strategy = RootNodeColoring(mock_workbook)
    result = strategy.convert(None)
    assert result is None


def test_convert_root_node(mock_workbook):
    strategy = RootNodeColoring(mock_workbook)
    cell_ref = RangeReference('book', 'sheet', 'A1', RangeReferenceType.CELL)
    cell_range = CellRange(cell_ref, 'value', 'formula')

    mock_workbook.has_dependent.return_value = False
    mock_workbook.has_precedent.return_value = True

    result = strategy.convert(cell_range)
    assert result == ColorScheme[ColorRole.ROOT_NODE]


def test_convert_non_root_node(mock_workbook):
    strategy = RootNodeColoring(mock_workbook)
    cell_ref = RangeReference('book', 'sheet', 'A1', RangeReferenceType.CELL)
    cell_range = CellRange(cell_ref, 'value', 'formula')

    mock_workbook.has_dependent.return_value = True
    mock_workbook.has_precedent.return_value = True

    result = strategy.convert(cell_range)
    assert result is None
