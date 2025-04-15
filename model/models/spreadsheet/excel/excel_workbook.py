from typing import Optional

import xlwings

from model.models.i_connected_workbook import IConnectedWorkbook
from model.models.spreadsheet.cell_address import CellAddress
from model.models.spreadsheet.spreadsheet_classes import Cell
from model.services.spreadsheet_connection.excel_connection.xlwings_utils import convert_xlwings_address, \
    convert_xlwings_sheet
from model.utils.colour_utils import get_hex_color_from_tuple, rgb_to_grayscale
from model.utils.utils import convert_to_absolute_range, generate_addresses


class ConnectedExcelWorkbook(IConnectedWorkbook):

    def __init__(self, xlwings_workbook: xlwings.Book):
        super().__init__()
        self.connected_workbook: xlwings.Book = xlwings_workbook
        self.name = self.connected_workbook.name
        self.fullpath = self.connected_workbook.fullname

        for sheet in xlwings_workbook.sheets:
            custom_worksheet = convert_xlwings_sheet(sheet)
            self.worksheets[custom_worksheet.name.lower()] = custom_worksheet

    def get_range_color(self, cell_range: CellAddress) -> Optional[str]:
        return get_hex_color_from_tuple(self._get_range(cell_range.sheet, cell_range.address).color)

    def set_range_color(self, cell_range: CellAddress, color: str):
        self._get_range(cell_range.sheet, cell_range.address).color = color

    def set_ranges_color(self, cell_ranges: [CellAddress], color: str):
        self.disable_screen_updating()
        for cell_range in cell_ranges:
            self.set_range_color(cell_range, color)
        self.enable_screen_updating()

    def set_cells_color(self, cells: [Cell], color: str):
        self.disable_screen_updating()
        for cell in cells:
            self.set_range_color(cell.address, color)
        self.enable_screen_updating()

    def get_selected_cell(self) -> CellAddress:
        selection = self.connected_workbook.selection
        return convert_xlwings_address(selection)

    def add_name(self, cell_range: CellAddress, new_name: str) -> None:
        self.connected_workbook.names.add(new_name,
                                          f"='{cell_range.sheet}'!{convert_to_absolute_range(cell_range.address)}")

    def get_names(self) -> dict[str, str]:
        names: dict[str, str] = {}
        for name in self.connected_workbook.names:
            names[name.name] = name.refers_to
        return names

    def set_formula(self, cell: CellAddress, formula: str):
        self._get_range(cell.sheet, cell.address).formula = formula

    def disable_screen_updating(self):
        self.connected_workbook.app.screen_updating = False

    def enable_screen_updating(self):
        self.connected_workbook.app.screen_updating = True

    def set_colors_from_dict(self, colors: dict[CellAddress, str]):
        self.disable_screen_updating()
        for cell_address, color in colors.items():
            self.set_range_color(cell_address, color)
        self.enable_screen_updating()

    def grayscale_colors_and_return_initial_colors(self) -> dict[CellAddress, str]:
        colors: dict[CellAddress, str] = {}
        self.disable_screen_updating()
        for sheet in self.connected_workbook.sheets:
            sheet: xlwings.Sheet
            cell_range: xlwings.Range = sheet.used_range
            cell_addresses_2d: [[str]] = generate_addresses(cell_range.row, cell_range.column, cell_range.shape)

            for row in cell_addresses_2d:
                row: [str]
                for cell_address in row:
                    cell: xlwings.Range = sheet.range(cell_address)
                    color: tuple = cell.color
                    colors[CellAddress(self.name, sheet.name, cell_address)] = get_hex_color_from_tuple(color)
                    cell.color = rgb_to_grayscale(color)
        self.enable_screen_updating()
        return colors

    def _get_range(self, sheet: str, cell_range: str) -> xlwings.Range:
        return self._get_sheet(sheet).range(cell_range)

    def _get_sheet(self, sheet: str) -> xlwings.Sheet:
        return self.connected_workbook.sheets[sheet]
