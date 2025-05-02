from abc import abstractmethod, ABC

from model.domain_model.spreadsheet.cell_range import CellRange
from model.domain_model.spreadsheet.workbook import Workbook


class IRangeColorStrategy(ABC):
    def __init__(self, workbook: Workbook):
        self.workbook: Workbook = workbook

    @abstractmethod
    def convert(self, cell_range: CellRange) -> str:
        pass
