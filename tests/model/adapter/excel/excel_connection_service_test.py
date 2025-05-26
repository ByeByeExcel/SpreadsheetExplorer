import xlwings as xw

from model.adapters.excel.connected_excel_workbook import ConnectedExcelWorkbook
from model.adapters.excel.excel_connection_service import ExcelConnectionService


def test_get_open_workbooks(tmp_path):
    service = ExcelConnectionService()

    # Open a new workbook
    app = xw.App(visible=False)
    wb = app.books.add()
    wb_name = wb.name

    try:
        open_books = service.get_open_workbooks()
        assert wb_name in open_books
    finally:
        wb.close()
        app.quit()


def test_connect_to_workbook(tmp_path):
    service = ExcelConnectionService()

    # Create a temporary Excel file
    app = xw.App(visible=False)
    wb = app.books.add()

    try:
        # Connect to the saved workbook
        connected_wb = service.connect_to_workbook(wb.name)
        assert isinstance(connected_wb, ConnectedExcelWorkbook)
        assert connected_wb.get_workbook_name() == wb.name

    finally:
        wb.close()
        app.quit()
