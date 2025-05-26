from unittest.mock import Mock, patch

import pytest

from model.domain_model.feature import Feature
from model.services.features.coloring.static.feature_coloring_service import FEATURE_TO_COLOR_STRATEGY
from model.services.features.coloring.static.feature_coloring_service import FeatureColoringService


@pytest.fixture
def mock_app_state():
    app_state = Mock()
    app_state.can_start_feature.return_value = True
    app_state.get_connected_workbook().get_all_cell_ranges.return_value = []
    app_state.get_connected_workbook().initial_to_grayscale_and_set_from_dict_and_return_initial_colors.return_value = {}
    return app_state


@patch.dict('model.services.features.coloring.static.feature_coloring_service.FEATURE_TO_COLOR_STRATEGY',
            {Feature.DEPENDENTS_HEATMAP: Mock(), Feature.ROOT_NODES: Mock()})
def test_show_feature_coloring_ok(mock_app_state):
    service = FeatureColoringService(mock_app_state)

    # Test DEPENDENTS_HEATMAP
    service.show_feature_coloring(Feature.DEPENDENTS_HEATMAP)

    mock_app_state.set_feature_active.assert_called_with(Feature.DEPENDENTS_HEATMAP)
    strategy_cls = FEATURE_TO_COLOR_STRATEGY[Feature.DEPENDENTS_HEATMAP]
    strategy_cls.assert_called_once_with(mock_app_state.get_connected_workbook())

    # Test ROOT_NODES
    service.show_feature_coloring(Feature.ROOT_NODES)

    mock_app_state.set_feature_active.assert_called_with(Feature.ROOT_NODES)
    strategy_cls = FEATURE_TO_COLOR_STRATEGY[Feature.ROOT_NODES]
    strategy_cls.assert_called_once_with(mock_app_state.get_connected_workbook())


def test_show_feature_coloring_fail(mock_app_state):
    service = FeatureColoringService(mock_app_state)
    with pytest.raises(ValueError):
        service.show_feature_coloring(Feature.DEPENDENCY_HIGHLIGHTING)


def test_show_feature_coloring_cannot_start(mock_app_state):
    mock_app_state.can_start_feature.return_value = False
    service = FeatureColoringService(mock_app_state)
    with pytest.raises(ValueError):
        service.show_feature_coloring(Feature.DEPENDENTS_HEATMAP)


def test_stop_feature_coloring(mock_app_state):
    service = FeatureColoringService(mock_app_state)
    service.stop_feature_coloring(Feature.DEPENDENTS_HEATMAP)

    mock_app_state.get_connected_workbook().set_colors_from_dict.assert_called_once_with(
        mock_app_state.get_initial_colors()
    )
    mock_app_state.clear_initial_colors.assert_called_once()
    mock_app_state.set_feature_inactive.assert_called_once_with(Feature.DEPENDENTS_HEATMAP)
