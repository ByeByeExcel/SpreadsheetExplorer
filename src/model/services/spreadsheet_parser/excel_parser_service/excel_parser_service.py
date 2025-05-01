import re

import networkx as nx
import xlwings as xw

from model.domain_model.i_connected_workbook import IConnectedWorkbook
from model.domain_model.spreadsheet.cell_range import CellRange
from model.domain_model.spreadsheet.dependency_graph import DependencyGraph
from model.domain_model.spreadsheet.range_reference import RangeReference, RangeReferenceType
from model.services.spreadsheet_parser.i_spreadsheet_parser_service import ISpreadsheetParserService


class ExcelParserService(ISpreadsheetParserService):

    def __init__(self, connected_workbook: IConnectedWorkbook):
        self.wb: xw.Book = connected_workbook.get_connected_workbook()
        self.graph: nx.DiGraph[RangeReference] = nx.DiGraph()

    def get_dependencies(self) -> DependencyGraph:
        self.graph.clear()
        self.build_dependency_graph()

        return DependencyGraph(self.graph)

    def add_range_dependencies(self, range_ref: RangeReference) -> None:
        if range_ref is None or range_ref.reference_type != RangeReferenceType.RANGE:
            return
        sheet: xw.Sheet = self.wb.sheets[range_ref.sheet]
        if sheet is None:
            return
        cell_range = sheet.range(range_ref.reference)
        if cell_range is None:
            return

        rows, cols = cell_range.shape
        for row in range(cell_range.row - 1, rows + cell_range.row - 1):
            for col in range(cell_range.column - 1, cols + cell_range.column - 1):
                xw_cell: xw.Range = sheet[row, col]
                precedent_ref = RangeReference.from_raw(self.wb.name, sheet.name, xw_cell.address)
                if precedent_ref not in self.graph:
                    precedent_cell_range = CellRange(precedent_ref, xw_cell.value, xw_cell.formula)
                    self.graph.add_node(precedent_ref, cell_range=precedent_cell_range)

                self.graph.add_edge(precedent_ref, range_ref)

    def build_dependency_graph(self) -> None:
        for sheet in self.wb.sheets:
            self.parse_worksheet(sheet)

        for named_node in list(node for node in self.graph.nodes if
                               node.reference_type in {RangeReferenceType.DEFINED_NAME_GLOBAL,
                                                       RangeReferenceType.DEFINED_NAME_LOCAL}):

            name: xw.Name
            if named_node.reference_type == RangeReferenceType.DEFINED_NAME_GLOBAL:
                name = self.wb.names[named_node.reference]
            else:
                name = self.wb.sheets[named_node.sheet].names[named_node.reference]
            if not name:
                continue

            named_range: xw.Range = name.refers_to_range
            is_range = named_range.shape[0] > 1 or named_range.shape[1] > 1
            named_range_ref = RangeReference.from_raw(named_range.sheet.book.name, named_range.sheet.name,
                                                      named_range.address,
                                                      RangeReferenceType.RANGE if is_range else RangeReferenceType.CELL)
            if named_range_ref not in self.graph:
                if named_range_ref.reference_type == RangeReferenceType.RANGE:
                    self.graph.add_node(named_range_ref, cell_range=CellRange(named_range_ref, "", ""))
                else:
                    self.graph.add_node(named_range_ref,
                                        cell_range=CellRange(named_range_ref, named_range.value, named_range.formula))
            self.graph.add_edge(named_range_ref, named_node)

        for range_range_ref in list(
                range_ref for range_ref in self.graph.nodes if range_ref.reference_type == RangeReferenceType.RANGE):
            self.add_range_dependencies(range_range_ref)

    def parse_worksheet(self, sheet: xw.Sheet) -> None:
        used_range: xw.Range = sheet.used_range
        if not used_range:
            return

        rows, cols = used_range.shape
        for row in range(used_range.row - 1, rows + used_range.row - 1):
            for col in range(used_range.column - 1, cols + used_range.column - 1):
                cell_range: xw.Range = sheet[row, col]
                if cell_range and cell_range.formula and isinstance(cell_range.formula, str):

                    range_ref = RangeReference.from_raw(cell_range.sheet.book.name, cell_range.sheet.name,
                                                        cell_range.address)
                    if range_ref not in self.graph:
                        self.graph.add_node(range_ref,
                                            cell_range=CellRange(range_ref, cell_range.value, cell_range.formula))

                    precedents_addr = self._extract_precedents(cell_range.formula, sheet.name)
                    for precedent_addr in precedents_addr:
                        if precedent_addr.reference_type == RangeReferenceType.EXTERNAL:
                            self.graph.add_node(precedent_addr)
                        elif not precedent_addr in self.graph:
                            if precedent_addr.reference_type == RangeReferenceType.RANGE:
                                self.graph.add_node(precedent_addr, cell_range=CellRange(precedent_addr, "", ""))
                            else:
                                dep_range: xw.Range = sheet[precedent_addr.reference]
                                self.graph.add_node(precedent_addr,
                                                    cell_range=CellRange(precedent_addr, dep_range.value,
                                                                         dep_range.formula))

                        self.graph.add_edge(precedent_addr, range_ref)

    def _extract_precedents(self, formula: str, current_sheet: str) -> set[RangeReference]:
        dependencies: set[RangeReference] = set()

        for match in self.REFERENCE_RE.finditer(formula):
            workbook = match.group("workbook") or self.wb.name
            sheet = match.group("sheet")
            if sheet:
                sheet = sheet.strip("'").replace("''", "'")  # Unescape Excel sheet names
            else:
                sheet = current_sheet
            address = match.group("address")

            if workbook.lower() != self.wb.name.lower():
                dependencies.add(RangeReference.from_raw(workbook, sheet, address, RangeReferenceType.EXTERNAL))
                continue

            try:
                rn: xw.Range = self.wb.sheets[sheet][address]
                is_range = rn.shape[0] > 1 or rn.shape[1] > 1
                dependencies.add(RangeReference.from_raw(workbook, sheet, rn.address,
                                                         RangeReferenceType.RANGE if is_range else RangeReferenceType.CELL))
            except Exception:
                continue

        # Fallback: find named ranges or Excel functions
        existing_spans = [m.span() for m in self.REFERENCE_RE.finditer(formula)]

        def is_within_existing(match_start: int):
            return any(start <= match_start < end for start, end in existing_spans)

        for m in re.finditer(r'\b[A-Za-z_][A-Za-z0-9_]*\b', formula):
            if is_within_existing(m.start()):
                continue
            name = m.group(0)
            if name in self.wb.names:
                dependencies.add(
                    RangeReference.from_raw(self.wb.name, None, name, RangeReferenceType.DEFINED_NAME_GLOBAL))
            elif name in self.wb.sheets[current_sheet].names:
                dependencies.add(
                    RangeReference.from_raw(self.wb.name, current_sheet, name, RangeReferenceType.DEFINED_NAME_LOCAL))

        return dependencies

    @property
    def REFERENCE_RE(self):
        return re.compile(r"""
        (?:\[(?P<workbook>[^\]]+)\])?           # Optional [Workbook.xlsx]
        (?:(?P<sheet>'[^']+'|[A-Za-z0-9_]+)!)?  # Optional 'Sheet One'! or Sheet1!
        (?P<address>                            # Cell or range
            \$?[A-Z]{1,3}\$?\d+                 # Start cell
            (?::\$?[A-Z]{1,3}\$?\d+)?           # Optional :End cell
        )
    """, re.VERBOSE)
