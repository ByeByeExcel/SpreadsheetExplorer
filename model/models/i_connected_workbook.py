from abc import ABC, abstractmethod
from typing import Any

from model.models.spreadsheet.cell_address import CellAddress
from model.models.spreadsheet.spreadsheet_classes import Workbook, Cell


class IConnectedWorkbook(ABC, Workbook):
    connected_workbook: Any = None
    fullpath: str = None
    name: str = None

    @abstractmethod
    def get_range_color(self, cell_range: CellAddress) -> str:
        pass

    @abstractmethod
    def set_range_color(self, cell: CellAddress, color: str):
        pass

    @abstractmethod
    def set_ranges_color(self, cell: [CellAddress], color: str):
        pass

    @abstractmethod
    def set_cells_color(self, cell: [Cell], color: str):
        pass

    @abstractmethod
    def get_selected_cell(self) -> CellAddress:
        pass
