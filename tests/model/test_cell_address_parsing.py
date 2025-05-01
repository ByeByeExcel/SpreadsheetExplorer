from model.domain_model.spreadsheet.range_reference import RangeReference


def test_parsing_1():
    a = RangeReference.from_excel_ref("[Book1.xlsx]Sheet1!A1")
    assert a is not None
    assert a.workbook == "book1.xlsx"
    assert a.sheet == "sheet1"
    assert a.reference == "a1"


def test_parsing_2():
    a = RangeReference.from_excel_ref("'[Book1.xlsx]SHEET1'!$A$1")
    assert a is not None
    assert a.workbook == "book1.xlsx"
    assert a.sheet == "sheet1"
    assert a.reference == "a1"
