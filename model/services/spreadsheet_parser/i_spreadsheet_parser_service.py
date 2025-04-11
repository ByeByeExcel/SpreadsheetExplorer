from abc import ABC, abstractmethod

from model.models.spreadsheet.spreadsheet_classes import CellDependencies


class ISpreadsheetParserService(ABC):
    @abstractmethod
    def get_dependencies(self, filename: str) -> CellDependencies:
        pass
