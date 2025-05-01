from typing import Optional

from model.domain_model.spreadsheet.cell_range import CellRange
from model.services.functionality.one_time_painting.cell_to_color_converter.i_cell_to_color_converter import \
    RangeToColorConverter
from model.settings.colour_scheme import ColourScheme, ColorRole


class RootNodeHighlighter(RangeToColorConverter):
    def convert(self, cell_range: CellRange) -> Optional[str]:
        if not cell_range:
            return None
        has_dependents = self.workbook.has_dependent(cell_range.reference)
        has_precedents = self.workbook.has_precedent(cell_range.reference)
        if not has_dependents and has_precedents:
            return ColourScheme[ColorRole.ROOT_NODE]

        return None
