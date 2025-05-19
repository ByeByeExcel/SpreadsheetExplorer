from abc import ABC, abstractmethod

from model.domain_model.spreadsheet.dependency_graph import DependencyGraph


class ISpreadsheetParserService(ABC):
    @abstractmethod
    def get_dependencies(self) -> DependencyGraph:
        pass
