from model.models.spreadsheet.cell_address import CellAddress


def test_parsing_1():
    a = CellAddress.from_excel_ref("[Book1.xlsx]Sheet1!A1")
    assert a is not None
    assert a.workbook == "book1.xlsx"
    assert a.sheet == "sheet1"
    assert a.address == "a1"

def test_parsing_2():
    a = CellAddress.from_excel_ref("'[Book1.xlsx]SHEET1'!$A$1")
    assert a is not None
    assert a.workbook == "book1.xlsx"
    assert a.sheet == "sheet1"
    assert a.address == "a1"