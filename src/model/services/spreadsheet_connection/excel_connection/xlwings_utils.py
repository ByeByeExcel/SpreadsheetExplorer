import xlwings as xw

from src.model.models.spreadsheet.cell_address import CellAddress, CellAddressType
from src.model.models.spreadsheet.spreadsheet_classes import Worksheet, Cell


def convert_xlwings_sheet(xlwings_sheet: xw.Sheet) -> Worksheet:
    used_range: xw.Range = xlwings_sheet.used_range

    cells: dict[CellAddress, Cell] = {}
    for cell in used_range:
        cell_address: CellAddress = CellAddress(
            xlwings_sheet.book.name.lower(),
            xlwings_sheet.name,
            cell.address,
        )
        custom_cell = Cell(cell_address, cell.value, cell.formula)
        cells[custom_cell.address] = custom_cell

    custom_worksheet = Worksheet(xlwings_sheet.name, cells)
    return custom_worksheet


def convert_xlwings_address(cell_range: xw.Range) -> CellAddress:
    range_type: CellAddressType = CellAddressType.CELL if cell_range.shape == (1, 1) else CellAddressType.RANGE

    return CellAddress(cell_range.sheet.book.name, cell_range.sheet.name, cell_range.address, range_type)
