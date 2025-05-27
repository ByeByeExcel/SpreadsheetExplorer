from model.adapters.excel.connected_excel_workbook import ConnectedExcelWorkbook
from model.adapters.excel.excel_connection_service import ExcelConnectionService


def test_get_open_workbooks(excel_app):
    service = ExcelConnectionService()

    # Open a new workbook
    wb = excel_app.books.add()
    wb_name = wb.name

    try:
        open_books = service.get_open_workbooks()
        assert wb_name in open_books
    finally:
        wb.close()


def test_connect_to_workbook(excel_app):
    service = ExcelConnectionService()

    wb = excel_app.books.add()

    try:
        # Connect to the saved workbook
        connected_wb = service.connect_to_workbook(wb.name)
        assert isinstance(connected_wb, ConnectedExcelWorkbook)
        assert connected_wb.name == wb.name

    finally:
        wb.close()
