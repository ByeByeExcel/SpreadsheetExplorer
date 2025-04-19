from typing import Optional

from model.app_state import AppState
from model.services.functionality.basic_context_generation_observer import \
    BasicContextGenerationObserver
from model.services.functionality.interactive_painting.selection_listener.i_selection_observer import ISelectionObserver


class InteractiveContextService:

    def __init__(self, app_state: AppState) -> None:
        self._app_state = app_state
        self._selection_observer: Optional[ISelectionObserver] = None

    def start_basic_cell_information(self) -> None:
        observer = BasicContextGenerationObserver(self._app_state.get_connected_workbook(),
                                                  self._app_state.context_information)
        self._app_state.selected_cell.add_observer(observer)
        self._selection_observer = observer

    def stop(self) -> None:
        if self._selection_observer is None:
            return
        self._selection_observer.stop()
        self._app_state.selected_cell.remove_observer(self._selection_observer)
        self._selection_observer = None
