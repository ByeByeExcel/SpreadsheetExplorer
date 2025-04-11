from model.models.i_connected_workbook import IConnectedWorkbook
from model.models.spreadsheet.spreadsheet_classes import CellDependencies
from model.models.workbook_click_watcher import WorkbookClickWatcher
from model.services.functionality.highlight_precedent_dependent_listener import HighlightCellSelectionListener
from model.services.spreadsheet_connection.excel_connection.excel_connection_service import ExcelConnectionService
from model.services.spreadsheet_connection.i_spreadsheet_connection_service import ISpreadsheetAppConnection
from model.services.spreadsheet_parser.excel_parser_service.excel_parser_service import ExcelParserService
from model.services.spreadsheet_parser.i_spreadsheet_parser_service import ISpreadsheetParserService


class ActiveWorkbookService:
    _connected_workbooks: dict[str, IConnectedWorkbook] = {}
    _workbook_click_watchers: [WorkbookClickWatcher] = []

    def __init__(self):
        self._connection_service: ISpreadsheetAppConnection = ExcelConnectionService()
        self._parser_service: ISpreadsheetParserService = ExcelParserService()

    def get_connection_service(self) -> ISpreadsheetAppConnection:
        return self._connection_service

    def get_parser_service(self) -> ISpreadsheetParserService:
        return self._parser_service

    def get_connected_workbooks(self) -> dict[str, IConnectedWorkbook]:
        return self._connected_workbooks

    def get_connected_workbook(self, filename: str) -> IConnectedWorkbook:
        return self._connected_workbooks.get(filename)

    def is_connected_to_workbook(self) -> bool:
        return bool(self._connected_workbooks)

    def connect_and_parse_workbook(self, filename: str) -> None:
        connected_workbook: IConnectedWorkbook = self._connection_service.connect_to_workbook(filename)
        if not connected_workbook:
            raise Exception(f"Error connecting workbook '{filename}'")
        dependencies: CellDependencies = self._parser_service.get_dependencies(connected_workbook.fullpath)
        connected_workbook.cell_dependencies = dependencies
        self._connected_workbooks[connected_workbook.name] = connected_workbook

    def stop_watchers(self) -> None:
        for watcher in self._workbook_click_watchers:
            watcher.stop()
        self._workbook_click_watchers = []

    def highlight_dependents_precedents(self):
        for connected_workbook in self._connected_workbooks.values():
            listener = HighlightCellSelectionListener(connected_workbook)
            watcher = WorkbookClickWatcher(connected_workbook.connected_workbook)
            self._workbook_click_watchers.append(watcher)
            watcher.start(listener)
