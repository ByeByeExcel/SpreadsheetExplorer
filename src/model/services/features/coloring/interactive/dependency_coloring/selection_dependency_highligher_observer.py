from typing import Optional

from model.domain_model.spreadsheet.i_connected_workbook import IConnectedWorkbook
from model.domain_model.spreadsheet.range_reference import RangeReference, RangeReferenceType
from model.services.current_range_selection.i_selection_observer import \
    ISelectionObserver
from model.settings.color_scheme import ColorScheme, ColorRole


class SelectionDependencyHighlighterObserver(ISelectionObserver):
    def __init__(self, workbook: IConnectedWorkbook):
        self.workbook = workbook
        self.original_colors: dict[RangeReference, Optional[str]] = {}

    def __call__(self, new_range_ref: RangeReference, _: Optional[RangeReference]):
        self.workbook.set_colors_from_dict(self.original_colors)
        self.original_colors.clear()

        if not new_range_ref or new_range_ref.workbook != self.workbook.name.lower():
            return

        if new_range_ref.reference_type == RangeReferenceType.RANGE:
            precedents = set()
        else:
            precedents = self.workbook.resolve_precedents_to_cell_level(new_range_ref)

        dependents = self.workbook.resolve_dependents_to_cell_level(new_range_ref)

        for precedent in precedents:
            self.original_colors[precedent] = self.workbook.get_range_color(precedent)

        for dependent in dependents:
            self.original_colors[dependent] = self.workbook.get_range_color(dependent)

        self.workbook.set_ranges_color(precedents, ColorScheme[ColorRole.PRECEDENT])
        self.workbook.set_ranges_color(dependents, ColorScheme[ColorRole.DEPENDENT])

    def stop(self):
        self.workbook.set_colors_from_dict(self.original_colors)
        self.original_colors.clear()

    def initialize(self, initial_range_ref: RangeReference):
        self(initial_range_ref, None)
