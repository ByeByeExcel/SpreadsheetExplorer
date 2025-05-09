from typing import Optional, Iterable

import openpyxl.utils
import xlwings as xw

from model.domain_model.spreadsheet.cell_range import CellRange
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

    def get_selected_range_ref(self) -> RangeReference:
        selection = self.connected_workbook.selection
        return convert_xlwings_address(selection)

    def get_range_color(self, range_ref: RangeReference) -> str:
        return get_hex_color_from_tuple(self._get_range(range_ref.sheet, range_ref.reference).color)

    def set_range_color(self, range_ref: RangeReference, color: str):
        self._get_range(range_ref.sheet, range_ref.reference).color = color

    def set_ranges_color(self, range_refs: Iterable[RangeReference], color: str):
        self.disable_screen_updating()
        try:
            for ref in range_refs:
                self.set_range_color(ref, color)
        finally:
            self.enable_screen_updating()

    def set_colors_from_dict(self, colors: dict[RangeReference, str]):
        self.disable_screen_updating()
        try:
            for ref, color in colors.items():
                self.set_range_color(ref, color)
        finally:
            self.enable_screen_updating()

    def set_formula(self, range_ref: RangeReference, formula: str):
        if not formula or range_ref.reference_type != RangeReferenceType.CELL:
            raise ValueError("Formula must be a non-empty string for a cell reference.")
        self._get_range(range_ref.sheet, range_ref.reference).formula = formula

    def disable_screen_updating(self):
        self.connected_workbook.app.screen_updating = False

    def enable_screen_updating(self):
        self.connected_workbook.app.screen_updating = True

    def add_name(self, range_ref: RangeReference, new_name: str) -> None:
        self.connected_workbook.names.add(
            new_name,
            f"='{range_ref.sheet}'!{convert_to_absolute_range(range_ref.reference)}"
        )

    def get_names(self) -> dict[str, str]:
        return {n.name: n.refers_to for n in self.connected_workbook.names}

    def resolve_defined_name(self, name: str) -> Optional[RangeReference]:
        try:
            xl_range = self.connected_workbook.names[name].refers_to_range
            is_range = xl_range.shape[0] > 1 or xl_range.shape[1] > 1
            return RangeReference.from_raw(
                xl_range.sheet.book.name,
                xl_range.sheet.name,
                xl_range.address,
                RangeReferenceType.RANGE if is_range else RangeReferenceType.CELL
            )
        except Exception:
            return None

    def get_used_range(self) -> Iterable[tuple[RangeReference, str, str]]:
        for sheet in self.connected_workbook.sheets:
            sheet: xw.Sheet
            used_range: xw.Range = sheet.used_range
            rows, cols = used_range.shape
            for row in range(0, rows):
                for col in range(0, cols):
                    ref = RangeReference.from_raw(sheet.book.name, sheet.name, used_range.rows[row][col].address)
                    yield ref, used_range.rows[row][col].value, used_range.rows[row][col].formula

    def resolve_range_reference(self, ref: RangeReference) -> tuple[str, str]:
        cell = self._get_range(ref.sheet, ref.reference)
        return cell.value, cell.formula

    def get_cells_in_range(self, range_ref: RangeReference) -> Iterable[CellRange]:
        sheet = self._get_sheet(range_ref.sheet)
        xl_range = sheet.range(range_ref.reference)
        rows, cols = xl_range.shape
        for row in range(0, rows):
            for col in range(0, cols):
                ref = RangeReference.from_raw(sheet.book.name, sheet.name, xl_range.rows[row][col].address)
                yield CellRange(ref, xl_range.rows[row][col].value, xl_range.rows[row][col].formula)

    def get_workbook_name(self) -> str:
        return self.connected_workbook.name

    def is_range(self, sheet: str, address: str) -> bool:
        try:
            rng = self.connected_workbook.sheets[sheet][address]
            return rng.shape[0] > 1 or rng.shape[1] > 1
        except Exception:
            return False

    def grayscale_colors_and_return_initial_colors(self) -> dict[RangeReference, str]:
        return self.initial_to_grayscale_and_set_from_dict_and_return_initial_colors({})

    def initial_to_grayscale_and_set_from_dict_and_return_initial_colors(
            self, new_colors: dict[RangeReference, str]
    ) -> dict[RangeReference, str]:
        initial_colors: dict[RangeReference, str] = {}
        self.disable_screen_updating()
        try:
            for sheet in self.connected_workbook.sheets:
                used_range = sheet.used_range
                for row in openpyxl.utils.rows_from_range(used_range.address):
                    for cell_address in row:
                        ref = RangeReference.from_raw(self.name, sheet.name, cell_address)
                        xw_cell = sheet.range(cell_address)
                        initial_color = xw_cell.color
                        initial_colors[ref] = get_hex_color_from_tuple(initial_color)
                        new_color = (
                            new_colors[ref] if new_colors and ref in new_colors
                            else rgb_to_grayscale(initial_color)
                        )
                        if new_color:
                            xw_cell.color = new_color
        finally:
            self.enable_screen_updating()
        return initial_colors

    def _get_range(self, sheet: str, cell_range: str) -> xw.Range:
        return self._get_sheet(sheet).range(cell_range)

    def _get_sheet(self, sheet: str) -> xw.Sheet:
        return self.connected_workbook.sheets[sheet]
