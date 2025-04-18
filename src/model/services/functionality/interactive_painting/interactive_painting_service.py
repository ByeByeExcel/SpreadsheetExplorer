from src.model.app_state import AppState
from src.model.feature import Feature
from src.model.services.functionality.interactive_painting.selection_listener.highlight_precedent_dependent_observer import \
    HighlightCellSelectionObserver


class InteractivePaintingService:

    def __init__(self, app_state: AppState) -> None:
        self._app_state = app_state
        self._selection_observers: dict[Feature, HighlightCellSelectionObserver] = {}

    def highlight_dependents_precedents(self) -> None:
        if not self._app_state.can_start_feature():
            raise ValueError("Dependency highlighting cannot be started.")

        self._app_state.set_feature_active(Feature.DEPENDENCY_HIGHLIGHTING)

        initial_colors = self._app_state.get_connected_workbook().grayscale_colors_and_return_initial_colors()
        self._app_state.store_initial_colors(initial_colors)

        observer = HighlightCellSelectionObserver(self._app_state.get_connected_workbook())
        self._app_state.selected_cell.add_observer(observer)
        self._selection_observers[Feature.DEPENDENCY_HIGHLIGHTING] = observer

    def stop_dependency_highlighting(self) -> None:
        self.stop_feature(Feature.DEPENDENCY_HIGHLIGHTING)
        self._app_state.get_connected_workbook().set_colors_from_dict(self._app_state.get_initial_colors())
        self._app_state.clear_initial_colors()
        self._app_state.set_feature_inactive(Feature.DEPENDENCY_HIGHLIGHTING)

    def stop_feature(self, feature: Feature) -> None:
        observer = self._selection_observers.pop(feature, None)
        if observer:
            observer.stop()
            self._app_state.selected_cell.remove_observer(observer)
