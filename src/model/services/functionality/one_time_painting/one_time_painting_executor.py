from model.domain_model.spreadsheet.cell_range import CellRange
from model.domain_model.spreadsheet.range_reference import RangeReference
from model.services.functionality.one_time_painting.cell_to_color_converter.i_cell_to_color_converter import \
    RangeToColorConverter


class OneTimePaintingExecutor:
    def __init__(
            self,
            cell_ranges: set[CellRange],
            cell_to_color_converter: RangeToColorConverter,
    ):
        self.cell_ranges = cell_ranges
        self.cell_to_color_converter = cell_to_color_converter

    def get_color_dict(self) -> dict[RangeReference, str]:
        color_dict: dict[RangeReference, str] = {}
        for cell_range in self.cell_ranges:
            new_color: str = self.cell_to_color_converter.convert(cell_range)
            if new_color is None:
                continue
            color_dict[cell_range.reference] = self.cell_to_color_converter.convert(cell_range)

        return color_dict
