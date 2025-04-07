import xlwings

from model.models.i_connected_workbook import IConnectedWorkbook
from model.models.spreadsheet.spreadsheet_classes import Worksheet, Cell


class ConnectedExcelWorkbook(IConnectedWorkbook):
    def __init__(self, xlwings_workbook: xlwings.Book):
        super().__init__()
        self.connected_workbook: xlwings.Book = xlwings_workbook

    def set_cell_color(self, sheet: Worksheet, cell: Cell, color: str):
        self._get_cell(sheet, cell).color = color

    def _get_sheet(self, sheet: Worksheet) -> xlwings.Sheet:
        return self.connected_workbook.sheets[sheet.name]

    def _get_cell(self, sheet: Worksheet, cell: Cell):
        return self._get_sheet(sheet).range(cell.address)
