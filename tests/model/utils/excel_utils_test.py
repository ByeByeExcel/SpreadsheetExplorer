import pytest

from model.domain_model.spreadsheet.range_reference import RangeReference, RangeReferenceType
from model.utils.excel_utils import (
    convert_to_absolute_range, convert_to_absolute_address, replace_cell_reference_in_formula,
    ref_string_is_range, get_address_from_offset, get_address, get_cell_references_of_range,
    parse_range_reference
)


def test_convert_to_absolute_address_and_range():
    assert convert_to_absolute_address('A1') == '$A$1'
    assert convert_to_absolute_range('A1:B2') == '$A$1:$B$2'
    assert convert_to_absolute_range('C3') == '$C$3'


def test_replace_cell_reference_in_formula():
    formula = '=A1 + B1'
    result = replace_cell_reference_in_formula(formula, 'A1', 'MyName')
    assert result == '=MyName + B1'


def test_replace_cell_reference_in_formula_function():
    formula = '=D8 + sum(A1:B3) + C1'
    result = replace_cell_reference_in_formula(formula, 'A1:B3', 'MyName')
    assert result == '=D8 + sum(MyName) + C1'


def test_ref_string_is_range():
    assert ref_string_is_range('A1:B2') is True
    assert ref_string_is_range('A1:A1') is False
    assert ref_string_is_range('C3') is False


def test_get_address_and_offset():
    assert get_address(3, 1) == 'A3'
    assert get_address_from_offset(3, 2, 0, 0) == 'B3'
    assert get_address_from_offset(3, 2, 1, 2) == 'D4'


def test_get_cell_references_of_range():
    range_ref = RangeReference.from_raw('book', 'Sheet1', 'A1:B2', RangeReferenceType.RANGE)
    refs = list(get_cell_references_of_range(range_ref))
    addresses = [ref.reference for ref in refs]
    assert 'A1' in addresses
    assert 'A2' in addresses
    assert 'B1' in addresses
    assert 'B2' in addresses
    assert len(refs) == 4


def test_get_cell_references_of_range_invalid():
    range_ref = RangeReference.from_raw('book', 'Sheet1', 'A1', RangeReferenceType.CELL)
    with pytest.raises(ValueError):
        list(get_cell_references_of_range(range_ref))


def test_parse_range_reference():
    ref = parse_range_reference('A$1', 'book', 'Sheet1')
    assert ref.reference_type == RangeReferenceType.CELL
    assert ref.reference == 'A1'
    assert ref.sheet == 'sheet1'
    assert ref.workbook == 'book'

    ref_range = parse_range_reference('$A$1:$B$2', 'book', 'sheet1')
    assert ref_range.reference_type == RangeReferenceType.RANGE
    assert ref_range.reference == 'A1:B2'
    assert ref_range.sheet == 'sheet1'
    assert ref_range.workbook == 'book'

    ref_name = parse_range_reference('MyNamedRange', 'book', 'Sheet1')
    assert ref_name.reference_type == RangeReferenceType.DEFINED_NAME
    assert ref_name.reference == 'MyNamedRange'
    assert ref_name.sheet == 'sheet1'
    assert ref_name.workbook == 'book'

    ref_external = parse_range_reference('OtherSheet!A1:A1', 'book', 'Sheet1')
    assert ref_external.reference_type == RangeReferenceType.CELL
    assert ref_external.reference == 'A1'
    assert ref_external.sheet == 'othersheet'
    assert ref_external.workbook == 'book'

    ref_external = parse_range_reference('[OtherBook]ExtSheet!A1', 'book', 'Sheet1')
    assert ref_external.reference_type == RangeReferenceType.EXTERNAL
    assert ref_external.reference == 'A1'
    assert ref_external.sheet == 'extsheet'
    assert ref_external.workbook == 'otherbook'
