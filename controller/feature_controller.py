from model.app_state import AppState
from model.services.functionality.interactive_painting.interactive_painting_service import InteractivePaintingService
from model.services.functionality.one_time_painting.painting_service import PaintingService
from model.services.functionality.renaming_service import RenamingService


class FeatureController:
    def __init__(self,
                 interactive_painting_service: InteractivePaintingService,
                 painting_service: PaintingService,
                 renaming_service: RenamingService,
                 app_state: AppState):
        self._interactive_painting_service = interactive_painting_service
        self._painting_service = painting_service
        self._renaming_service = renaming_service
        self._app_state = app_state

    # interactive features
    def start_dependency_highlighting(self) -> None:
        self._interactive_painting_service.highlight_dependents_precedents()

    def stop_dependency_highlighting(self) -> None:
        self._interactive_painting_service.stop_dependency_highlighting()

    # one-time painting features
    def show_heatmap(self) -> None:
        self._painting_service.show_heatmap(self._app_state.get_connected_workbook())

    def hide_heatmap(self) -> None:
        self._painting_service.stop_heatmap()

    def show_root_nodes(self) -> None:
        self._painting_service.show_root_nodes(self._app_state.get_connected_workbook())

    def hide_root_nodes(self) -> None:
        self._painting_service.stop_root_nodes()

    # cascade renaming
    def start_cascade_rename(self, name: str) -> None:
        if not name:
            raise ValueError("Name can not be empty.")
        self._renaming_service.cascade_name_cell(name)
