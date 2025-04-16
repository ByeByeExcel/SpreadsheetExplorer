from model.models.i_connected_workbook import IConnectedWorkbook
from model.models.spreadsheet.cell_address import CellAddress
from model.models.spreadsheet.spreadsheet_classes import Cell
from model.services.functionality.one_time_painting.cell_to_color_converter.i_cell_to_color_converter import \
    CellToColorConverter


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
        self.workbook.disable_screen_updating()
        for cell in self.cells:
            new_color: str = self.cell_to_color_converter.convert(cell)
            if new_color is None:
                continue
            self._original_colors[cell.address] = self.workbook.get_range_color(cell.address)
            self.workbook.set_range_color(cell.address, new_color)
        self.workbook.enable_screen_updating()

    def reset(self):
        self.workbook.disable_screen_updating()
        for cell in self.cells:
            if cell.address in self._original_colors:
                self.workbook.set_range_color(cell.address, self._original_colors[cell.address])
        self.workbook.enable_screen_updating()
        self._original_colors.clear()
