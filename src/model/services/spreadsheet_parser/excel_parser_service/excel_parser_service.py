import re

import networkx as nx
import xlwings as xw

from model.models.i_connected_workbook import IConnectedWorkbook
from model.models.spreadsheet.cell import Cell
from model.models.spreadsheet.cell_address import CellAddress, CellAddressType
from model.models.spreadsheet.dependency_graph import DependencyGraph
from model.services.spreadsheet_parser.i_spreadsheet_parser_service import ISpreadsheetParserService


class ExcelParserService(ISpreadsheetParserService):

    def __init__(self, connected_workbook: IConnectedWorkbook):
        self.wb = xw.Book(connected_workbook.name)
        self.graph: nx.DiGraph[CellAddress] = nx.DiGraph()

    def get_dependencies(self) -> DependencyGraph:
        self.graph.clear()
        self.build_dependency_graph()

        return DependencyGraph(self.graph)

    def add_range_dependencies(self, range_address: CellAddress) -> None:
        if range_address is None or range_address.address_type != CellAddressType.RANGE:
            return
        sheet: xw.Sheet = self.wb.sheets[range_address.sheet]
        if sheet is None:
            return
        cell_range = sheet.range(range_address.address)
        if cell_range is None:
            return

        rows, cols = cell_range.shape
        for row in range(cell_range.row - 1, rows + cell_range.row - 1):
            for col in range(cell_range.column - 1, cols + cell_range.column - 1):
                xw_cell: xw.Range = sheet[row, col]
                cell_address = CellAddress(self.wb.name, sheet.name, xw_cell.address)
                if cell_address not in self.graph:
                    custom_cell = Cell(cell_address, xw_cell.value, xw_cell.formula)
                    self.graph.add_node(cell_address, cell=custom_cell)

                self.graph.add_edge(cell_address, range_address)

    def build_dependency_graph(self) -> None:
        for sheet in self.wb.sheets:
            self.parse_worksheet(sheet)

        for named_node in list(node for node in self.graph.nodes if
                               node.address_type in {CellAddressType.DEFINED_NAME_GLOBAL,
                                                     CellAddressType.DEFINED_NAME_LOCAL}):

            name: xw.Name
            if named_node.address_type == CellAddressType.DEFINED_NAME_GLOBAL:
                name = self.wb.names[named_node.address]
            else:
                name = self.wb.sheets[named_node.sheet].names[named_node.address]
            if not name:
                continue

            named_range: xw.Range = name.refers_to_range
            is_range = named_range.shape[0] > 1 or named_range.shape[1] > 1
            named_cell_address = CellAddress(named_range.sheet.book.name, named_range.sheet.name, named_range.address,
                                             CellAddressType.RANGE if is_range else CellAddressType.CELL)
            if named_cell_address not in self.graph:
                if named_cell_address.address_type == CellAddressType.RANGE:
                    self.graph.add_node(named_cell_address, cell=Cell(named_cell_address, "", ""))
                else:
                    self.graph.add_node(named_cell_address,
                                        cell=Cell(named_cell_address, named_range.value, named_range.formula))
            self.graph.add_edge(named_cell_address, named_node)

        for range_node in list(node for node in self.graph.nodes if node.address_type == CellAddressType.RANGE):
            self.add_range_dependencies(range_node)

    def parse_worksheet(self, sheet: xw.Sheet) -> None:
        used_range: xw.Range = sheet.used_range
        if not used_range:
            return

        rows, cols = used_range.shape
        for row in range(used_range.row - 1, rows + used_range.row - 1):
            for col in range(used_range.column - 1, cols + used_range.column - 1):
                cell: xw.Range = sheet[row, col]
                if cell and cell.formula and isinstance(cell.formula, str) and cell.formula.startswith('='):

                    cell_address = CellAddress(cell.sheet.book.name, cell.sheet.name, cell.address)
                    if cell_address not in self.graph:
                        self.graph.add_node(cell_address, cell=Cell(cell_address, cell.value, cell.formula))

                    precedents_addr = self._extract_precedents(cell.formula, sheet.name)
                    for precedent_addr in precedents_addr:
                        if precedent_addr.address_type == CellAddressType.EXTERNAL:
                            self.graph.add_node(precedent_addr)
                        elif not precedent_addr in self.graph:
                            if precedent_addr.address_type == CellAddressType.RANGE:
                                self.graph.add_node(precedent_addr, cell=Cell(precedent_addr, "", ""))
                            else:
                                dep_range: xw.Range = sheet[precedent_addr.address]
                                self.graph.add_node(precedent_addr,
                                                    cell=Cell(precedent_addr, dep_range.value, dep_range.formula))

                        self.graph.add_edge(precedent_addr, cell_address)

    def _extract_precedents(self, formula: str, current_sheet: str) -> set[CellAddress]:
        dependencies: set[CellAddress] = set()

        for match in self.REFERENCE_RE.finditer(formula):
            workbook = match.group("workbook") or self.wb.name
            sheet = match.group("sheet")
            if sheet:
                sheet = sheet.strip("'").replace("''", "'")  # Unescape Excel sheet names
            else:
                sheet = current_sheet
            address = match.group("address")

            if workbook.lower() != self.wb.name.lower():
                dependencies.add(CellAddress(workbook, sheet, address, CellAddressType.EXTERNAL))
                continue

            try:
                rn: xw.Range = self.wb.sheets[sheet][address]
                is_range = rn.shape[0] > 1 or rn.shape[1] > 1
                dependencies.add(CellAddress(workbook, sheet, rn.address,
                                             CellAddressType.RANGE if is_range else CellAddressType.CELL))
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
                dependencies.add(CellAddress(self.wb.name, None, name, CellAddressType.DEFINED_NAME_GLOBAL))
            elif name in self.wb.sheets[current_sheet].names:
                dependencies.add(CellAddress(self.wb.name, current_sheet, name, CellAddressType.DEFINED_NAME_LOCAL))

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
