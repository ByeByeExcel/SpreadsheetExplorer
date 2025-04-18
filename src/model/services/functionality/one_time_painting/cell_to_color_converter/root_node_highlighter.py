from typing import Optional

from src.model.models.spreadsheet.spreadsheet_classes import Cell
from src.model.services.functionality.one_time_painting.cell_to_color_converter.i_cell_to_color_converter import \
    CellToColorConverter
from src.model.settings.colour_scheme import ColourScheme, ColorRole


class RootNodeHighlighter(CellToColorConverter):
    def convert(self, cell: Cell) -> Optional[str]:
        if not cell:
            return None
        dependents = self.workbook.cell_dependencies.dependents.get(cell.address)
        precedents = self.workbook.cell_dependencies.precedents.get(cell.address)
        if not dependents and precedents:
            return ColourScheme[ColorRole.ROOT_NODE]

        return None
