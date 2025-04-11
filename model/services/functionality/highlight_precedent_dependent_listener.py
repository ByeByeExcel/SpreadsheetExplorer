from typing import Optional

import webcolors

from model.models.i_connected_workbook import IConnectedWorkbook
from model.models.spreadsheet.cell_address import CellAddress
from model.services.functionality.i_selection_listener import ISelectionListener


class HighlightCellSelectionListener(ISelectionListener):
    def __init__(self, workbook: IConnectedWorkbook):
        self.workbook = workbook
        self.original_colors: dict[CellAddress, Optional[str]] = {}

    def __call__(self, old_cell: CellAddress, new_cell: CellAddress):
        for addr, color in self.original_colors.items():
            self.workbook.set_range_color(addr, color)
        self.original_colors.clear()

        precedents = self.workbook.cell_dependencies.precedents.get(new_cell, set())
        dependents = self.workbook.cell_dependencies.dependents.get(new_cell, set())

        for precedent in precedents:
            self.original_colors[precedent] = self.workbook.get_range_color(precedent)

        for dependent in dependents:
            self.original_colors[dependent] = self.workbook.get_range_color(dependent)

        self.workbook.set_ranges_color(precedents, webcolors.name_to_hex("yellow"))
        self.workbook.set_ranges_color(dependents, webcolors.name_to_hex("red"))

    def stop(self):
        for addr, color in self.original_colors.items():
            self.workbook.set_range_color(addr, color)
