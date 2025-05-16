import tkinter as tk
from typing import Optional

from model.domain_model.spreadsheet.i_connected_workbook import IConnectedWorkbook
from model.domain_model.spreadsheet.range_reference import RangeReference
from model.services.app_state_service import AppStateService
from model.services.current_range_selection.selection_monitoring import SelectionMonitoring
from model.services.spreadsheet_connection.i_spreadsheet_connection_service import ISpreadsheetConnectionService
from model.services.spreadsheet_parser.excel_parser_service.excel_parser_service_openpyxl import \
    ExcelParserServiceOpenpyxl


class ConnectedWorkbookService:
    selection_monitoring: Optional[SelectionMonitoring] = None

    def __init__(self, connection_service: ISpreadsheetConnectionService, app_state: AppStateService):
        self._connection_service: ISpreadsheetConnectionService = connection_service
        self._app_state: AppStateService = app_state
        self._tk_root: Optional[tk.Tk] = None

        app_state.is_connected_to_workbook.add_observer(self._on_wb_connection_change)

    def set_root(self, tk_root: tk.Tk) -> None:
        self._tk_root = tk_root

    def connect_workbook(self, filename: str) -> None:
        if self._app_state.active_feature.value is not None:
            raise RuntimeError("Cannot connect to workbook while a feature is active.")
        if self._app_state.is_connected_to_workbook.value:
            raise RuntimeError("Already connected to a workbook.")

        workbook: IConnectedWorkbook = self._connection_service.connect_to_workbook(filename)
        if not workbook:
            raise FileNotFoundError(f"Error connecting workbook '{filename}'")

        self._app_state.set_connected_workbook(workbook)

    def disconnect_workbook(self) -> None:
        if self._app_state.active_feature.value is not None:
            raise RuntimeError("Cannot disconnect workbook while a feature is active.")
        self.stop_watching_selected_cell()
        self._app_state.clear_connected_workbook()

    def parse_connected_workbook(self) -> None:
        if self._app_state.active_feature.value is not None:
            raise RuntimeError("Cannot parse workbook while a feature is active.")
        if not self._app_state.is_connected_to_workbook.value:
            raise RuntimeError("No connected workbook to parse.")

        if self._app_state.is_analyzing.value:
            raise RuntimeError("Workbook already analyzing.")

        self._app_state.is_analyzing.set_value(True)
        try:
            workbook: IConnectedWorkbook = self._app_state.get_connected_workbook()
            workbook.set_dependency_graph(ExcelParserServiceOpenpyxl(workbook).get_dependencies())
        finally:
            self._app_state.is_analyzing.set_value(False)

    def start_watching_selected_cell(self):
        self.stop_watching_selected_cell()
        if self._app_state.is_connected_to_workbook.value and self._tk_root:
            selection_monitoring = SelectionMonitoring(
                self._tk_root,
                self._app_state.get_connected_workbook(),
                self._update_selected_range)
            selection_monitoring.start()
            self.selection_monitoring = selection_monitoring

    def stop_watching_selected_cell(self) -> None:
        if self.selection_monitoring:
            self.selection_monitoring.stop()
            self.selection_monitoring = None

    def _update_selected_range(self, new_range_ref: RangeReference) -> None:
        self._app_state.selected_range.set_value(new_range_ref)

    def _on_wb_connection_change(self, is_connected: bool, _):
        if is_connected:
            self.start_watching_selected_cell()
        else:
            self.stop_watching_selected_cell()
