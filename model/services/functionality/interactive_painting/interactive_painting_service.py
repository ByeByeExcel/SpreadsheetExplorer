from model.app_state import AppState
from model.models.i_connected_workbook import IConnectedWorkbook
from model.services.functionality.interactive_painting.selection_listener.highlight_precedent_dependent_observer import \
    HighlightCellSelectionObserver


class InteractivePaintingService:
    _selection_observers: [HighlightCellSelectionObserver] = []

    def __init__(self, app_state: AppState) -> None:
        self._app_state = app_state

    def highlight_dependents_precedents(self, connected_workbook: IConnectedWorkbook) -> None:
        observer = HighlightCellSelectionObserver(connected_workbook)
        self._app_state.selected_cell.add_observer(observer)
        self._selection_observers.append(observer)

    def stop_all(self) -> None:
        for observer in self._selection_observers:
            self._app_state.selected_cell.remove_observer(observer)
        self._selection_observers = []
