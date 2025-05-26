import pytest
import xlwings as xw

from model.adapters.excel.connected_excel_workbook import ConnectedExcelWorkbook
from model.adapters.excel.excel_parser_service import ExcelParserService
from model.domain_model.spreadsheet.range_reference import RangeReference, RangeReferenceType


@pytest.fixture
def workbook():
    app = xw.App(visible=False)
    wb = app.books.add()
    yield wb
    wb.close()
    app.quit()


@pytest.fixture
def connected_workbook(workbook):
    return ConnectedExcelWorkbook(workbook)


@pytest.fixture
def parser_service(connected_workbook):
    return ExcelParserService(connected_workbook)


def test_get_dependencies_simple(parser_service, connected_workbook):
    sheet = connected_workbook.get_connected_workbook().sheets[0]
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
    sheet = connected_workbook.get_connected_workbook().sheets[0]
    sheet.range('A1').value = 10
    ref = RangeReference.from_raw(sheet.book.name, sheet.name, 'A1')
    connected_workbook.add_name(ref, 'MyNamedCell')

    dep_graph = parser_service.get_dependencies()

    named_node = RangeReference.from_raw(sheet.book.name, None, 'MyNamedCell', RangeReferenceType.DEFINED_NAME)
    assert dep_graph.get_cell_range(named_node) is not None
    assert dep_graph.get_precedents(named_node) is not None


def test_range_dependencies(parser_service, connected_workbook):
    sheet = connected_workbook.get_connected_workbook().sheets[0]
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
