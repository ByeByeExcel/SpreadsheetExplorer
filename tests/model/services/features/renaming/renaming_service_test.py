from unittest.mock import Mock

import pytest

from model.domain_model.feature import Feature
from model.domain_model.spreadsheet.cell_range import CellRange
from model.domain_model.spreadsheet.range_reference import RangeReference, RangeReferenceType
from model.services.features.renaming.renaming_service import RenamingService


@pytest.fixture
def mock_app_state():
    app_state = Mock()
    app_state.get_connected_workbook.return_value = Mock()
    app_state.selected_range.value = RangeReference('book', 'Sheet1', 'A1', RangeReferenceType.CELL)
    return app_state


def test_cascade_name_cell_success(mock_app_state):
    workbook = mock_app_state.get_connected_workbook.return_value
    workbook.get_names.return_value = {}
    dependent_ref = RangeReference('book', 'Sheet1', 'B1', RangeReferenceType.CELL)
    workbook.get_dependents.return_value = {dependent_ref}
    workbook.get_range.return_value = CellRange(dependent_ref, 'value', '=A1')

    service = RenamingService(mock_app_state)
    service.cascade_name_cell('MyNewName')

    workbook.add_name.assert_called_once_with(mock_app_state.selected_range.value, 'MyNewName')
    workbook.set_formula.assert_called_once_with(dependent_ref, '=MyNewName')
    mock_app_state.set_feature_inactive.assert_called_once_with(Feature.CASCADE_RENAME)


def test_cascade_name_cell_no_selected_range(mock_app_state):
    mock_app_state.selected_range.value = None

    service = RenamingService(mock_app_state)
    with pytest.raises(ValueError, match='No cell selected.'):
        service.cascade_name_cell('MyNewName')

    mock_app_state.set_feature_inactive.assert_called_once_with(Feature.CASCADE_RENAME)


def test_cascade_name_cell_name_already_exists(mock_app_state):
    workbook = mock_app_state.get_connected_workbook.return_value
    workbook.get_names.return_value = {'MyNewName': 'some_ref'}

    service = RenamingService(mock_app_state)
    with pytest.raises(ValueError, match='already exists'):
        service.cascade_name_cell('MyNewName')

    mock_app_state.set_feature_inactive.assert_called_once_with(Feature.CASCADE_RENAME)


def test_cascade_name_cell_with_no_dependents(mock_app_state):
    workbook = mock_app_state.get_connected_workbook.return_value
    workbook.get_names.return_value = {}
    workbook.get_dependents.return_value = set()

    service = RenamingService(mock_app_state)
    service.cascade_name_cell('MyNewName')

    workbook.add_name.assert_called_once_with(mock_app_state.selected_range.value, 'MyNewName')
    workbook.set_formula.assert_not_called()
    mock_app_state.set_feature_inactive.assert_called_once_with(Feature.CASCADE_RENAME)
