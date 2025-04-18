from abc import ABC, abstractmethod

from src.model.models.spreadsheet.spreadsheet_classes import CellDependencies


class ISpreadsheetParserService(ABC):
    @abstractmethod
    def get_dependencies(self) -> CellDependencies:
        pass
