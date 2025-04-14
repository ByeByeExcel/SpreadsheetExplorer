from typing import Optional

from model.models.i_connected_workbook import IConnectedWorkbook
from model.models.spreadsheet.cell_address import CellAddress
from model.utils.observable_value import ObservableValue


class AppState:
    def __init__(self):
        self.selected_cell: ObservableValue[Optional[CellAddress]] = ObservableValue(None)
        self.connected_workbooks: dict[str, IConnectedWorkbook] = {}

    def get_connected_workbooks(self) -> dict[str, IConnectedWorkbook]:
        return self.connected_workbooks

    def is_connected_to_workbook(self) -> bool:
        return bool(self.connected_workbooks)
