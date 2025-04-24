from typing import Optional

from model.models.i_connected_workbook import IConnectedWorkbook
from model.models.spreadsheet.cell_address import CellAddress, CellAddressType
from model.services.functionality.interactive_painting.selection_listener.i_selection_observer import \
    ISelectionObserver
from model.settings.colour_scheme import ColourScheme, ColorRole


class HighlightCellSelectionObserver(ISelectionObserver):
    def __init__(self, workbook: IConnectedWorkbook):
        self.workbook = workbook
        self.original_colors: dict[CellAddress, Optional[str]] = {}

    def __call__(self, new_cell: CellAddress, old_cell: Optional[CellAddress]):
        for addr, color in self.original_colors.items():
            self.workbook.set_range_color(addr, color)
        self.original_colors.clear()

        if not new_cell or new_cell.workbook != self.workbook.name.lower():
            return

        if new_cell.address_type == CellAddressType.RANGE:
            precedents = set()
        else:
            precedents = self.workbook.resolve_precedents_to_cell_level(new_cell)

        dependents = self.workbook.resolve_dependents_to_cell_level(new_cell)

        for precedent in precedents:
            self.original_colors[precedent] = self.workbook.get_range_color(precedent)

        for dependent in dependents:
            self.original_colors[dependent] = self.workbook.get_range_color(dependent)

        self.workbook.set_ranges_color(precedents, ColourScheme[ColorRole.PRECEDENT])
        self.workbook.set_ranges_color(dependents, ColourScheme[ColorRole.DEPENDENT])

    def stop(self):
        self.workbook.disable_screen_updating()
        for addr, color in self.original_colors.items():
            self.workbook.set_range_color(addr, color)
        self.original_colors.clear()
        self.workbook.enable_screen_updating()

    def initialize(self, initial_value: CellAddress):
        self(initial_value, None)
