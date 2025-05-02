from typing import Optional

from model.domain_model.feature import Feature
from model.services.app_state_service import AppStateService
from model.services.current_range_selection.i_selection_observer import ISelectionObserver
from model.services.features.coloring.interactive.dependency_coloring.selection_dependency_highligher_observer \
    import SelectionDependencyHighlighterObserver


class SelectionColoringService:

    def __init__(self, app_state: AppStateService) -> None:
        self._app_state = app_state
        self._selection_dependency_highlighter_observer: Optional[ISelectionObserver] = None

    def start_dependency_highlighting(self) -> None:
        if not self._app_state.can_start_feature():
            raise ValueError("Dependency highlighting cannot be started.")

        self._app_state.set_feature_active(Feature.DEPENDENCY_HIGHLIGHTING)

        initial_colors = self._app_state.get_connected_workbook().grayscale_colors_and_return_initial_colors()
        self._app_state.store_initial_colors(initial_colors)

        observer = SelectionDependencyHighlighterObserver(self._app_state.get_connected_workbook())
        if self._app_state.selected_range.value:
            observer.initialize(self._app_state.selected_range.value)
        self._app_state.selected_range.add_observer(observer)
        self._selection_dependency_highlighter_observer = observer

    def stop_dependency_highlighting(self) -> None:
        if not self._selection_dependency_highlighter_observer:
            return
        self._app_state.selected_range.remove_observer(self._selection_dependency_highlighter_observer)
        self._selection_dependency_highlighter_observer.stop()
        self._selection_dependency_highlighter_observer = None

        self._app_state.get_connected_workbook().set_colors_from_dict(self._app_state.get_initial_colors())
        self._app_state.clear_initial_colors()
        self._app_state.set_feature_inactive(Feature.DEPENDENCY_HIGHLIGHTING)
