import os
import tempfile

import openpyxl as pxl
import pytest

from model.services.spreadsheet_connection.excel_connection.excel_connection_service import ExcelConnectionService


@pytest.fixture
def simple_excel_sheet():
    fd, path = tempfile.mkstemp(suffix=".xlsx")
    os.close(fd)

    workbook = pxl.Workbook()
    worksheet = workbook.active

    worksheet["A1"] = 5
    worksheet["A2"] = 6
    worksheet["A3"] = "=A1*A2"

    workbook.save(path)

    yield path
    os.remove(path)


def test_excel_loading(simple_excel_sheet):
    workbook = ExcelConnectionService().connect_to_workbook(simple_excel_sheet)
    assert workbook is not None
    assert workbook.worksheets["Sheet"] is not None
    # assert workbook.worksheets["Sheet"].cells["$A$3"] is not None
    # assert workbook.worksheets["Sheet"].cells["$A$3"].value == 30

    workbook.connected_workbook.close()

# def test_set_cell_color(simple_excel_sheet):
#     workbook = ExcelConnectionService().connect_to_workbook(simple_excel_sheet)
#     assert workbook is not None
#     ws = workbook.worksheets["Sheet"]
#     c = ws.cells["$A$3"]
#     workbook.set_range_color(ws, c, webcolors.name_to_hex('red'))
