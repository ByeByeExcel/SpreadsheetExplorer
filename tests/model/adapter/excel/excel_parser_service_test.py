import pytest
import xlwings as xw

from model.adapters.excel.connected_excel_workbook import ConnectedExcelWorkbook
from model.adapters.excel.excel_parser_service import ExcelParserService
from model.domain_model.spreadsheet.range_reference import RangeReference, RangeReferenceType
from model.utils.excel_utils import get_cell_references_of_range


@pytest.fixture(scope='session')
def excel_app():
    app = xw.App(visible=False)
    yield app
    app.quit()


@pytest.fixture
def workbook(excel_app):
    wb = excel_app.books.add()
    yield wb
    wb.close()


@pytest.fixture
def connected_workbook(workbook):
    return ConnectedExcelWorkbook(workbook)


@pytest.fixture
def parser_service(connected_workbook):
    return ExcelParserService(connected_workbook)


def test_get_dependencies_simple(parser_service, connected_workbook):
    sheet = connected_workbook._xlwings_book.sheets[0]
    sheet.range('A1').formula = '=1+1'
    dep_graph = parser_service.get_dependencies()

    a1_ref = RangeReference.from_raw(sheet.book.name, sheet.name, 'A1')
    assert dep_graph.get_cell_range(a1_ref) is not None
    assert len(dep_graph.get_precedents(a1_ref)) == 0
    assert len(dep_graph.get_dependents(a1_ref)) == 0


def test_extract_precedents(parser_service):
    formula = '=A1 + B2 + Sheet2!C3 + [Other.xlsx]Sheet1!D4'
    current_sheet = 'Sheet1'
    precedents = parser_service._extract_precedents(formula, current_sheet)

    assert any(p.reference == 'A1' for p in precedents)
    assert any(p.reference == 'B2' for p in precedents)
    assert any(p.sheet == 'Sheet2'.lower() and p.reference == 'C3' for p in precedents)
    assert any(p.reference_type == RangeReferenceType.EXTERNAL for p in precedents)


def test_named_range_dependency(parser_service, connected_workbook):
    sheet = connected_workbook._xlwings_book.sheets[0]
    sheet.range('A1').value = 10
    ref = RangeReference.from_raw(sheet.book.name, sheet.name, 'A1')
    connected_workbook.add_name(ref, 'MyNamedCell')

    dep_graph = parser_service.get_dependencies()

    named_node = RangeReference.from_raw(sheet.book.name, None, 'MyNamedCell', RangeReferenceType.DEFINED_NAME)
    assert dep_graph.get_cell_range(named_node) is not None
    assert dep_graph.get_precedents(named_node) is not None


def test_range_dependencies(parser_service, connected_workbook):
    sheet = connected_workbook._xlwings_book.sheets[0]
    sheet.range('A1').formula = '=SUM(B1:C1)'
    sheet.range('B1').value = 2
    sheet.range('C1').value = 3

    dep_graph = parser_service.get_dependencies()

    a1_ref = RangeReference.from_raw(sheet.book.name, sheet.name, 'A1')
    b1_ref = RangeReference.from_raw(sheet.book.name, sheet.name, 'B1')
    c1_ref = RangeReference.from_raw(sheet.book.name, sheet.name, 'C1')

    b1c1_ref = RangeReference.from_raw(sheet.book.name, sheet.name, 'B1:C1', RangeReferenceType.RANGE)

    assert dep_graph.get_precedents(a1_ref) is not None
    assert b1c1_ref in dep_graph.get_precedents(a1_ref)

    assert dep_graph.get_dependents(b1_ref) is not None
    assert b1c1_ref in dep_graph.get_dependents(b1_ref)

    assert dep_graph.get_dependents(c1_ref) is not None
    assert b1c1_ref in dep_graph.get_dependents(c1_ref)


def test_named_range_resolves_to_cell_level(parser_service, connected_workbook):
    sheet = connected_workbook._xlwings_book.sheets[0]

    # Setup: put values in B1:C3
    for row in range(1, 4):
        for col in ['B', 'C']:
            cell = f"{col}{row}"
            sheet.range(cell).value = row

    # Define named range "TestRange" = B1:C3
    test_range_ref = RangeReference.from_raw(sheet.book.name, sheet.name, 'B1:C3', RangeReferenceType.RANGE)
    connected_workbook.add_name(test_range_ref, 'TestRange')

    # Formula in A1 using named range
    sheet.range('A1').formula = '=SUM(TestRange)'

    dep_graph = parser_service.get_dependencies()

    a1_ref = RangeReference.from_raw(sheet.book.name, sheet.name, 'A1')

    # Get all cell-level references inside B1:C3
    cell_refs = get_cell_references_of_range(test_range_ref)

    precedents = dep_graph.resolve_precedents_to_cell_level(a1_ref)

    # Check that each cell inside TestRange is among A1's precedents
    for cell_ref in cell_refs:
        assert cell_ref in precedents, f"Expected {cell_ref} to be precedent of {a1_ref}"
        dependents = dep_graph.resolve_dependents_to_cell_level(cell_ref)
        assert a1_ref in dependents, f"Expected {a1_ref} to be dependent of {cell_ref}"
