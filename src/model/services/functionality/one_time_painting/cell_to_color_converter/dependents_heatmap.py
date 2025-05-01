from typing import Optional

from model.domain_model.spreadsheet.cell_range import CellRange
from model.services.functionality.one_time_painting.cell_to_color_converter.i_cell_to_color_converter import \
    RangeToColorConverter
from model.settings.colour_scheme import ColourScheme, ColorRole
from model.utils.colour_utils import interpolate_color
from model.utils.utils import clamp


class DependentsHeatmap(RangeToColorConverter):
    _MAX_DEPENDENTS_FOR_COLOR = 10

    def convert(self, cell_range: CellRange) -> Optional[str]:
        if not cell_range:
            return None
        dependents = self.workbook.resolve_dependents_to_cell_level(cell_range.reference)
        if not dependents:
            return None
        k = clamp(len(dependents) / self._MAX_DEPENDENTS_FOR_COLOR, 0, 1)
        return interpolate_color(ColourScheme[ColorRole.HEATMAP_0], ColourScheme[ColorRole.HEATMAP_1], k)
