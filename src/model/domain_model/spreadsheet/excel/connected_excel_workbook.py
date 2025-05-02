from typing import Optional

import openpyxl.utils
import xlwings as xw

from model.domain_model.spreadsheet.i_connected_workbook import IConnectedWorkbook
from model.domain_model.spreadsheet.range_reference import RangeReference, RangeReferenceType
from model.utils.color_utils import get_hex_color_from_tuple, rgb_to_grayscale
from model.utils.excel_utils import convert_to_absolute_range, convert_xlwings_address


class ConnectedExcelWorkbook(IConnectedWorkbook):

    def __init__(self, xlwings_workbook: xw.Book):
        self.connected_workbook: xw.Book = xlwings_workbook

        super().__init__(self.connected_workbook.name, self.connected_workbook.fullname)

    def get_connected_workbook(self) -> xw.Book:
        return self.connected_workbook

    def calculate_workbook(self):
        self.connected_workbook.app.calculate()

    def get_range_color(self, range_ref: RangeReference) -> Optional[str]:
        return get_hex_color_from_tuple(self._get_range(range_ref.sheet, range_ref.reference).color)

    def set_range_color(self, range_ref: RangeReference, color: str):
        self._get_range(range_ref.sheet, range_ref.reference).color = color

    def set_ranges_color(self, range_refs: list[RangeReference], color: str):
        self.disable_screen_updating()
        try:
            for range_ref in range_refs:
                self.set_range_color(range_ref, color)
        finally:
            self.enable_screen_updating()

    def get_selected_range_ref(self) -> RangeReference:
        selection = self.connected_workbook.selection
        return convert_xlwings_address(selection)

    def add_name(self, range_ref: RangeReference, new_name: str) -> None:
        self.connected_workbook.names.add(new_name,
                                          f"='{range_ref.sheet}'!{convert_to_absolute_range(range_ref.reference)}")

    def get_names(self) -> dict[str, str]:
        names: dict[str, str] = {}
        for name in self.connected_workbook.names:
            names[name.name] = name.refers_to
        return names

    def set_formula(self, range_ref: RangeReference, formula: str):
        if not formula or range_ref.reference_type != RangeReferenceType.CELL:
            raise ValueError("Formula cannot be empty.")
        self._get_range(range_ref.sheet, range_ref.reference).formula = formula

    def disable_screen_updating(self):
        self.connected_workbook.app.screen_updating = False

    def enable_screen_updating(self):
        self.connected_workbook.app.screen_updating = True

    def set_colors_from_dict(self, colors: dict[RangeReference, str]):
        self.disable_screen_updating()
        for range_reference, color in colors.items():
            self.set_range_color(range_reference, color)
        self.enable_screen_updating()

    def grayscale_colors_and_return_initial_colors(self) -> dict[RangeReference, str]:
        new_colors: dict[RangeReference, str] = {}
        return self.initial_to_grayscale_and_set_from_dict_and_return_initial_colors(new_colors)

    def initial_to_grayscale_and_set_from_dict_and_return_initial_colors(self, new_colors: dict[RangeReference, str]) -> \
            dict[RangeReference, str]:
        initial_colors: dict[RangeReference, str] = {}
        self.disable_screen_updating()
        try:
            for sheet in self.connected_workbook.sheets:
                sheet: xw.Sheet
                used_range: xw.Range = sheet.used_range

                for row in openpyxl.utils.rows_from_range(used_range.address):
                    for cell_address_string in row:
                        range_reference: RangeReference = RangeReference.from_raw(self.name, sheet.name,
                                                                                  cell_address_string)
                        xw_cell: xw.Range = sheet.range(cell_address_string)
                        # get and save initial color
                        initial_color: tuple = xw_cell.color
                        initial_colors[range_reference] = get_hex_color_from_tuple(initial_color)
                        # set new color
                        if new_colors and range_reference in new_colors:
                            new_color = new_colors[range_reference]
                        else:
                            new_color = rgb_to_grayscale(initial_color)
                        if new_color:
                            xw_cell.color = new_color
        finally:
            self.enable_screen_updating()

        return initial_colors

    def _get_range(self, sheet: str, cell_range: str) -> xw.Range:
        return self._get_sheet(sheet).range(cell_range)

    def _get_sheet(self, sheet: str) -> xw.Sheet:
        return self.connected_workbook.sheets[sheet]
