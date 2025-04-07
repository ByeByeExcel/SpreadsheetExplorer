from abc import ABC, abstractmethod

from model.models.spreadsheet.spreadsheet_classes import Cell, Worksheet, Workbook


class IConnectedWorkbook(ABC, Workbook):
    connected_workbook = None

    @abstractmethod
    def set_cell_color(self, sheet: Worksheet, cell: Cell, color: str):
        pass
