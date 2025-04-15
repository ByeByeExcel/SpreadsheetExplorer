from model.app_state import AppState
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
    def interactive_highlight_dependents_precedents(self, workbook: IConnectedWorkbook = None) -> None:
        if workbook:
            self._interactive_painting_service.highlight_dependents_precedents(workbook)
        else:
            for connected_workbook in self._app_state.get_connected_workbooks().values():
                self._interactive_painting_service.highlight_dependents_precedents(connected_workbook)

    def stop_all_watchers(self) -> None:
        self._interactive_painting_service.stop_all()

    # one-time painting features
    def show_heatmap(self, workbook: IConnectedWorkbook = None) -> None:
        if workbook:
            self._painting_service.show_heatmap(workbook)
        else:
            for connected_workbook in self._app_state.get_connected_workbooks().values():
                self._painting_service.show_heatmap(connected_workbook)

    def show_root_nodes(self, workbook: IConnectedWorkbook = None) -> None:
        if workbook:
            self._painting_service.show_root_nodes(workbook)
        else:
            for connected_workbook in self._app_state.get_connected_workbooks().values():
                self._painting_service.show_root_nodes(connected_workbook)

    def reset_all_painters(self) -> None:
        self._painting_service.reset_all_painters()

    # cascade renaming
    def cascade_rename(self, name: str) -> None:
        self._renaming_service.cascade_name_cell(name, self._app_state.selected_cell.value)
