from abc import ABC, abstractmethod

from model.models.spreadsheet.cell_address import CellAddress
from model.models.spreadsheet.workbook import Workbook


class IConnectedWorkbook(ABC, Workbook):

    @abstractmethod
    def get_connected_workbook(self):
        pass

    @abstractmethod
    def calculate_workbook(self):
        pass

    @abstractmethod
    def get_range_color(self, cell_range: CellAddress) -> str:
        pass

    @abstractmethod
    def set_range_color(self, cell_range: CellAddress, color: str):
        pass

    @abstractmethod
    def set_ranges_color(self, cell_ranges: set[CellAddress], color: str):
        pass

    @abstractmethod
    def get_selected_cell(self) -> CellAddress:
        pass

    @abstractmethod
    def add_name(self, cell_range: CellAddress, new_name: str) -> None:
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
    def initial_to_grayscale_and_set_from_dict_and_return_initial_colors(
            self,
            new_colors: dict[CellAddress, str]
    ) -> dict[CellAddress, str]:
        pass

    @abstractmethod
    def set_colors_from_dict(self, colors: dict[CellAddress, str]):
        pass
