import os
import tempfile

import openpyxl as pxl
import pytest

from model.services.spreadsheet_parser.excel_parser_service.excel_parser_service import ExcelParserService


@pytest.fixture
def simple_excel_sheet():
    fd, path = tempfile.mkstemp(suffix=".xlsx")
    os.close(fd)

    workbook = pxl.Workbook()
    worksheet = workbook.active

    worksheet["A1"] = 5
    worksheet["A2"] = 6
    worksheet["A3"] = "=A1*A2"
    worksheet["A4"] = "=SUM(A1:A3)"
    worksheet["A5"] = "=SUM(A1:A3) + A1 - 2"
    worksheet["A6"] = "=SUM(B3) + A1 - 2"

    workbook.save(path)

    yield path
    os.remove(path)


def test_excel_loading(simple_excel_sheet):
    dependencies = ExcelParserService().get_dependencies(simple_excel_sheet)
    # assert len(dependencies.dependents) == 3
    # assert len(dependencies.precedents) == 2
    print(dependencies.dependents)
    print(dependencies.precedents)
