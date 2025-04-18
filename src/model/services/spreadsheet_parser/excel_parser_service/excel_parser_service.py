import re

import networkx as nx
import xlwings as xw

from src.model.models.i_connected_workbook import IConnectedWorkbook
from src.model.models.spreadsheet.cell_address import CellAddress, CellAddressType
from src.model.models.spreadsheet.spreadsheet_classes import CellDependencies
from src.model.services.spreadsheet_connection.excel_connection.xlwings_utils import convert_xlwings_address
from src.model.services.spreadsheet_parser.i_spreadsheet_parser_service import ISpreadsheetParserService


class ExcelParserService(ISpreadsheetParserService):

    def __init__(self, connected_workbook: IConnectedWorkbook):
        self.wb = xw.Book(connected_workbook.name)
        self.graph: nx.DiGraph[CellAddress] = nx.DiGraph()

    def get_dependencies(self) -> CellDependencies:
        self.graph.clear()
        self.build_dependency_graph()
        dependencies = CellDependencies()

        for cell in self.graph.nodes():
            precedents = self.get_precedents(cell)
            dependents = self.get_dependents(cell)

            if precedents:
                dependencies.precedents[cell] = precedents
            if dependents:
                dependencies.dependents[cell] = dependents

        return dependencies

    def add_range_dependencies(self, cell: CellAddress) -> None:
        if cell is None or cell.address_type != CellAddressType.RANGE:
            return

        sheet: xw.Sheet = self.wb.sheets[cell.sheet]
        cell_range = sheet.range(cell.address)
        if cell_range is None or sheet is None:
            return

        rows, cols = cell_range.shape
        for row in range(cell_range.row - 1, rows + cell_range.row - 1):
            for col in range(cell_range.column - 1, cols + cell_range.column - 1):
                xw_cell: xw.Range = sheet[row, col]
                cell_address = CellAddress(self.wb.name, sheet.name, xw_cell.address)

                self.graph.add_edge(cell_address, cell)

    def build_dependency_graph(self) -> None:
        for sheet in self.wb.sheets:
            self.parse_worksheet(sheet)

        for cell in list(self.graph.nodes()):
            if cell.address_type == CellAddressType.DEFINED_NAME_GLOBAL:
                self.graph.add_edge(convert_xlwings_address(self.wb.names[cell.address].refers_to_range), cell)

            if cell.address_type == CellAddressType.DEFINED_NAME_LOCAL:
                self.graph.add_edge(
                    convert_xlwings_address(self.wb.sheets[cell.sheet].names[cell.address].refers_to_range), cell)

        for cell in list(self.graph.nodes()):
            if cell.address_type == CellAddressType.RANGE:
                self.add_range_dependencies(cell)

    def parse_worksheet(self, sheet: xw.Sheet) -> None:
        used_range: xw.Range = sheet.used_range
        if not used_range:
            return

        rows, cols = used_range.shape
        for row in range(used_range.row - 1, rows + used_range.row - 1):
            for col in range(used_range.column - 1, cols + used_range.column - 1):
                cell: xw.Range = sheet[row, col]
                if cell.formula and isinstance(cell.formula, str) and cell.formula.startswith('='):
                    cell_address = CellAddress(self.wb.name, sheet.name, cell.address)
                    dependencies = self._extract_dependencies(cell.formula, sheet.name)
                    for dep in dependencies:
                        self.graph.add_edge(dep, cell_address)

    def _extract_dependencies(self, formula: str, current_sheet: str) -> set[CellAddress]:
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

    def get_precedents(self, cell: CellAddress) -> set[CellAddress]:
        if cell in self.graph:
            return set(self.graph.predecessors(cell))
        return set()

    def get_dependents(self, cell: CellAddress) -> set[CellAddress]:
        if cell in self.graph:
            return set(self.graph.successors(cell))
        return set()

    @property
    def REFERENCE_RE(self):
        return re.compile(r"""
            (                           # Full reference
                (?:\[(?P<workbook>[^]]+)])?          # [Workbook.xlsx]
                (?:(?P<sheet>'[^']+'|[^'!]+)!)?        # Sheet name, quoted or not
                (?P<address>\$?[A-Z]{1,3}\$?\d+(?::\$?[A-Z]{1,3}\$?\d+)?)  # A1 or A1:B2
            )
        """, re.VERBOSE)
