from typing import Optional

from model.models.formula_context_information import RangeInformation
from model.models.i_connected_workbook import IConnectedWorkbook
from model.models.spreadsheet.cell_address import CellAddress, CellAddressType
from model.services.functionality.interactive_painting.selection_listener.i_selection_observer import \
    ISelectionObserver
from model.utils.observable_value import ObservableValue


class BasicContextGenerationObserver(ISelectionObserver):

    def __init__(self, workbook: IConnectedWorkbook,
                 formula_context_information_observable: ObservableValue[Optional[RangeInformation]]):
        self.workbook = workbook
        self._formula_context_information = formula_context_information_observable

    def __call__(self, new_cell: Optional[CellAddress], old_cell: Optional[CellAddress]):
        if not new_cell:
            self._formula_context_information.set_value(None)
            return
        if new_cell.workbook != self.workbook.name.lower():
            return

        range_information = self.get_range_information(new_cell)
        self._formula_context_information.set_value(range_information)

    def initialize(self, initial_value: CellAddress) -> None:
        self(initial_value, None)

    def stop(self):
        self._formula_context_information.set_value(None)

    def get_range_information(self, cell_address: CellAddress) -> Optional[RangeInformation]:
        if cell_address.address_type == CellAddressType.EXTERNAL:
            return None

        precedents_addr = self.workbook.get_precedents(cell_address)
        range_information: list[RangeInformation] = []

        for precedent_addr in precedents_addr:
            range_information.append(self.get_range_information(precedent_addr))

        range_information.sort(
            key=lambda r: (
                r.cell_address
            )
        )
        cell = self.workbook.get_cell(cell_address)
        if cell:
            return RangeInformation(cell_address, cell.formula, cell.value, range_information)

        return RangeInformation(cell_address, "", "", range_information)
