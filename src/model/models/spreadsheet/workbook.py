from typing import Optional

from model.models.spreadsheet.cell import Cell
from model.models.spreadsheet.cell_address import CellAddress
from model.models.spreadsheet.dependency_graph import DependencyGraph


class Workbook:
    def __init__(self, name: str, fullpath: str):
        super().__init__()
        self.name = name
        self.fullpath = fullpath
        self._dependency_graph: Optional[DependencyGraph] = None

    def __str__(self):
        return f"Workbook(name={self.name}, fullpath={self.fullpath})"

    def __repr__(self):
        return f"Workbook(name={self.name}, fullpath={self.fullpath})"

    def get_all_cells(self) -> set[Cell]:
        if self._dependency_graph:
            return self._dependency_graph.get_cells()
        return set()

    def get_cell(self, cell_address: CellAddress) -> Cell | None:
        return self._dependency_graph.get_cell(cell_address) if self._dependency_graph else None

    def set_dependency_graph(self, dependency_graph: DependencyGraph):
        self._dependency_graph = dependency_graph

    def has_precedent(self, cell_address: CellAddress) -> bool:
        return self._dependency_graph.has_precedent(cell_address) if self._dependency_graph else False

    def has_dependent(self, cell_address: CellAddress) -> bool:
        return self._dependency_graph.has_dependent(cell_address) if self._dependency_graph else False

    def resolve_dependents_to_cell_level(self, cell_address: CellAddress) -> set[CellAddress]:
        return self._dependency_graph.resolve_dependents_to_cell_level(
            cell_address) if self._dependency_graph else set()

    def resolve_precedents_to_cell_level(self, cell_address: CellAddress) -> set[CellAddress]:
        return self._dependency_graph.resolve_precedents_to_cell_level(
            cell_address) if self._dependency_graph else set()

    def get_dependents(self, cell_address: CellAddress) -> set[CellAddress]:
        return self._dependency_graph.get_dependents(cell_address) if self._dependency_graph else set()

    def get_precedents(self, cell_address: CellAddress) -> set[CellAddress]:
        return self._dependency_graph.get_precedents(cell_address) if self._dependency_graph else set()
