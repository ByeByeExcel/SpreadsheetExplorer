from unittest.mock import Mock

import pytest

from model.domain_model.spreadsheet.cell_range import CellRange
from model.domain_model.spreadsheet.range_reference import RangeReference, RangeReferenceType
from model.services.features.coloring.static.color_strategies.dependents_heatmap import DependentsHeatmap
from model.settings.color_scheme import ColorScheme, ColorRole
from model.utils.color_utils import interpolate_color


@pytest.fixture
def mock_workbook():
    wb = Mock()
    return wb


def test_convert_with_no_cell_range(mock_workbook):
    strategy = DependentsHeatmap(mock_workbook)
    result = strategy.convert(None)
    assert result is None


def test_convert_with_no_dependents(mock_workbook):
    strategy = DependentsHeatmap(mock_workbook)
    cell_ref = RangeReference('book', 'sheet', 'A1', RangeReferenceType.CELL)
    cell_range = CellRange(cell_ref, 'value', 'formula')
    mock_workbook.resolve_dependents_to_cell_level.return_value = set()

    result = strategy.convert(cell_range)
    assert result is None


def test_convert_with_dependents(mock_workbook):
    strategy = DependentsHeatmap(mock_workbook)
    cell_ref = RangeReference('book', 'sheet', 'A1', RangeReferenceType.CELL)
    cell_range = CellRange(cell_ref, 'value', 'formula')
    mock_workbook.resolve_dependents_to_cell_level.return_value = {Mock(), Mock(), Mock()}  # 3 dependents

    expected_k = 3 / strategy._MAX_DEPENDENTS_FOR_COLOR
    expected_color = interpolate_color(ColorScheme[ColorRole.HEATMAP_0], ColorScheme[ColorRole.HEATMAP_1], expected_k)

    result = strategy.convert(cell_range)
    assert result == expected_color


def test_convert_max_dependents_clamping(mock_workbook):
    strategy = DependentsHeatmap(mock_workbook)
    cell_ref = RangeReference('book', 'sheet', 'A1', RangeReferenceType.CELL)
    cell_range = CellRange(cell_ref, 'value', 'formula')
    mock_workbook.resolve_dependents_to_cell_level.return_value = {Mock() for _ in range(20)}  # exceeds max

    expected_k = 1  # clamped
    expected_color = interpolate_color(ColorScheme[ColorRole.HEATMAP_0], ColorScheme[ColorRole.HEATMAP_1], expected_k)

    result = strategy.convert(cell_range)
    assert result == expected_color
