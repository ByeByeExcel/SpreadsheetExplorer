from model.app_state import AppState
from model.models.i_connected_workbook import IConnectedWorkbook
from model.models.spreadsheet.cell_address import CellAddress
from model.models.spreadsheet.spreadsheet_classes import Cell
from model.utils.utils import replace_cell_reference_in_formula


class RenamingService:
    def __init__(self, app_state: AppState) -> None:
        self._app_state = app_state

    def cascade_name_cell(self, new_name: str, cell: CellAddress):

        workbook: IConnectedWorkbook = self._app_state.get_connected_workbooks().get(cell.workbook.lower())

        if not workbook:
            raise ValueError(f"Workbook {cell.workbook} is not connected.")
        if workbook.get_names().get(new_name):
            raise ValueError(f"Name {new_name} already exists in workbook {cell.workbook}.")

        workbook.add_name(cell, new_name)
        dependents: [CellAddress] = workbook.cell_dependencies.dependents.get(cell)
        if dependents:
            for dependent in dependents:
                if not dependent.is_cell_reference():
                    continue
                dependent_cell: Cell = workbook.get_cell(dependent)
                new_formula = replace_cell_reference_in_formula(dependent_cell.formula, cell.address, new_name)
                workbook.set_formula(dependent, new_formula)
