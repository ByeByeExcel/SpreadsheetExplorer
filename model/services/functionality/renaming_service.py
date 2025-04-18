from model.app_state import AppState
from model.feature import Feature
from model.models.i_connected_workbook import IConnectedWorkbook
from model.models.spreadsheet.cell_address import CellAddress
from model.models.spreadsheet.spreadsheet_classes import Cell
from model.utils.utils import replace_cell_reference_in_formula


class RenamingService:
    def __init__(self, app_state: AppState) -> None:
        self._app_state = app_state

    def cascade_name_cell(self, new_name: str):
        if not self._app_state.can_start_feature():
            raise ValueError("Can not start cascade renaming.")
        self._app_state.set_feature_active(Feature.CASCADE_RENAME)

        try:
            workbook: IConnectedWorkbook = self._app_state.get_connected_workbook()
            cell: CellAddress = self._app_state.selected_cell.value
            if not cell:
                raise ValueError("No cell selected.")

            if workbook.get_names().get(new_name):
                raise ValueError(f"Name {new_name} already exists in workbook {cell.workbook}.")

            workbook.add_name(cell, new_name)
            dependents: set[CellAddress] = workbook.cell_dependencies.dependents.get(cell)
            if dependents:
                for dependent in dependents:
                    if not dependent.is_cell_reference():
                        continue

                    dependent_cell: Cell = workbook.get_cell(dependent)

                    if not dependent_cell:
                        print(f"[WARNING] Could not find dependent cell {dependent.address} — skipping.")
                        continue

                    new_formula = replace_cell_reference_in_formula(dependent_cell.formula, cell.address, new_name)
                    workbook.set_formula(dependent, new_formula)
        finally:
            self._app_state.set_feature_inactive(Feature.CASCADE_RENAME)
