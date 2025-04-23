from typing import Optional

from model.app_state import AppState
from model.models.i_connected_workbook import IConnectedWorkbook
from model.models.spreadsheet.cell_address import CellAddress
from model.models.workbook_click_watcher import WorkbookClickWatcher
from model.services.spreadsheet_connection.i_spreadsheet_connection_service import ISpreadsheetConnectionService
from model.services.spreadsheet_parser.excel_parser_service.excel_parser_service import ExcelParserService


class ConnectedWorkbookService:
    _workbook_selected_cell_watcher: Optional[WorkbookClickWatcher] = None

    def __init__(self, connection_service: ISpreadsheetConnectionService, app_state: AppState):
        self.connection_service: ISpreadsheetConnectionService = connection_service
        self._app_state: AppState = app_state

    def connect_workbook(self, filename: str) -> None:
        if self._app_state.active_feature.value is not None:
            raise RuntimeError("Cannot connect to workbook while a feature is active.")
        if self._app_state.is_connected_to_workbook.value:
            raise RuntimeError("Already connected to a workbook.")

        workbook: IConnectedWorkbook = self.connection_service.connect_to_workbook(filename)
        if not workbook:
            raise FileNotFoundError(f"Error connecting workbook '{filename}'")

        self._app_state.set_connected_workbook(workbook)

    def parse_connected_workbook(self) -> None:
        if self._app_state.active_feature.value is not None:
            raise RuntimeError("Cannot parse workbook while a feature is active.")
        if not self._app_state.is_connected_to_workbook.value:
            raise RuntimeError("No connected workbook to parse.")

        if self._app_state.is_analyzing.value:
            raise RuntimeError("Workbook already analyzing.")

        self._app_state.is_analyzing.set_value(True)

        self.stop_watching_selected_cell()
        workbook: IConnectedWorkbook = self._app_state.get_connected_workbook()
        workbook.load()
        workbook.cell_dependencies = ExcelParserService(workbook).get_dependencies()
        self.start_watching_selected_cell()
        self._app_state.is_analyzing.set_value(False)

    def start_watching_selected_cell(self):
        self.stop_watching_selected_cell()
        if self._app_state.is_connected_to_workbook.value:
            watcher = WorkbookClickWatcher(self._app_state.get_connected_workbook(), self._update_selected_cell)
            watcher.start()
            self._workbook_selected_cell_watcher = watcher

    def stop_watching_selected_cell(self) -> None:
        if self._workbook_selected_cell_watcher:
            self._workbook_selected_cell_watcher.stop()
            self._workbook_selected_cell_watcher = None

    def disconnect_workbook(self) -> None:
        if self._app_state.active_feature.value is not None:
            raise RuntimeError("Cannot disconnect workbook while a feature is active.")
        self.stop_watching_selected_cell()
        self._app_state.clear_connected_workbook()

    def _update_selected_cell(self, new_cell: CellAddress) -> None:
        self._app_state.selected_cell.set_value(new_cell)
