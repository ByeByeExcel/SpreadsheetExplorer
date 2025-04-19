from typing import Optional

from model.models.formula_context_information import FormulaContextInformation, RangeInformation
from model.models.i_connected_workbook import IConnectedWorkbook
from model.models.spreadsheet.cell_address import CellAddress, CellAddressType
from model.services.functionality.interactive_painting.selection_listener.i_selection_observer import \
    ISelectionObserver
from model.utils.observable_value import ObservableValue


class BasicContextGenerationObserver(ISelectionObserver):

    def __init__(self, workbook: IConnectedWorkbook,
                 formula_context_information_observable: ObservableValue[Optional[FormulaContextInformation]]):
        self.workbook = workbook
        self._formula_context_information = formula_context_information_observable

    def __call__(self, new_cell: Optional[CellAddress], old_cell: Optional[CellAddress]):
        if not new_cell:
            self._formula_context_information.set_value(None)
            return
        if new_cell.workbook != self.workbook.name.lower():
            return

        precedents_information: list[RangeInformation] = []
        if new_cell.address_type == CellAddressType.CELL:
            precedents = self.workbook.cell_dependencies.resolve_precedents(new_cell, set())
            for precedent in precedents:
                cell = self.workbook.get_cell(precedent)
                if cell:
                    precedents_information.append(
                        RangeInformation(cell.address, cell.formula, cell.value))
                else:
                    precedents_information.append(RangeInformation(precedent, "", ""))

        context_information = FormulaContextInformation(new_cell, precedents_information)
        self._formula_context_information.set_value(context_information)

    def initialize(self, initial_value: CellAddress) -> None:
        self(initial_value, None)

    def stop(self):
        self._formula_context_information.set_value(None)
