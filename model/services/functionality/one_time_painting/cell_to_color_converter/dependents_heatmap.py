from typing import Optional

from model.models.spreadsheet.spreadsheet_classes import Cell
from model.services.functionality.one_time_painting.cell_to_color_converter.i_cell_to_color_converter import \
    CellToColorConverter
from model.settings.colour_scheme import ColourScheme, ColorRole
from model.utils.colour_utils import interpolate_color
from model.utils.utils import clamp


class DependentsHeatmap(CellToColorConverter):
    _MAX_DEPENDENTS_FOR_COLOR = 10

    def convert(self, cell: Cell) -> Optional[str]:
        if not cell:
            return None
        dependents = self.workbook.cell_dependencies.dependents.get(cell.address)
        if dependents is None:
            return None
        k = clamp(len(dependents) / self._MAX_DEPENDENTS_FOR_COLOR, 0, 1)
        return interpolate_color(ColourScheme[ColorRole.HEATMAP_0], ColourScheme[ColorRole.HEATMAP_1], k)
