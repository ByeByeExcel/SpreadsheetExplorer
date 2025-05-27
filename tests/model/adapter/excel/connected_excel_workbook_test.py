import pytest

from model.adapters.excel.connected_excel_workbook import ConnectedExcelWorkbook
from model.domain_model.spreadsheet.range_reference import RangeReference
from model.utils.color_utils import get_hex_color_from_tuple


@pytest.fixture
def workbook(excel_app):
    wb = excel_app.books.add()
    yield wb
    wb.close()


@pytest.fixture
def connected_workbook(workbook):
    return ConnectedExcelWorkbook(workbook)


def test_get_workbook_name(connected_workbook):
    assert connected_workbook.get_workbook_name() == connected_workbook._xlwings_book.name


def test_add_and_resolve_name(connected_workbook):
    sheet = connected_workbook._xlwings_book.sheets[0]
    ref = RangeReference.from_raw(sheet.book.name, sheet.name, 'A1')
    connected_workbook.add_name(ref, 'TestName')
    resolved = connected_workbook.resolve_defined_name('TestName')
    assert resolved.reference == 'A1'


def test_set_and_get_formula(connected_workbook):
    sheet = connected_workbook._xlwings_book.sheets[0]
    ref = RangeReference.from_raw(sheet.book.name, sheet.name, 'A1')
    connected_workbook.set_formula(ref, '=1+1')
    value, formula = connected_workbook.resolve_range_reference(ref)
    assert formula == '=1+1'
    assert value == 2


def test_set_and_get_range_color(connected_workbook):
    sheet = connected_workbook._xlwings_book.sheets[0]
    ref = RangeReference.from_raw(sheet.book.name, sheet.name, 'A1')
    connected_workbook.set_ranges_color([ref], (255, 0, 0))  # Red
    color = connected_workbook.get_range_color(ref)
    assert color is not None
    assert color == '#ff0000'


def test_get_names(connected_workbook):
    sheet = connected_workbook._xlwings_book.sheets[0]
    ref1 = RangeReference.from_raw(sheet.book.name, sheet.name, 'A1')
    ref2 = RangeReference.from_raw(sheet.book.name, sheet.name, 'B2:C5')
    connected_workbook.add_name(ref1, 'MyTestName1')
    connected_workbook.add_name(ref2, 'MyTestName2')
    names = connected_workbook.get_names()
    assert 'MyTestName1' in names
    assert 'MyTestName2' in names


def test_get_used_range(connected_workbook):
    sheet = connected_workbook._xlwings_book.sheets[0]
    sheet.range('A1').value = 'test1'
    sheet.range('A2').value = 'test2'
    sheet.range('B1').formula = '=A1'

    used_ranges = list(connected_workbook.get_used_range())

    # Check that at least two cells are reported (A1 and A2)
    addresses = [ref.reference.upper() for ref, _, _ in used_ranges]
    assert 'A1' in addresses
    assert 'A2' in addresses
    assert 'B1' in addresses
    assert 'B2' in addresses

    # Check that values are correct
    values = {ref.reference: val for ref, val, _ in used_ranges}
    assert values['A1'] == 'test1'
    assert values['A2'] == 'test2'
    assert values['B1'] == 'test1'
    assert values['B2'] is None

    # Check that formulas are correct
    formulas = {ref.reference: formula for ref, _, formula in used_ranges}
    assert formulas['B1'] == '=A1'


def test_initial_to_grayscale_and_set_from_dict_and_return_initial_colors(connected_workbook):
    sheet = connected_workbook._xlwings_book.sheets[0]

    # Set some initial colors
    sheet.range('A1').color = (255, 0, 0)  # Red
    sheet.range('A2').color = (0, 255, 0)  # Green

    ref_a1 = RangeReference.from_raw(sheet.book.name, sheet.name, 'A1')
    ref_a2 = RangeReference.from_raw(sheet.book.name, sheet.name, 'A2')

    # Provide a new color only for A1, A2 will be grayscaled
    new_colors = {ref_a1: (0, 0, 255)}  # Blue

    initial_colors = connected_workbook.initial_to_grayscale_and_set_from_dict_and_return_initial_colors(new_colors)

    # Check that initial color was stored
    assert ref_a1 in initial_colors
    assert ref_a2 in initial_colors
    assert initial_colors[ref_a1] == get_hex_color_from_tuple((255, 0, 0))
    assert initial_colors[ref_a2] == get_hex_color_from_tuple((0, 255, 0))

    # Verify that A1 is now blue and A2 is now gray
    assert sheet.range('A1').color == (0, 0, 255)
    assert sheet.range('A2').color != (0, 255, 0)
