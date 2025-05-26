import networkx as nx
from openpyxl.formula import Tokenizer
from openpyxl.formula.tokenizer import Token

from model.adapters.i_connected_workbook import IConnectedWorkbook
from model.adapters.i_spreadsheet_parser_service import ISpreadsheetParserService
from model.domain_model.spreadsheet.cell_range import CellRange
from model.domain_model.spreadsheet.dependency_graph import DependencyGraph
from model.domain_model.spreadsheet.range_reference import RangeReference, RangeReferenceType
from model.utils.excel_utils import parse_range_reference, get_cell_references_of_range


class ExcelParserService(ISpreadsheetParserService):
    def __init__(self, workbook: IConnectedWorkbook):
        self.wb = workbook
        self.graph: nx.DiGraph[RangeReference] = nx.DiGraph()
        self.names_dict: dict[str, str] = {}

    def get_dependencies(self) -> DependencyGraph:
        self.graph.clear()
        self._build_dependency_graph()
        return DependencyGraph(self.graph)

    def _build_dependency_graph(self) -> None:
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

        for name in self.names_dict:
            defined_ref = self.wb.resolve_defined_name(name)
            if defined_ref:
                if defined_ref not in self.graph:
                    raise ValueError(f"Defined name '{name}' does not resolve to a known range.")

                named_node = RangeReference.from_raw(self.wb.get_workbook_name(), None, name,
                                                     RangeReferenceType.DEFINED_NAME)
                self.graph.add_node(named_node, cell_range=CellRange(named_node, "", ""))
                self.graph.add_edge(defined_ref, named_node)

        for range_ref in [r for r in self.graph.nodes if r.reference_type == RangeReferenceType.RANGE]:
            self._add_range_dependencies(range_ref)

        self.wb.enable_screen_updating()

    def _add_range_dependencies(self, range_ref: RangeReference) -> None:
        if range_ref.reference_type != RangeReferenceType.RANGE:
            return
        cell_references = get_cell_references_of_range(range_ref)
        for cell_reference in cell_references:
            if cell_reference in self.graph:
                self.graph.add_edge(cell_reference, range_ref)

    def _extract_precedents(self, formula: str, current_sheet: str) -> set[RangeReference]:
        if not formula or not formula.strip() or not formula.strip().startswith('='):
            return set()
        dependencies: set[RangeReference] = set()
        wb_name = self.wb.get_workbook_name()

        tokens = Tokenizer(formula)

        for token in tokens.items:
            if token.type == Token.OPERAND and token.subtype == Token.RANGE:
                dependencies.add(parse_range_reference(token.value, wb_name, current_sheet))

        return dependencies
