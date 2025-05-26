import pytest

from model.domain_model.feature import Feature
from model.domain_model.spreadsheet.range_reference import RangeReference
from model.services.app_state_service import AppStateService


class DummyWorkbook:
    pass


def test_initial_state():
    service = AppStateService()
    assert service.active_feature.value is None
    assert service.is_connected_to_workbook.value is False
    assert service.is_analyzing.value is False
    assert service.selected_range.value is None
    assert service.selected_range_with_context.value is None
    assert service.get_connected_workbook() is None
    assert service.get_initial_colors() == {}
    assert service.can_start_feature() is False


def test_set_and_clear_connected_workbook():
    service = AppStateService()
    dummy = DummyWorkbook()
    service.set_connected_workbook(dummy)
    assert service.get_connected_workbook() == dummy
    assert service.is_connected_to_workbook.value is True

    service.clear_connected_workbook()
    assert service.get_connected_workbook() is None
    assert service.is_connected_to_workbook.value is False


def test_feature_activation_and_deactivation():
    service = AppStateService()
    service.set_feature_active(Feature.CASCADE_RENAME)
    assert service.active_feature.value == Feature.CASCADE_RENAME

    service.set_feature_inactive(Feature.CASCADE_RENAME)
    assert service.active_feature.value is None


def test_feature_activation_conflicts():
    service = AppStateService()
    service.set_feature_active(Feature.CASCADE_RENAME)

    with pytest.raises(ValueError, match="Feature is already active."):
        service.set_feature_active(Feature.CASCADE_RENAME)

    with pytest.raises(ValueError, match="Another feature is already active."):
        service.set_feature_active(Feature.DEPENDENTS_HEATMAP)

    # Deactivating with wrong feature should raise
    with pytest.raises(ValueError, match="Another feature"):
        service.set_feature_inactive(Feature.DEPENDENTS_HEATMAP)


def test_is_feature_active():
    service = AppStateService()
    assert service.is_feature_active(Feature.DEPENDENTS_HEATMAP) is False

    service.set_feature_active(Feature.DEPENDENTS_HEATMAP)
    assert service.is_feature_active(Feature.DEPENDENTS_HEATMAP) is True
    assert service.is_feature_active(Feature.ROOT_NODES) is False


def test_store_and_clear_initial_colors():
    service = AppStateService()
    range1 = RangeReference.from_raw("Workbook1", "Sheet1", "A1")
    range2 = RangeReference.from_raw("Workbook1", "Sheet1", "B2")
    colors = {range1: "#FF0000", range2: "#00FF00"}

    service.store_initial_colors(colors)
    assert service.get_initial_colors() == colors

    with pytest.raises(ValueError, match="already been set"):
        service.store_initial_colors(colors)

    service.clear_initial_colors()
    assert service.get_initial_colors() == {}


def test_can_start_feature():
    service = AppStateService()
    assert not service.can_start_feature()

    service.set_connected_workbook(DummyWorkbook())
    assert service.can_start_feature() is True

    service.set_feature_active(Feature.ROOT_NODES)
    assert service.can_start_feature() is False
