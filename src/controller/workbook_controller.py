import tkinter as tk

from model.services.connected_workbook_service import ConnectedWorkbookService
from model.services.spreadsheet_connection.i_spreadsheet_connection_service import ISpreadsheetConnectionService


class WorkbookController:
    def __init__(self,
                 connected_workbook_service: ConnectedWorkbookService,
                 connection_service: ISpreadsheetConnectionService) -> None:
        self._connected_workbook_service = connected_workbook_service
        self._connection_service = connection_service

    def get_open_workbooks(self) -> list[str]:
        return self._connection_service.get_open_workbooks()

    def connect_and_parse_workbook(self, filename: str) -> None:
        self._connected_workbook_service.connect_workbook(filename)
        self._connected_workbook_service.parse_connected_workbook()

    def parse_connected_workbook(self) -> None:
        self._connected_workbook_service.parse_connected_workbook()

    def disconnect_workbook(self) -> None:
        self._connected_workbook_service.disconnect_workbook()

    def set_tk_root(self, tk_root: tk.Tk) -> None:
        self._connected_workbook_service.set_root(tk_root)
