from dataclasses import dataclass
from typing import Optional

from model.domain_model.spreadsheet.cell_range import CellRange
from model.domain_model.spreadsheet.dependency_graph import DependencyGraph
from model.domain_model.spreadsheet.range_reference import RangeReference


@dataclass
class Workbook:
    name: str
    fullpath: str
    _dependency_graph: Optional[DependencyGraph] = None

    def get_all_cell_ranges(self) -> set[CellRange]:
        if self._dependency_graph:
            return self._dependency_graph.get_cell_ranges()
        return set()

    def get_range(self, range_ref: RangeReference) -> CellRange | None:
        return self._dependency_graph.get_cell_range(range_ref) if self._dependency_graph else None

    def set_dependency_graph(self, dependency_graph: DependencyGraph):
        self._dependency_graph = dependency_graph

    def has_precedent(self, range_ref: RangeReference) -> bool:
        return self._dependency_graph.has_precedent(range_ref) if self._dependency_graph else False

    def has_dependent(self, range_ref: RangeReference) -> bool:
        return self._dependency_graph.has_dependent(range_ref) if self._dependency_graph else False

    def resolve_dependents_to_cell_level(self, range_ref: RangeReference) -> set[RangeReference]:
        return self._dependency_graph.resolve_dependents_to_cell_level(
            range_ref) if self._dependency_graph else set()

    def resolve_precedents_to_cell_level(self, range_ref: RangeReference) -> set[RangeReference]:
        return self._dependency_graph.resolve_precedents_to_cell_level(
            range_ref) if self._dependency_graph else set()

    def get_dependents(self, range_ref: RangeReference) -> set[RangeReference]:
        return self._dependency_graph.get_dependents(range_ref) if self._dependency_graph else set()

    def get_precedents(self, range_ref: RangeReference) -> set[RangeReference]:
        return self._dependency_graph.get_precedents(range_ref) if self._dependency_graph else set()
