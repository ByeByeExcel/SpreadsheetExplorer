from typing import Optional

from model.feature import Feature
from model.models.i_connected_workbook import IConnectedWorkbook
from model.models.spreadsheet.cell_address import CellAddress
from model.utils.observable_value import ObservableValue


class AppState:
    def __init__(self):
        self.selected_cell: ObservableValue[Optional[CellAddress]] = ObservableValue(None)
        self.connected_workbooks: dict[str, IConnectedWorkbook] = {}
        self._active_features: set[Feature] = set()

    def get_connected_workbooks(self) -> dict[str, IConnectedWorkbook]:
        return self.connected_workbooks

    def is_connected_to_workbook(self) -> bool:
        return bool(self.connected_workbooks)

    def set_feature_active(self, feature: Feature) -> None:
        self._active_features.add(feature)

    def set_feature_inactive(self, feature: Feature) -> None:
        self._active_features.discard(feature)

    def is_active(self, feature: Feature) -> bool:
        return feature in self._active_features

    def get_active_features(self) -> set[Feature]:
        return self._active_features
