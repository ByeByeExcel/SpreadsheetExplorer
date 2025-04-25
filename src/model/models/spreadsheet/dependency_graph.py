from dataclasses import dataclass
from typing import Optional

import networkx as nx

from model.models.spreadsheet.cell import Cell
from model.models.spreadsheet.cell_address import CellAddress, CellAddressType


@dataclass
class DependencyGraph:
    def __init__(self, graph: nx.DiGraph):
        self.graph: nx.DiGraph = graph

    def get_cell(self, cell_address: CellAddress) -> Optional[Cell]:
        if cell_address not in self.graph:
            return None
        return self.graph.nodes.get(cell_address).get('cell')

    def get_cells(self) -> set[Cell]:
        cells: set[Cell] = set()
        for cell_address in self.graph.nodes:
            cell = self.get_cell(cell_address)
            if cell:
                cells.add(cell)
        return cells

    def has_precedent(self, cell_address: CellAddress) -> bool:
        return len(self.get_precedents(cell_address)) > 0

    def has_dependent(self, cell_address: CellAddress) -> bool:
        return len(self.get_dependents(cell_address)) > 0

    def resolve_dependents_to_cell_level(self,
                                         cell_address: CellAddress,
                                         resolved_dependents: set[CellAddress] = None) -> set[CellAddress]:
        if resolved_dependents is None:
            resolved_dependents = set()
        for dependent in self.get_dependents(cell_address):
            if dependent.address_type == CellAddressType.CELL:
                resolved_dependents.add(dependent)
            elif dependent.address_type != CellAddressType.EXTERNAL:
                resolved_dependents.update(self.resolve_dependents_to_cell_level(dependent, resolved_dependents))
        return resolved_dependents

    def resolve_precedents_to_cell_level(self,
                                         cell_address: CellAddress,
                                         resolved_precedents: set[CellAddress] = None) -> set[CellAddress]:
        if resolved_precedents is None:
            resolved_precedents = set()
        for precedent in self.get_precedents(cell_address):
            if precedent.address_type == CellAddressType.CELL:
                resolved_precedents.add(precedent)
            elif precedent.address_type != CellAddressType.EXTERNAL:
                resolved_precedents.update(self.resolve_precedents_to_cell_level(precedent, resolved_precedents))
        return resolved_precedents

    def get_precedents(self, cell: CellAddress) -> set[CellAddress]:
        if cell in self.graph:
            return set(self.graph.predecessors(cell))
        return set()

    def get_dependents(self, cell: CellAddress) -> set[CellAddress]:
        if cell in self.graph:
            return set(self.graph.successors(cell))
        return set()
