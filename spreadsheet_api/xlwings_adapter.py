import xlwings as xw

from .base import SpreadsheetInterface


class ExcelSpreadsheet(SpreadsheetInterface):
    def __init__(self, filepath):
        self.wb = xw.Book(filepath)
        self.sheet = self.wb.sheets[0]

    def get_value(self, cell):
        return self.sheet.range(cell).value

    def set_value(self, cell, value):
        self.sheet.range(cell).value = value

    def save(self):
        self.wb.save()

    def close(self):
        self.wb.close()
