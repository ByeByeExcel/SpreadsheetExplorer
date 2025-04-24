import xlwings as xw

from model.models.spreadsheet.cell_address import CellAddress, CellAddressType


def convert_xlwings_address(cell_range: xw.Range) -> CellAddress:
    range_type: CellAddressType = CellAddressType.CELL if cell_range.shape == (1, 1) else CellAddressType.RANGE

    return CellAddress(cell_range.sheet.book.name, cell_range.sheet.name, cell_range.address, range_type)
