from typing import Optional

from src.model.models.i_connected_workbook import IConnectedWorkbook
from src.model.models.spreadsheet.cell_address import CellAddress, CellAddressType
from src.model.services.functionality.interactive_painting.selection_listener.i_selection_observer import \
    ISelectionObserver
from src.model.settings.colour_scheme import ColourScheme, ColorRole


class HighlightCellSelectionObserver(ISelectionObserver):
    def __init__(self, workbook: IConnectedWorkbook):
        self.workbook = workbook
        self.original_colors: dict[CellAddress, Optional[str]] = {}

    def __call__(self, new_cell: CellAddress, old_cell: CellAddress):
        if new_cell.workbook != self.workbook.name.lower():
            return
        for addr, color in self.original_colors.items():
            self.workbook.set_range_color(addr, color)
        self.original_colors.clear()

        if new_cell.address_type == CellAddressType.RANGE:
            precedents = set()
        else:
            precedents = self.workbook.cell_dependencies.resolve_precedents(new_cell, set())

        dependents = self.workbook.cell_dependencies.resolve_dependents(new_cell, set())

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
