from unittest.mock import MagicMock

import pytest

from controller.feature_controller import FeatureController
from model.domain_model.feature import Feature


@pytest.fixture
def mock_services():
    return {
        "interactive_painting_service": MagicMock(),
        "painting_service": MagicMock(),
        "renaming_service": MagicMock(),
        "app_state": MagicMock()
    }


@pytest.fixture
def controller(mock_services):
    return FeatureController(
        interactive_painting_service=mock_services["interactive_painting_service"],
        painting_service=mock_services["painting_service"],
        renaming_service=mock_services["renaming_service"],
        app_state=mock_services["app_state"]
    )


def test_start_stop_dependency_highlighting(controller, mock_services):
    controller.start_dependency_highlighting()
    controller.stop_dependency_highlighting()

    mock_services["interactive_painting_service"].start_dependency_highlighting.assert_called_once()
    mock_services["interactive_painting_service"].stop_dependency_highlighting.assert_called_once()


def test_show_hide_heatmap(controller, mock_services):
    controller.show_heatmap()
    controller.hide_heatmap()

    mock_services["painting_service"].show_feature_coloring.assert_called_with(Feature.DEPENDENTS_HEATMAP)
    mock_services["painting_service"].stop_feature_coloring.assert_called_with(Feature.DEPENDENTS_HEATMAP)


def test_show_hide_root_nodes(controller, mock_services):
    controller.show_root_nodes()
    controller.hide_root_nodes()

    mock_services["painting_service"].show_feature_coloring.assert_called_with(Feature.ROOT_NODES)
    mock_services["painting_service"].stop_feature_coloring.assert_called_with(Feature.ROOT_NODES)


def test_activate_deactivate_cascade_rename(controller, mock_services):
    controller.activate_cascade_rename()
    controller.deactivate_cascade_rename()

    mock_services["app_state"].set_feature_active.assert_called_with(Feature.CASCADE_RENAME)
    mock_services["app_state"].set_feature_inactive.assert_called_with(Feature.CASCADE_RENAME)


def test_cascade_rename_valid_name(controller, mock_services):
    controller.cascade_rename("NewName")
    mock_services["renaming_service"].cascade_name_cell.assert_called_with("NewName")


def test_cascade_rename_invalid_name(controller):
    with pytest.raises(ValueError, match="Name cannot be empty."):
        controller.cascade_rename("   ")
