from typing import Optional

from model.models.spreadsheet.cell import Cell
from model.services.functionality.one_time_painting.cell_to_color_converter.i_cell_to_color_converter import \
    CellToColorConverter
from model.settings.colour_scheme import ColourScheme, ColorRole


class RootNodeHighlighter(CellToColorConverter):
    def convert(self, cell: Cell) -> Optional[str]:
        if not cell:
            return None
        has_dependents = self.workbook.has_dependent(cell.address)
        has_precedents = self.workbook.has_precedent(cell.address)
        if not has_dependents and has_precedents:
            return ColourScheme[ColorRole.ROOT_NODE]

        return None
