from abc import ABC, abstractmethod
from typing import Any

from model.models.spreadsheet.cell_address import CellAddress
from model.models.spreadsheet.spreadsheet_classes import Workbook


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
    def set_ranges_color(self, cell: set[CellAddress], color: str):
        pass

    @abstractmethod
    def get_selected_cell(self) -> CellAddress:
        pass

    @abstractmethod
    def add_name(self, cell: CellAddress, new_name: str) -> None:
        pass

    @abstractmethod
    def get_names(self) -> dict[str, str]:
        pass

    @abstractmethod
    def set_formula(self, cell: CellAddress, formula: str):
        pass

    @abstractmethod
    def disable_screen_updating(self):
        pass

    @abstractmethod
    def enable_screen_updating(self):
        pass

    @abstractmethod
    def grayscale_colors_and_return_initial_colors(self) -> dict[CellAddress, str]:
        pass

    @abstractmethod
    def initial_to_grayscale_and_set_from_dict_and_return_initial_colors(self, colors: dict[CellAddress, str]) -> dict[
        CellAddress, str]:
        pass

    @abstractmethod
    def set_colors_from_dict(self, colors: dict[CellAddress, str]):
        pass
