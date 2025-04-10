import xlwings as xw

from model.models.spreadsheet.excel.excel_workbook import ConnectedExcelWorkbook
from model.models.spreadsheet.spreadsheet_classes import Worksheet, Cell


def convert_xlwings_book(xlwings_book: xw.Book) -> ConnectedExcelWorkbook:
    custom_workbook = ConnectedExcelWorkbook(xlwings_book)

    for sheet in xlwings_book.sheets:
        custom_worksheet = convert_xlwings_sheet(sheet)
        custom_workbook.worksheets[custom_worksheet.name] = custom_worksheet

    return custom_workbook


def convert_xlwings_sheet(xlwings_sheet: xw.Sheet) -> Worksheet:
    used_range = xlwings_sheet.used_range

    cells: dict[str, Cell] = {}
    for cell in used_range:
        custom_cell = Cell(cell.address, cell.value, cell.formula)
        cells[cell.address] = custom_cell

    custom_worksheet = Worksheet(xlwings_sheet.name, cells)
    return custom_worksheet
