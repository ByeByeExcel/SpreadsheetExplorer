from typing import Optional

from model.domain_model.spreadsheet.cell_range import CellRange
from model.services.features.coloring.static.color_strategies.i_range_color_strategy import \
    IRangeColorStrategy
from model.settings.color_scheme import ColorScheme, ColorRole


class RootNodeColoring(IRangeColorStrategy):
    def convert(self, cell_range: CellRange) -> Optional[str]:
        if not cell_range:
            return None
        has_dependents = self.workbook.has_dependent(cell_range.reference)
        has_precedents = self.workbook.has_precedent(cell_range.reference)
        if not has_dependents and has_precedents:
            return ColorScheme[ColorRole.ROOT_NODE]

        return None
