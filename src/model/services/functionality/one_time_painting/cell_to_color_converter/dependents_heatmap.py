from typing import Optional

from src.model.models.spreadsheet.spreadsheet_classes import Cell
from src.model.services.functionality.one_time_painting.cell_to_color_converter.i_cell_to_color_converter import \
    CellToColorConverter
from src.model.settings.colour_scheme import ColourScheme, ColorRole
from src.model.utils.colour_utils import interpolate_color
from src.model.utils.utils import clamp


class DependentsHeatmap(CellToColorConverter):
    _MAX_DEPENDENTS_FOR_COLOR = 10

    def convert(self, cell: Cell) -> Optional[str]:
        if not cell:
            return None
        dependents = self.workbook.cell_dependencies.resolve_dependents(cell.address, set())
        if not dependents:
            return None
        k = clamp(len(dependents) / self._MAX_DEPENDENTS_FOR_COLOR, 0, 1)
        return interpolate_color(ColourScheme[ColorRole.HEATMAP_0], ColourScheme[ColorRole.HEATMAP_1], k)
