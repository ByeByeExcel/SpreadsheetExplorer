from typing import Optional

from model.app_state import AppState
from model.feature import Feature
from model.models.formula_context_information import FormulaContextInformation
from model.services.functionality.interactive_painting.interactive_context_service import InteractiveContextService
from model.services.functionality.interactive_painting.interactive_painting_service import \
    InteractivePaintingService
from model.services.functionality.one_time_painting.painting_service import PaintingService
from model.services.functionality.renaming_service import RenamingService


class FeatureController:
    def __init__(self,
                 interactive_painting_service: InteractivePaintingService,
                 interactive_context_service: InteractiveContextService,
                 painting_service: PaintingService,
                 renaming_service: RenamingService,
                 app_state: AppState):
        self._interactive_painting_service = interactive_painting_service
        self._interactive_context_service = interactive_context_service
        self._painting_service = painting_service
        self._renaming_service = renaming_service
        self._app_state = app_state

    # interactive features
    def start_dependency_highlighting(self) -> None:
        self._interactive_painting_service.highlight_dependents_precedents()
        self.start_context_information()

    def stop_dependency_highlighting(self) -> None:
        self._interactive_painting_service.stop_dependency_highlighting()
        self.stop_context_information()

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
    def start_cascade_rename(self) -> None:
        self._app_state.set_feature_active(Feature.CASCADE_RENAME)

    def stop_cascade_rename(self) -> None:
        self._app_state.set_feature_inactive(Feature.CASCADE_RENAME)

    def cascade_rename(self, name: str) -> None:
        if not name.strip():
            raise ValueError("Name cannot be empty.")
        self._renaming_service.cascade_name_cell(name)

    # context information
    def start_context_information(self) -> None:
        self._interactive_context_service.start_basic_cell_information()

    def stop_context_information(self) -> None:
        self._interactive_context_service.stop()
