from model.app_state import AppState
from model.feature import Feature
from model.models.i_connected_workbook import IConnectedWorkbook
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
    def start_dependency_highlighting(self, workbook: IConnectedWorkbook = None) -> None:
        if self._app_state.is_active(Feature.DEPENDENCY_HIGHLIGHTING):
            raise ValueError("Dependency highlighting is already active.")
        if workbook:
            self._interactive_painting_service.highlight_dependents_precedents(workbook)
        else:
            for connected_workbook in self._app_state.get_connected_workbooks().values():
                self._interactive_painting_service.highlight_dependents_precedents(connected_workbook)
        self._app_state.set_feature_active(Feature.DEPENDENCY_HIGHLIGHTING)

    def stop_dependency_highlighting(self) -> None:
        self._interactive_painting_service.stop_dependency_highlighting()
        self._app_state.set_feature_inactive(Feature.DEPENDENCY_HIGHLIGHTING)

    # one-time painting features
    def show_heatmap(self, workbook: IConnectedWorkbook = None) -> None:
        if self._app_state.is_active(Feature.DEPENDENTS_HEATMAP):
            raise ValueError("Heatmap is already active.")
        if workbook:
            self._painting_service.show_heatmap(workbook)
        else:
            for connected_workbook in self._app_state.get_connected_workbooks().values():
                self._painting_service.show_heatmap(connected_workbook)
        self._app_state.set_feature_active(Feature.DEPENDENTS_HEATMAP)

    def hide_heatmap(self) -> None:
        self._painting_service.stop_heatmap()
        self._app_state.set_feature_inactive(Feature.DEPENDENTS_HEATMAP)

    def show_root_nodes(self, workbook: IConnectedWorkbook = None) -> None:
        if workbook:
            self._painting_service.show_root_nodes(workbook)
        else:
            for connected_workbook in self._app_state.get_connected_workbooks().values():
                self._painting_service.show_root_nodes(connected_workbook)

    def hide_root_nodes(self) -> None:
        self._painting_service.stop_root_nodes()
        self._app_state.set_feature_inactive(Feature.ROOT_NODES)

    def stop_all_painters(self) -> None:
        self._painting_service.stop_all()
        self._app_state.set_feature_inactive(Feature.DEPENDENTS_HEATMAP)
        self._app_state.set_feature_inactive(Feature.ROOT_NODES)

    # cascade renaming
    def start_cascade_rename(self, name: str) -> None:
        if self._app_state.is_active(Feature.CASCADE_RENAME):
            raise ValueError("Cascade renaming is already active.")
        self._app_state.set_feature_active(Feature.CASCADE_RENAME)
        self._renaming_service.cascade_name_cell(name, self._app_state.selected_cell.value)
        self._app_state.set_feature_inactive(Feature.CASCADE_RENAME)
