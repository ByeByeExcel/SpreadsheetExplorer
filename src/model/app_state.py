from typing import Optional

from model.domain_model.i_connected_workbook import IConnectedWorkbook
from model.domain_model.spreadsheet.range_reference import RangeReference
from model.domain_model.spreadsheet.range_with_context import RangeWithContext
from model.feature import Feature
from model.utils.observable_value import ObservableValue


class AppState:
    def __init__(self):
        self.active_feature: ObservableValue[Optional[Feature]] = ObservableValue(None)
        self.is_connected_to_workbook: ObservableValue[bool] = ObservableValue(False)
        self.is_analyzing: ObservableValue[bool] = ObservableValue(False)
        self.selected_range: ObservableValue[Optional[RangeReference]] = ObservableValue(None)
        self.selected_range_with_context: ObservableValue[Optional[RangeWithContext]] = ObservableValue(None)

        self._connected_workbook: Optional[IConnectedWorkbook] = None
        self._initial_colors: dict[RangeReference, str] = {}

    def get_connected_workbook(self) -> Optional[IConnectedWorkbook]:
        return self._connected_workbook

    def set_connected_workbook(self, workbook: IConnectedWorkbook) -> None:
        self._connected_workbook = workbook
        self.is_connected_to_workbook.set_value(True)

    def clear_connected_workbook(self) -> None:
        self._connected_workbook = None
        self.is_connected_to_workbook.set_value(False)

    def set_feature_active(self, feature: Feature) -> None:
        if self.active_feature.value is None:
            self.active_feature.set_value(feature)
        elif self.active_feature.value == feature:
            raise ValueError("Feature is already active.")
        else:
            raise ValueError("Another feature is already active.")

    def set_feature_inactive(self, feature: Feature) -> None:
        if self.active_feature.value == feature:
            self.active_feature.set_value(None)
        elif self.active_feature.value is None:
            return
        else:
            raise ValueError(f"Another feature ({feature}) is active.")

    def is_feature_active(self, feature: Feature) -> bool:
        return feature == self.active_feature.value

    def store_initial_colors(self, colors: dict[RangeReference, str]) -> None:
        if self._initial_colors:
            raise ValueError("Initial colors have already been set.")
        self._initial_colors = colors

    def get_initial_colors(self) -> dict[RangeReference, str]:
        return self._initial_colors

    def clear_initial_colors(self) -> None:
        self._initial_colors.clear()

    def can_start_feature(self) -> bool:
        return not self.active_feature.value and self.is_connected_to_workbook.value
