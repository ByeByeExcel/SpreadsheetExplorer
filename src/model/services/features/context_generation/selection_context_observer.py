from typing import Optional, Callable

from model.adapters.i_connected_workbook import IConnectedWorkbook
from model.domain_model.spreadsheet.range_reference import RangeReference, RangeReferenceType
from model.domain_model.spreadsheet.range_with_context import RangeWithContext
from model.services.current_range_selection.i_selection_observer import \
    ISelectionObserver


class SelectionContextObserver(ISelectionObserver):
    def __init__(self, workbook: IConnectedWorkbook,
                 on_context_updated: Callable[[Optional[RangeWithContext]], None]):
        self.workbook = workbook
        self._on_context_updated = on_context_updated

    def __call__(self, new_range_ref: Optional[RangeReference], _: Optional[RangeReference]) -> None:
        if not new_range_ref:
            self._on_context_updated(None)
            return
        if new_range_ref.workbook != self.workbook.name.lower():
            return

        range_information = self._get_range_information(new_range_ref)
        self._on_context_updated(range_information)

    def initialize(self, initial_range_ref: RangeReference) -> None:
        self(initial_range_ref, None)

    def stop(self) -> None:
        self._on_context_updated(None)

    def _get_range_information(self, range_ref: RangeReference) -> Optional[RangeWithContext]:
        if range_ref.reference_type == RangeReferenceType.EXTERNAL:
            return RangeWithContext(range_ref, "", "", [])

        precedents_addr = self.workbook.get_precedents(range_ref)
        precedents: list[RangeWithContext] = []

        for precedent_addr in precedents_addr:
            precedents.append(self._get_range_information(precedent_addr))

        precedents.sort(key=lambda r: r.reference)

        cell_range = self.workbook.get_range(range_ref)
        if cell_range:
            return RangeWithContext(range_ref, cell_range.value, cell_range.formula, precedents)

        return RangeWithContext(range_ref, "", "", precedents)
