from unittest.mock import Mock, patch

import pytest

from model.domain_model.feature import Feature
from model.services.features.coloring.interactive.selection_coloring_service import SelectionColoringService


@pytest.fixture
def mock_app_state():
    app_state = Mock()
    app_state.can_start_feature.return_value = True
    app_state.get_connected_workbook().grayscale_colors_and_return_initial_colors.return_value = {'A1': '#ffffff'}
    app_state.selected_range.value = 'A1'
    return app_state


@patch('model.services.features.coloring.interactive.selection_coloring_service.SelectionDependencyHighlighterObserver')
def test_start_dependency_highlighting_ok(mock_observer_class, mock_app_state):
    mock_observer = Mock()
    mock_observer_class.return_value = mock_observer

    service = SelectionColoringService(mock_app_state)
    service.start_dependency_highlighting()

    mock_app_state.set_feature_active.assert_called_once_with(Feature.DEPENDENCY_HIGHLIGHTING)
    mock_app_state.store_initial_colors.assert_called_once_with({'A1': '#ffffff'})
    mock_app_state.selected_range.add_observer.assert_called_once_with(mock_observer)
    mock_observer.initialize.assert_called_once_with('A1')
    assert service._selection_dependency_highlighter_observer == mock_observer


def test_start_dependency_highlighting_fail(mock_app_state):
    mock_app_state.can_start_feature.return_value = False
    service = SelectionColoringService(mock_app_state)

    with pytest.raises(ValueError):
        service.start_dependency_highlighting()


@patch('model.services.features.coloring.interactive.selection_coloring_service.SelectionDependencyHighlighterObserver')
def test_stop_dependency_highlighting_ok(mock_observer_class, mock_app_state):
    mock_observer = Mock()
    service = SelectionColoringService(mock_app_state)
    service._selection_dependency_highlighter_observer = mock_observer

    service.stop_dependency_highlighting()

    mock_app_state.selected_range.remove_observer.assert_called_once_with(mock_observer)
    mock_observer.stop.assert_called_once()
    mock_app_state.get_connected_workbook().set_colors_from_dict.assert_called_once_with(
        mock_app_state.get_initial_colors())
    mock_app_state.clear_initial_colors.assert_called_once()
    mock_app_state.set_feature_inactive.assert_called_once_with(Feature.DEPENDENCY_HIGHLIGHTING)
    assert service._selection_dependency_highlighter_observer is None


def test_stop_dependency_highlighting_noop(mock_app_state):
    service = SelectionColoringService(mock_app_state)
    service._selection_dependency_highlighter_observer = None

    service.stop_dependency_highlighting()

    mock_app_state.selected_range.remove_observer.assert_not_called()
    mock_app_state.get_connected_workbook().set_colors_from_dict.assert_not_called()
    mock_app_state.clear_initial_colors.assert_not_called()
    mock_app_state.set_feature_inactive.assert_not_called()
