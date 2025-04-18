import xlwings as xw

from src.model.models.i_connected_workbook import IConnectedWorkbook
from src.model.models.spreadsheet.excel.excel_workbook import ConnectedExcelWorkbook
from src.model.services.spreadsheet_connection.i_spreadsheet_connection_service import ISpreadsheetConnectionService


class ExcelConnectionService(ISpreadsheetConnectionService):
    def get_open_workbooks(self) -> list[str]:
        app = xw.apps.active
        if not app:
            raise Exception('Excel is not running.')
        return [book.name for book in app.books]

    def connect_to_workbook(self, filename: str) -> IConnectedWorkbook:
        xlwings_excel = xw.Book(filename)
        return ConnectedExcelWorkbook(xlwings_excel)
