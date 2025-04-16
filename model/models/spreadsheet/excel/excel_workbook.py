from typing import Optional

import xlwings

from model.models.i_connected_workbook import IConnectedWorkbook
from model.models.spreadsheet.cell_address import CellAddress
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
        try:
            for cell_range in cell_ranges:
                self.set_range_color(cell_range, color)
        finally:
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
        new_colors: dict[CellAddress, str] = {}
        return self.initial_to_grayscale_and_set_from_dict_and_return_initial_colors(new_colors)

    def initial_to_grayscale_and_set_from_dict_and_return_initial_colors(self, new_colors: dict[CellAddress, str]) -> \
            dict[CellAddress, str]:
        initial_colors: dict[CellAddress, str] = {}
        self.disable_screen_updating()
        try:
            for sheet in self.connected_workbook.sheets:
                sheet: xlwings.Sheet
                used_range: xlwings.Range = sheet.used_range
                cell_addresses_2d: [[str]] = generate_addresses(used_range.row, used_range.column, used_range.shape)

                for row in cell_addresses_2d:
                    row: [str]
                    for cell_address_string in row:
                        cell_address: CellAddress = CellAddress(self.name, sheet.name, cell_address_string)
                        xw_cell: xlwings.Range = sheet.range(cell_address_string)
                        # get and save initial color
                        initial_color: tuple = xw_cell.color
                        initial_colors[cell_address] = get_hex_color_from_tuple(initial_color)
                        # set new color
                        if new_colors and cell_address in new_colors:
                            new_color = new_colors[cell_address]
                        else:
                            new_color = rgb_to_grayscale(initial_color)
                        if new_color:
                            xw_cell.color = new_color
        finally:
            self.enable_screen_updating()
            return initial_colors

    def _get_range(self, sheet: str, cell_range: str) -> xlwings.Range:
        return self._get_sheet(sheet).range(cell_range)

    def _get_sheet(self, sheet: str) -> xlwings.Sheet:
        return self.connected_workbook.sheets[sheet]
