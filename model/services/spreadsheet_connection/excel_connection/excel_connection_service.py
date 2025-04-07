import xlwings as xw

from model.models.spreadsheet.excel.excel_workbook import ConnectedExcelWorkbook
from model.services.spreadsheet_connection.excel_connection.utils import convert_xlwings_book
from model.services.spreadsheet_connection.i_spreadsheet_connection_service import ISpreadsheetAppConnection


class ExcelConnectionService(ISpreadsheetAppConnection):
    def get_open_workbooks(self) -> [str]:
        app = xw.apps.active
        return [book.name for book in app.books]

    def connect_to_workbook(self, filename: str) -> ConnectedExcelWorkbook:
        xlwings_excel = xw.Book(filename)
        return convert_xlwings_book(xlwings_excel)
