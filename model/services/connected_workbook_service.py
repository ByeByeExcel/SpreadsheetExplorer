from model.app_state import AppState
from model.models.i_connected_workbook import IConnectedWorkbook
from model.models.spreadsheet.cell_address import CellAddress
from model.models.spreadsheet.spreadsheet_classes import CellDependencies
from model.models.workbook_click_watcher import WorkbookClickWatcher
from model.services.spreadsheet_connection.i_spreadsheet_connection_service import ISpreadsheetConnectionService
from model.services.spreadsheet_parser.i_spreadsheet_parser_service import ISpreadsheetParserService


class ConnectedWorkbookService:
    _workbook_click_watchers: [WorkbookClickWatcher] = []

    def __init__(self, connection_service: ISpreadsheetConnectionService, parser_service: ISpreadsheetParserService,
                 app_state: AppState):
        self._connection_service: ISpreadsheetConnectionService = connection_service
        self._parser_service: ISpreadsheetParserService = parser_service
        self._app_state: AppState = app_state

    def get_connection_service(self) -> ISpreadsheetConnectionService:
        return self._connection_service

    def get_parser_service(self) -> ISpreadsheetParserService:
        return self._parser_service

    def connect_and_parse_workbook(self, filename: str) -> None:
        connected_workbook: IConnectedWorkbook = self._connection_service.connect_to_workbook(filename)
        if not connected_workbook:
            raise Exception(f"Error connecting workbook '{filename}'")
        dependencies: CellDependencies = self._parser_service.get_dependencies(connected_workbook.fullpath)
        connected_workbook.cell_dependencies = dependencies
        self._app_state.connected_workbook = connected_workbook
        self.start_watching_selected_cell()

    def start_watching_selected_cell(self):
        self.stop_watching_selected_cell()
        if self._app_state.connected_workbook:
            watcher = WorkbookClickWatcher(self._app_state.connected_workbook, self._update_selected_cell)
            watcher.start()
            self._workbook_click_watchers.append(watcher)

    def stop_watching_selected_cell(self) -> None:
        for watcher in self._workbook_click_watchers:
            watcher.stop()
        self._workbook_click_watchers = []

    def disconnect_all_workbooks(self) -> None:
        self.stop_watching_selected_cell()
        self._app_state.selected_cell.remove_all_observers()

    def _update_selected_cell(self, new_cell: CellAddress) -> None:
        self._app_state.selected_cell.set_value(new_cell)
