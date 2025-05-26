from unittest.mock import MagicMock, create_autospec

import pytest

from model.adapters.i_connected_workbook import IConnectedWorkbook
from model.adapters.i_spreadsheet_connection_service import ISpreadsheetConnectionService
from model.domain_model.feature import Feature
from model.services.app_state_service import AppStateService
from model.services.connected_workbook_service import ConnectedWorkbookService
from model.services.current_range_selection.selection_monitoring import SelectionMonitoring
from model.utils.observable_value import ObservableValue


@pytest.fixture
def mock_workbook():
    mock = create_autospec(IConnectedWorkbook)

    # Stub expected methods and return values
    mock.get_names.return_value = []

    def dummy_set_dependency_graph(graph):
        mock._graph = graph

    mock.set_dependency_graph.side_effect = dummy_set_dependency_graph
    mock._graph = None

    return mock


@pytest.fixture
def app_state():
    state = AppStateService()
    state.active_feature = ObservableValue(None)
    state.is_connected_to_workbook = ObservableValue(False)
    state.is_analyzing = ObservableValue(False)
    state.set_connected_workbook = MagicMock()
    state.clear_connected_workbook = MagicMock()
    state.get_connected_workbook = MagicMock()
    state.selected_range = ObservableValue(None)
    return state


@pytest.fixture
def connection_service():
    return create_autospec(ISpreadsheetConnectionService)


@pytest.fixture
def controller(app_state, connection_service):
    return ConnectedWorkbookService(connection_service, app_state)


def test_connect_workbook_success(controller, app_state, connection_service):
    dummy_wb = MagicMock(spec=IConnectedWorkbook)
    connection_service.connect_to_workbook.return_value = dummy_wb

    controller.connect_workbook("test.xlsx")

    connection_service.connect_to_workbook.assert_called_with("test.xlsx")
    app_state.set_connected_workbook.assert_called_with(dummy_wb)


def test_connect_workbook_fails_if_feature_active(controller, app_state):
    app_state.active_feature.set_value(Feature.ROOT_NODES)
    with pytest.raises(RuntimeError, match="feature is active"):
        controller.connect_workbook("test.xlsx")


def test_connect_workbook_fails_if_already_connected(controller, app_state):
    app_state.is_connected_to_workbook.set_value(True)
    with pytest.raises(RuntimeError, match="Already connected"):
        controller.connect_workbook("test.xlsx")


def test_connect_workbook_file_not_found(controller, app_state, connection_service):
    connection_service.connect_to_workbook.return_value = None
    with pytest.raises(FileNotFoundError):
        controller.connect_workbook("missing.xlsx")


def test_disconnect_workbook_success(controller, app_state, mock_workbook):
    mock_monitoring = MagicMock()
    controller.selection_monitoring = mock_monitoring

    controller.disconnect_workbook()

    mock_monitoring.stop.assert_called_once()
    app_state.clear_connected_workbook.assert_called_once()


def test_disconnect_workbook_fails_if_feature_active(controller, app_state):
    app_state.active_feature.set_value(Feature.DEPENDENTS_HEATMAP)
    with pytest.raises(RuntimeError, match="feature is active"):
        controller.disconnect_workbook()


def test_parse_connected_workbook_success(controller, app_state, mock_workbook):
    app_state.get_connected_workbook.return_value = mock_workbook
    app_state.is_connected_to_workbook.set_value(True)

    controller.parse_connected_workbook()

    assert app_state.is_analyzing.value is False


def test_parse_connected_workbook_fails_if_conditions_not_met(controller, app_state):
    with pytest.raises(RuntimeError, match="No connected workbook"):
        controller.parse_connected_workbook()

    app_state.is_connected_to_workbook.set_value(True)
    app_state.is_analyzing.set_value(True)
    with pytest.raises(RuntimeError, match="already analyzing"):
        controller.parse_connected_workbook()

    app_state.is_analyzing.set_value(False)
    app_state.active_feature.set_value(Feature.CASCADE_RENAME)
    with pytest.raises(RuntimeError, match="feature is active"):
        controller.parse_connected_workbook()


def test_start_stop_watching_selected_cell(controller, app_state):
    app_state.get_connected_workbook.return_value = MagicMock()
    app_state.is_connected_to_workbook.set_value(True)

    mock_root = MagicMock()
    controller.set_root(mock_root)

    controller.start_watching_selected_cell()

    # Ensure a SelectionMonitoring instance is created
    assert isinstance(controller.selection_monitoring, SelectionMonitoring)

    # Replace .stop with a mock and preserve a reference before stopping
    mock_stop = MagicMock()
    controller.selection_monitoring.stop = mock_stop

    controller.stop_watching_selected_cell()

    mock_stop.assert_called_once()
    assert controller.selection_monitoring is None


def test_update_selected_range_sets_value(controller, app_state):
    from model.domain_model.spreadsheet.range_reference import RangeReference, RangeReferenceType
    ref = RangeReference.from_raw("Book", "Sheet", "A1", RangeReferenceType.CELL)
    controller._update_selected_range(ref)
    assert app_state.selected_range.value == ref
