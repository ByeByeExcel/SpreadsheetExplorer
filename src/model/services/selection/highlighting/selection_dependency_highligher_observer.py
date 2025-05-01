from typing import Optional

from model.domain_model.i_connected_workbook import IConnectedWorkbook
from model.domain_model.spreadsheet.range_reference import RangeReference, RangeReferenceType
from model.services.selection.i_selection_observer import \
    ISelectionObserver
from model.settings.colour_scheme import ColourScheme, ColorRole


class SelectionDependencyHighlighterObserver(ISelectionObserver):
    def __init__(self, workbook: IConnectedWorkbook):
        self.workbook = workbook
        self.original_colors: dict[RangeReference, Optional[str]] = {}

    def __call__(self, new_range_ref: RangeReference, _: Optional[RangeReference]):
        for addr, color in self.original_colors.items():
            self.workbook.set_range_color(addr, color)
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

        self.workbook.set_ranges_color(precedents, ColourScheme[ColorRole.PRECEDENT])
        self.workbook.set_ranges_color(dependents, ColourScheme[ColorRole.DEPENDENT])

    def stop(self):
        self.workbook.disable_screen_updating()
        for addr, color in self.original_colors.items():
            self.workbook.set_range_color(addr, color)
        self.original_colors.clear()
        self.workbook.enable_screen_updating()

    def initialize(self, initial_range_ref: RangeReference):
        self(initial_range_ref, None)
