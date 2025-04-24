from abc import ABC, abstractmethod

from model.models.spreadsheet.dependency_graph import DependencyGraph


class ISpreadsheetParserService(ABC):
    @abstractmethod
    def get_dependencies(self) -> DependencyGraph:
        pass
