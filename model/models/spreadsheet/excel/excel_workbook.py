from typing import Optional

import xlwings

from model.models.i_connected_workbook import IConnectedWorkbook
from model.models.spreadsheet.cell_address import CellAddress
from model.models.spreadsheet.spreadsheet_classes import Cell
from model.services.spreadsheet_connection.excel_connection.xlwings_utils import convert_xlwings_address, \
    convert_xlwings_sheet
from model.utils.colour_utils import get_hex_color_from_tuple


class ConnectedExcelWorkbook(IConnectedWorkbook):
    def __init__(self, xlwings_workbook: xlwings.Book):
        super().__init__()
        self.connected_workbook: xlwings.Book = xlwings_workbook
        self.name = self.connected_workbook.name
        self.fullpath = self.connected_workbook.fullname

        for sheet in xlwings_workbook.sheets:
            custom_worksheet = convert_xlwings_sheet(sheet)
            self.worksheets[custom_worksheet.name] = custom_worksheet

    def get_range_color(self, cell_range: CellAddress) -> Optional[str]:
        return get_hex_color_from_tuple(self._get_range(cell_range.sheet, cell_range.address).color)

    def set_range_color(self, cell_range: CellAddress, color: str):
        self._get_range(cell_range.sheet, cell_range.address).color = color

    def set_ranges_color(self, cell_ranges: [CellAddress], color: str):
        for cell_range in cell_ranges:
            self.set_range_color(cell_range, color)

    def set_cells_color(self, cells: [Cell], color: str):
        for cell in cells:
            self.set_range_color(cell.address, color)

    def get_selected_cell(self) -> CellAddress:
        selection = self.connected_workbook.selection
        return convert_xlwings_address(selection)

    def _get_sheet(self, sheet: str) -> xlwings.Sheet:
        return self.connected_workbook.sheets[sheet]

    def _get_range(self, sheet: str, cell_range: str) -> xlwings.Range:
        return self._get_sheet(sheet).range(cell_range)


