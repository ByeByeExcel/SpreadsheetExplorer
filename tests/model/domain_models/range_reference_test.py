from model.domain_model.spreadsheet.range_reference import (
    RangeReference,
    RangeReferenceType
)


def test_from_raw_normalization():
    ref = RangeReference.from_raw("Workbook.xlsx", "Sheet1", "$A$1")
    assert ref.workbook == "workbook.xlsx"
    assert ref.sheet == "sheet1"
    assert ref.reference == "A1"
    assert ref.reference_type == RangeReferenceType.CELL


def test_formatted_reference_cell_type():
    ref = RangeReference("book", "sheet", "a1", RangeReferenceType.CELL)
    assert ref.formatted_reference == "A1"


def test_formatted_reference_defined_name():
    ref = RangeReference("book", "sheet", "myNamedRange", RangeReferenceType.DEFINED_NAME)
    assert ref.formatted_reference == "myNamedRange"


def test_equality_and_ordering():
    r1 = RangeReference.from_raw("Book", "Sheet1", "A1")
    r2 = RangeReference.from_raw("book", "sheet1", "$A$1")
    r3 = RangeReference.from_raw("Book", "Sheet1", "B1")

    assert r1 == r2
    assert r1 != r3
    assert r1 < r3
    assert r3 > r1
    assert sorted([r3, r1, r2]) == [r1, r2, r3]


def test_address_key_cell():
    r = RangeReference.from_raw("Book", "Sheet", "C10")
    assert r._address_key() == ("C", 10)


def test_address_key_named_range_fallback():
    r = RangeReference("book", "sheet", "NamedRange", RangeReferenceType.DEFINED_NAME)
    assert r._address_key() == ("NamedRange", 0)


def test_comparison_with_invalid_type():
    r = RangeReference.from_raw("Book", "Sheet1", "A1")
    assert (r.__lt__("not a range ref") is NotImplemented)
