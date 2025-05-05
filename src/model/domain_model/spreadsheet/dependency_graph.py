from dataclasses import dataclass
from typing import Optional

import networkx as nx

from model.domain_model.spreadsheet.cell_range import CellRange
from model.domain_model.spreadsheet.range_reference import RangeReference, RangeReferenceType


@dataclass(frozen=True)
class DependencyGraph:
    graph: nx.DiGraph

    def get_cell_range(self, range_ref: RangeReference) -> Optional[CellRange]:
        if range_ref not in self.graph:
            return None
        return self.graph.nodes.get(range_ref).get('cell_range')

    def get_cell_ranges(self) -> set[CellRange]:
        cell_ranges: set[CellRange] = set()
        for cell_reference in self.graph.nodes:
            cell = self.get_cell_range(cell_reference)
            if cell:
                cell_ranges.add(cell)
        return cell_ranges

    def has_precedent(self, range_ref: RangeReference) -> bool:
        return len(self.get_precedents(range_ref)) > 0

    def has_dependent(self, range_ref: RangeReference) -> bool:
        return len(self.get_dependents(range_ref)) > 0

    def resolve_dependents_to_cell_level(self,
                                         range_ref: RangeReference,
                                         resolved_dependents: set[RangeReference] = None) -> set[RangeReference]:
        if resolved_dependents is None:
            resolved_dependents = set()
        for dependent in self.get_dependents(range_ref):
            if dependent.reference_type == RangeReferenceType.CELL:
                resolved_dependents.add(dependent)
            elif dependent.reference_type != RangeReferenceType.EXTERNAL:
                resolved_dependents.update(self.resolve_dependents_to_cell_level(dependent, resolved_dependents))
        return resolved_dependents

    def resolve_precedents_to_cell_level(self,
                                         range_ref: RangeReference,
                                         resolved_precedents: set[RangeReference] = None) -> set[RangeReference]:
        if resolved_precedents is None:
            resolved_precedents = set()
        for precedent in self.get_precedents(range_ref):
            if precedent.reference_type == RangeReferenceType.CELL:
                resolved_precedents.add(precedent)
            elif precedent.reference_type != RangeReferenceType.EXTERNAL:
                resolved_precedents.update(self.resolve_precedents_to_cell_level(precedent, resolved_precedents))
        return resolved_precedents

    def get_precedents(self, cell: RangeReference) -> set[RangeReference]:
        if cell in self.graph:
            return set(self.graph.predecessors(cell))
        return set()

    def get_dependents(self, cell: RangeReference) -> set[RangeReference]:
        if cell in self.graph:
            return set(self.graph.successors(cell))
        return set()
