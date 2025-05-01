import xlwings as xw

from model.domain_model.i_connected_workbook import IConnectedWorkbook
from model.domain_model.spreadsheet.excel.connected_excel_workbook import ConnectedExcelWorkbook
from model.services.spreadsheet_connection.i_spreadsheet_connection_service import ISpreadsheetConnectionService


class ExcelConnectionService(ISpreadsheetConnectionService):
    def get_open_workbooks(self) -> list[str]:
        app = xw.apps.active
        if not app:
            raise RuntimeError('Excel is not running.')
        return [book.name for book in app.books]

    def connect_to_workbook(self, filename: str) -> IConnectedWorkbook:
        xlwings_excel = xw.Book(filename)
        return ConnectedExcelWorkbook(xlwings_excel)
