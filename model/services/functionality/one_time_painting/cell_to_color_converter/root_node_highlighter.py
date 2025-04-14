from typing import Optional

from model.models.spreadsheet.spreadsheet_classes import Cell
from model.services.functionality.one_time_painting.cell_to_color_converter.i_cell_to_color_converter import \
    CellToColorConverter
from model.settings.colour_scheme import ColourScheme, ColorRole


class RootNodeHighlighter(CellToColorConverter):
    def convert(self, cell: Cell) -> Optional[str]:
        dependents = self.workbook.cell_dependencies.dependents.get(cell.address)
        precedents = self.workbook.cell_dependencies.precedents.get(cell.address)
        if not dependents and precedents:
            return ColourScheme[ColorRole.ROOT_NODE]
        else:
            return None
