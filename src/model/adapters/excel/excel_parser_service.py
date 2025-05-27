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
        self._wb = workbook
        self._graph: nx.DiGraph[RangeReference] = nx.DiGraph()
        self._names_dict: dict[str, str] = {}

    def get_dependencies(self) -> DependencyGraph:
        self._graph.clear()
        self._build_dependency_graph()
        return DependencyGraph(self._graph)

    def _build_dependency_graph(self) -> None:
        self._names_dict = self._wb.get_names()
        self._wb.disable_screen_updating()

        for ref, val, formula in self._wb.get_used_range():
            self._graph.add_node(ref, cell_range=CellRange(ref, val, formula))

        for node in list(self._graph.nodes):
            precedents = self._extract_precedents(self._graph.nodes[node]['cell_range'].formula, node.sheet)
            for precedent in precedents:
                if precedent not in self._graph:
                    if precedent.reference_type == RangeReferenceType.CELL:
                        raise ValueError(f"Precedent '{precedent}' is a cell reference, which should already be in the dependency graph.")
                    else:
                        self._graph.add_node(precedent, cell_range=CellRange(precedent, "", ""))
                self._graph.add_edge(precedent, node)

        for name in self._names_dict:
            defined_ref = self._wb.resolve_defined_name(name)
            if defined_ref:
                if defined_ref not in self._graph:
                    if defined_ref.reference_type == RangeReferenceType.CELL:
                        raise ValueError(f"Defined name '{name}' refers to a cell, which should already be in the dependency graph.")
                    else:
                        self._graph.add_node(defined_ref, cell_range=CellRange(defined_ref, "", ""))

                named_node = RangeReference.from_raw(self._wb.name, None, name,
                                                     RangeReferenceType.DEFINED_NAME)
                self._graph.add_node(named_node, cell_range=CellRange(named_node, "", ""))
                self._graph.add_edge(defined_ref, named_node)

        for range_ref in [r for r in self._graph.nodes if r.reference_type == RangeReferenceType.RANGE]:
            self._add_range_dependencies(range_ref)

        self._wb.enable_screen_updating()

    def _add_range_dependencies(self, range_ref: RangeReference) -> None:
        if range_ref.reference_type != RangeReferenceType.RANGE:
            return
        cell_references = get_cell_references_of_range(range_ref)
        for cell_reference in cell_references:
            if cell_reference in self._graph:
                self._graph.add_edge(cell_reference, range_ref)

    def _extract_precedents(self, formula: str, current_sheet: str) -> set[RangeReference]:
        if not formula or not formula.strip() or not formula.strip().startswith('='):
            return set()
        dependencies: set[RangeReference] = set()
        wb_name = self._wb.name

        tokens = Tokenizer(formula)

        for token in tokens.items:
            if token.type == Token.OPERAND and token.subtype == Token.RANGE:
                dependencies.add(parse_range_reference(token.value, wb_name, current_sheet))

        return dependencies
