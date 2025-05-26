from unittest.mock import Mock

import pytest

from model.services.features.context_generation.selection_context_service import SelectionContextService


@pytest.fixture
def mock_app_state():
    app_state = Mock()
    app_state.is_connected_to_workbook.add_observer = Mock()
    app_state.get_connected_workbook.return_value = Mock()
    app_state.selected_range.add_observer = Mock()
    app_state.selected_range.remove_observer = Mock()
    app_state.selected_range_with_context.set_value = Mock()
    return app_state


def test_start_selection_context_generation(mock_app_state):
    service = SelectionContextService(mock_app_state)
    service._start_selection_context_generation()
    mock_app_state.get_connected_workbook.assert_called_once()
    mock_app_state.selected_range.add_observer.assert_called_once()
    assert service._selection_observer is not None


def test_stop_selection_context_generation(mock_app_state):
    service = SelectionContextService(mock_app_state)
    mock_observer = Mock()
    service._selection_observer = mock_observer

    service._stop()
    mock_observer.stop.assert_called_once()
    mock_app_state.selected_range.remove_observer.assert_called_once_with(mock_observer)
    assert service._selection_observer is None


def test_stop_without_observer_does_nothing(mock_app_state):
    service = SelectionContextService(mock_app_state)
    service._selection_observer = None

    service._stop()
    mock_app_state.selected_range.remove_observer.assert_not_called()


def test_on_wb_connection_change_starts_and_stops(mock_app_state):
    service = SelectionContextService(mock_app_state)

    service._on_wb_connection_change(True, None)
    mock_app_state.selected_range.add_observer.assert_called_once()

    # Now force stop
    service._on_wb_connection_change(False, None)
    mock_app_state.selected_range.remove_observer.assert_called()


def test_on_context_updated_sets_value(mock_app_state):
    service = SelectionContextService(mock_app_state)
    context = Mock()
    service._on_context_updated(context)
    mock_app_state.selected_range_with_context.set_value.assert_called_once_with(context)
