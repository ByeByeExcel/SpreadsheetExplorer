from typing import Optional

from model.feature import Feature
from model.models.i_connected_workbook import IConnectedWorkbook
from model.models.spreadsheet.cell_address import CellAddress
from model.utils.observable_value import ObservableValue


class AppState:
    def __init__(self):
        self.active_feature: ObservableValue[Optional[Feature]] = ObservableValue(None)
        self.is_connected_to_workbook: ObservableValue[bool] = ObservableValue(False)
        self.selected_cell: ObservableValue[Optional[CellAddress]] = ObservableValue(None)
        self._connected_workbook: Optional[IConnectedWorkbook] = None
        self._initial_colors: dict[CellAddress, str] = {}

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
            raise ValueError("No feature is active.")
        else:
            raise ValueError(f"Feature {feature} is not active.")

    def is_feature_active(self, feature: Feature) -> bool:
        return feature == self.active_feature.value

    def store_initial_colors(self, colors: dict[CellAddress, str]) -> None:
        if self._initial_colors:
            raise ValueError("Initial colors have already been set.")
        self._initial_colors = colors

    def get_initial_colors(self) -> dict[CellAddress, str]:
        return self._initial_colors

    def clear_initial_colors(self) -> None:
        self._initial_colors.clear()

    def can_start_feature(self) -> bool:
        return not self.active_feature.value and self.is_connected_to_workbook.value
