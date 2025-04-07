from model.models.i_connected_workbook import IConnectedWorkbook
from model.services.spreadsheet_connection.excel_connection.excel_connection_service import ExcelConnectionService
from model.services.spreadsheet_connection.i_spreadsheet_connection_service import ISpreadsheetAppConnection


class ActiveWorkbookService:
    _current_workbook: IConnectedWorkbook

    def __init__(self):
        self._connection_service: ISpreadsheetAppConnection = ExcelConnectionService()

    def get_connection_service(self) -> ISpreadsheetAppConnection:
        return self._connection_service

    def connect_to_workbook(self, filename: str):
        self._current_workbook = self._connection_service.connect_to_workbook(filename)

    def get_current_workbook(self):
        return self._current_workbook
