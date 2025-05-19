from model.adapters.i_connected_workbook import IConnectedWorkbook
from model.domain_model.feature import Feature
from model.domain_model.spreadsheet.cell_range import CellRange
from model.domain_model.spreadsheet.range_reference import RangeReference, RangeReferenceType
from model.services.app_state_service import AppStateService
from model.utils.excel_utils import replace_cell_reference_in_formula


class RenamingService:
    def __init__(self, app_state: AppStateService) -> None:
        self._app_state = app_state

    def cascade_name_cell(self, new_name: str):
        try:
            workbook: IConnectedWorkbook = self._app_state.get_connected_workbook()
            range_ref: RangeReference = self._app_state.selected_range.value
            if not range_ref:
                raise ValueError("No cell selected.")

            if workbook.get_names().get(new_name):
                raise ValueError(f"Name {new_name} already exists in workbook {range_ref.workbook}.")

            workbook.add_name(range_ref, new_name)
            dependents: set[RangeReference] = workbook.get_dependents(range_ref)
            if dependents:
                for dependent in dependents:
                    if dependent.reference_type != RangeReferenceType.CELL:
                        continue

                    dependent_cell_range: CellRange = workbook.get_range(dependent)

                    if not dependent_cell_range:
                        print(f"[WARNING] Could not find dependent cell {dependent.reference} — skipping.")
                        continue

                    new_formula = replace_cell_reference_in_formula(dependent_cell_range.formula, range_ref.reference,
                                                                    new_name)
                    workbook.set_formula(dependent, new_formula)
        finally:
            self._app_state.set_feature_inactive(Feature.CASCADE_RENAME)
