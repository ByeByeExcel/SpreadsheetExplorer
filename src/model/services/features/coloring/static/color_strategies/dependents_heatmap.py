from typing import Optional

from model.domain_model.spreadsheet.cell_range import CellRange
from model.services.features.coloring.static.color_strategies.i_range_color_strategy import \
    IRangeColorStrategy
from model.settings.color_scheme import ColorScheme, ColorRole
from model.utils.color_utils import interpolate_color
from model.utils.utils import clamp


class DependentsHeatmap(IRangeColorStrategy):
    _MAX_DEPENDENTS_FOR_COLOR = 10

    def convert(self, cell_range: CellRange) -> Optional[str]:
        if not cell_range:
            return None
        dependents = self.workbook.resolve_dependents_to_cell_level(cell_range.reference)
        if not dependents:
            return None
        k = clamp(len(dependents) / self._MAX_DEPENDENTS_FOR_COLOR, 0, 1)
        return interpolate_color(ColorScheme[ColorRole.HEATMAP_0], ColorScheme[ColorRole.HEATMAP_1], k)
