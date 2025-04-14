from model.models.i_connected_workbook import IConnectedWorkbook
from model.models.spreadsheet.cell_address import CellAddress
from model.models.spreadsheet.spreadsheet_classes import Cell
from model.services.functionality.one_time_painting.cell_to_color_converter.i_cell_to_color_converter import CellToColorConverter


class OneTimePaintingExecutor:
    def __init__(
            self,
            workbook: IConnectedWorkbook,
            cells: set[Cell],
            cell_to_color_converter: CellToColorConverter,
    ):
        self.workbook = workbook
        self.cells = cells
        self.cell_to_color_converter = cell_to_color_converter
        self._original_colors: dict[CellAddress, str] = {}

    def paint(self):
        for cell in self.cells:
            self._original_colors[cell.address] = self.workbook.get_range_color(cell.address)
            self.workbook.set_range_color(cell.address, self.cell_to_color_converter.convert(cell))

    def reset(self):
        for cell in self.cells:
            if cell.address in self._original_colors:
                self.workbook.set_range_color(cell.address, self._original_colors[cell.address])

        self._original_colors.clear()
