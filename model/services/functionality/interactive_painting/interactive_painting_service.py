from model.app_state import AppState
from model.feature import Feature
from model.models.i_connected_workbook import IConnectedWorkbook
from model.services.functionality.interactive_painting.selection_listener.highlight_precedent_dependent_observer import \
    HighlightCellSelectionObserver


class InteractivePaintingService:
    _selection_observers: dict[Feature, HighlightCellSelectionObserver] = {}

    def __init__(self, app_state: AppState) -> None:
        self._app_state = app_state

    def highlight_dependents_precedents(self, connected_workbook: IConnectedWorkbook) -> None:
        observer = HighlightCellSelectionObserver(connected_workbook)
        self._app_state.selected_cell.add_observer(observer)
        self._selection_observers[Feature.DEPENDENCY_HIGHLIGHTING] = observer

    def stop_dependency_highlighting(self) -> None:
        self.stop_feature(Feature.DEPENDENCY_HIGHLIGHTING)

    def stop_feature(self, feature: Feature) -> None:
        observer = self._selection_observers.pop(feature, None)
        if observer:
            observer.stop()
            self._app_state.selected_cell.remove_observer(observer)

    def stop_all(self) -> None:
        for feature in self._selection_observers.keys():
            self.stop_feature(feature)
