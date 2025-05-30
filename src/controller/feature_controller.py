from model.domain_model.feature import Feature
from model.services.app_state_service import AppStateService
from model.services.connected_workbook_service import ConnectedWorkbookService
from model.services.features.coloring.interactive.selection_coloring_service import \
    SelectionColoringService
from model.services.features.coloring.static.feature_coloring_service import FeatureColoringService
from model.services.features.renaming.renaming_service import RenamingService


class FeatureController:
    def __init__(self,
                 interactive_painting_service: SelectionColoringService,
                 painting_service: FeatureColoringService,
                 renaming_service: RenamingService,
                 app_state: AppStateService,
                 connected_workbook_service: ConnectedWorkbookService) -> None:
        self._interactive_painting_service = interactive_painting_service
        self._painting_service = painting_service
        self._renaming_service = renaming_service
        self._app_state = app_state
        self._connected_workbook_service = connected_workbook_service

    # interactive features
    def start_dependency_highlighting(self) -> None:
        self._interactive_painting_service.start_dependency_highlighting()

    def stop_dependency_highlighting(self) -> None:
        self._interactive_painting_service.stop_dependency_highlighting()

    # one-time painting features
    def show_heatmap(self) -> None:
        self._painting_service.show_feature_coloring(Feature.DEPENDENTS_HEATMAP)

    def hide_heatmap(self) -> None:
        self._painting_service.stop_feature_coloring(Feature.DEPENDENTS_HEATMAP)

    def show_root_nodes(self) -> None:
        self._painting_service.show_feature_coloring(Feature.ROOT_NODES)

    def hide_root_nodes(self) -> None:
        self._painting_service.stop_feature_coloring(Feature.ROOT_NODES)

    # cascade renaming
    def activate_cascade_rename(self) -> None:
        self._app_state.set_feature_active(Feature.CASCADE_RENAME)

    def deactivate_cascade_rename(self) -> None:
        self._app_state.set_feature_inactive(Feature.CASCADE_RENAME)

    def cascade_rename(self, name: str) -> None:
        if not name.strip():
            raise ValueError("Name cannot be empty.")
        self._renaming_service.cascade_name_cell(name)
        self._connected_workbook_service.parse_connected_workbook()
