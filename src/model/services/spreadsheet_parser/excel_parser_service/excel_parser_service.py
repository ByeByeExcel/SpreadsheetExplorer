import re

import networkx as nx

from model.domain_model.spreadsheet.cell_range import CellRange
from model.domain_model.spreadsheet.dependency_graph import DependencyGraph
from model.domain_model.spreadsheet.i_connected_workbook import IConnectedWorkbook
from model.domain_model.spreadsheet.range_reference import RangeReference, RangeReferenceType
from model.services.spreadsheet_parser.i_spreadsheet_parser_service import ISpreadsheetParserService
from model.utils.excel_utils import ref_string_is_range


class ExcelParserService(ISpreadsheetParserService):
    def __init__(self, workbook: IConnectedWorkbook):
        self.wb = workbook
        self.graph: nx.DiGraph[RangeReference] = nx.DiGraph()
        self.names_dict:dict[str, str] = {}

    def get_dependencies(self) -> DependencyGraph:
        self.graph.clear()
        self.build_dependency_graph()
        return DependencyGraph(self.graph)

    def build_dependency_graph(self) -> None:
        self.names_dict = self.wb.get_names()
        self.wb.disable_screen_updating()
        for ref, val, formula in self.wb.get_used_range():
            self.graph.add_node(ref, cell_range=CellRange(ref, val, formula))

        for node in list(self.graph.nodes):
            precedents = self._extract_precedents(self.graph.nodes[node]['cell_range'].formula, node.sheet)
            for precedent in precedents:
                if precedent not in self.graph:
                    if precedent.reference_type == RangeReferenceType.RANGE:
                        self.graph.add_node(precedent, cell_range=CellRange(precedent, "", ""))
                    else:
                        value, formula = self.wb.resolve_range_reference(precedent)
                        self.graph.add_node(precedent, cell_range=CellRange(precedent, value, formula))
                self.graph.add_edge(precedent, node)

        for name, _ in self.names_dict.items():
            defined_ref = self.wb.resolve_defined_name(name)
            if defined_ref:
                if defined_ref not in self.graph:
                    if defined_ref.reference_type == RangeReferenceType.RANGE:
                        self.graph.add_node(defined_ref, cell_range=CellRange(defined_ref, "", ""))
                    else:
                        value, formula = self.wb.resolve_range_reference(defined_ref)
                        self.graph.add_node(defined_ref, cell_range=CellRange(defined_ref, value, formula))

                named_node = RangeReference.from_raw(self.wb.get_workbook_name(), None, name,
                                                     RangeReferenceType.DEFINED_NAME)
                self.graph.add_edge(defined_ref, named_node)

        for range_ref in [r for r in self.graph.nodes if r.reference_type == RangeReferenceType.RANGE]:
            self._add_range_dependencies(range_ref)

        self.wb.enable_screen_updating()

    def _add_range_dependencies(self, range_ref: RangeReference) -> None:
        if range_ref.reference_type != RangeReferenceType.RANGE:
            return
        cells = self.wb.get_cells_in_range(range_ref)
        for cell in cells:
            if cell.reference not in self.graph:
                self.graph.add_node(cell.reference, cell_range=cell)
            self.graph.add_edge(cell.reference, range_ref)

    def _extract_precedents(self, formula: str, current_sheet: str) -> set[RangeReference]:
        if not formula or not formula.strip() or not formula.strip().startswith('='):
            return set()
        dependencies: set[RangeReference] = set()
        wb_name = self.wb.get_workbook_name()

        for match in self.REFERENCE_RE.finditer(formula):
            workbook = match.group("workbook") or wb_name
            sheet = match.group("sheet")
            if sheet:
                sheet = sheet.strip("'").replace("''", "'")
            else:
                sheet = current_sheet
            address = match.group("address")

            if workbook.lower() != wb_name.lower():
                dependencies.add(RangeReference.from_raw(workbook, sheet, address, RangeReferenceType.EXTERNAL))
                continue

            try:
                ref_type = RangeReferenceType.RANGE if ref_string_is_range(address) else RangeReferenceType.CELL
                dependencies.add(RangeReference.from_raw(workbook, sheet, address, ref_type))
            except Exception:
                continue

        existing_spans = [m.span() for m in self.REFERENCE_RE.finditer(formula)]

        def is_within_existing(pos: int):
            return any(start <= pos < end for start, end in existing_spans)

        for m in re.finditer(r'\b[A-Za-z_][A-Za-z0-9_]*\b', formula):
            if is_within_existing(m.start()):
                continue
            name = m.group(0)
            if name in self.names_dict:
                dependencies.add(RangeReference.from_raw(wb_name, None, name, RangeReferenceType.DEFINED_NAME))

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
