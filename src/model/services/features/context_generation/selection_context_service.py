from typing import Optional

from model.domain_model.spreadsheet.range_with_context import RangeWithContext
from model.services.app_state_service import AppStateService
from model.services.current_range_selection.i_selection_observer import ISelectionObserver
from model.services.features.context_generation.selection_context_observer import \
    SelectionContextObserver


class SelectionContextService:

    def __init__(self, app_state: AppStateService) -> None:
        self._app_state = app_state
        self._selection_observer: Optional[ISelectionObserver] = None

        app_state.is_connected_to_workbook.add_observer(self._on_wb_connection_change)

    def _start_selection_context_generation(self) -> None:
        observer = SelectionContextObserver(self._app_state.get_connected_workbook(),
                                            self._on_context_updated)
        self._app_state.selected_range.add_observer(observer)
        self._selection_observer = observer

    def _stop(self) -> None:
        if self._selection_observer is None:
            return
        self._selection_observer.stop()
        self._app_state.selected_range.remove_observer(self._selection_observer)
        self._selection_observer = None

    def _on_wb_connection_change(self, is_connected: bool, _):
        if is_connected:
            self._start_selection_context_generation()
        else:
            self._stop()

    def _on_context_updated(self, selected_range_with_context: RangeWithContext) -> None:
        self._app_state.selected_range_with_context.set_value(selected_range_with_context)
