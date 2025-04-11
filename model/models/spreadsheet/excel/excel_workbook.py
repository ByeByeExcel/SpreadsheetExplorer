import time
from typing import Optional

import xlwings

from model.models.i_connected_workbook import IConnectedWorkbook
from model.models.spreadsheet.cell_address import CellAddress
from model.utils.utils import get_hex_color_from_tuple


class ConnectedExcelWorkbook(IConnectedWorkbook):
    def on_cell_click_execute(self, listener: callable, stop):
        sheet = self.connected_workbook.sheets.active
        previous_selection = self.connected_workbook.selection.address

        while not stop():
            time.sleep(0.5)
            current_selection = self.connected_workbook.selection.address

            if current_selection != previous_selection:
                sheet.range(previous_selection).color = None

                current_cell = sheet.range(current_selection)
                # current_cell.color = webcolors.name_to_hex("yellow")
                previous_selection = current_selection
                listener(current_cell)

    def __init__(self, xlwings_workbook: xlwings.Book):
        super().__init__()
        self.connected_workbook: xlwings.Book = xlwings_workbook
        self.name = self.connected_workbook.name
        self.fullpath = self.connected_workbook.fullname

    def get_range_color(self, cell_range: CellAddress) -> Optional[str]:
        return get_hex_color_from_tuple(self._get_range(cell_range.sheet, cell_range.address).color)

    def set_range_color(self, cell_range: CellAddress, color: str):
        self._get_range(cell_range.sheet, cell_range.address).color = color

    def set_ranges_color(self, cell_ranges: [CellAddress], color: str):
        for cell_range in cell_ranges:
            self.set_range_color(cell_range, color)

    def _get_sheet(self, sheet: str) -> xlwings.Sheet:
        return self.connected_workbook.sheets[sheet]

    def _get_range(self, sheet: str, cell_range: str) -> xlwings.Range:
        return self._get_sheet(sheet).range(cell_range)
