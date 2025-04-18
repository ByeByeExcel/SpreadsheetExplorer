from abc import abstractmethod, ABC

from model.models.spreadsheet.spreadsheet_classes import Cell, Workbook


class CellToColorConverter(ABC):
    def __init__(self, workbook: Workbook):
        self.workbook: Workbook = workbook

    @abstractmethod
    def convert(self, cell: Cell) -> str:
        pass
