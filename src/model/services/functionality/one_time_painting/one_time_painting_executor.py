from model.models.spreadsheet.cell_address import CellAddress
from model.models.spreadsheet.spreadsheet_classes import Cell
from model.services.functionality.one_time_painting.cell_to_color_converter.i_cell_to_color_converter import \
    CellToColorConverter


class OneTimePaintingExecutor:
    def __init__(
            self,
            cells: set[Cell],
            cell_to_color_converter: CellToColorConverter,
    ):
        self.cells = cells
        self.cell_to_color_converter = cell_to_color_converter

    def get_color_dict(self) -> dict[CellAddress, str]:
        color_dict: dict[CellAddress, str] = {}
        for cell in self.cells:
            new_color: str = self.cell_to_color_converter.convert(cell)
            if new_color is None:
                continue
            color_dict[cell.address] = self.cell_to_color_converter.convert(cell)

        return color_dict
