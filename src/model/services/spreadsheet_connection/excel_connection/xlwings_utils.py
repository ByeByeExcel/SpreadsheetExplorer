import xlwings as xw

from model.domain_model.spreadsheet.range_reference import RangeReference, RangeReferenceType


def convert_xlwings_address(cell_range: xw.Range) -> RangeReference:
    range_type: RangeReferenceType = RangeReferenceType.CELL if cell_range.shape == (1, 1) else RangeReferenceType.RANGE

    return RangeReference.from_raw(cell_range.sheet.book.name, cell_range.sheet.name, cell_range.address, range_type)
