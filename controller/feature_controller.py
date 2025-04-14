from model.models.i_connected_workbook import IConnectedWorkbook
from model.services.connected_workbook_service import ConnectedWorkbookService
from model.services.functionality.interactive_painting.interactive_painting_service import InteractivePaintingService
from model.services.functionality.one_time_painting.painting_service import PaintingService


class FeatureController:
    def __init__(self,
                 connected_workbook_service: ConnectedWorkbookService,
                 interactive_painting_service: InteractivePaintingService,
                 painting_service: PaintingService):

        self._connected_workbook_service = connected_workbook_service
        self._interactive_painting_service = interactive_painting_service
        self._painting_service = painting_service

    # interactive features
    def interactive_highlight_dependents_precedents(self, workbook: IConnectedWorkbook = None) -> None:
        if workbook:
            self._interactive_painting_service.highlight_dependents_precedents(workbook)
        else:
            for connected_workbook in self._connected_workbook_service.get_connected_workbooks().values():
                self._interactive_painting_service.highlight_dependents_precedents(connected_workbook)

    def stop_all_watchers(self) -> None:
        self._interactive_painting_service.stop_all_watchers()

    # one-time painting features
    def show_heatmap(self, workbook: IConnectedWorkbook = None) -> None:
        if workbook:
            self._painting_service.show_heatmap(workbook)
        else:
            for connected_workbook in self._connected_workbook_service.get_connected_workbooks().values():
                self._painting_service.show_heatmap(connected_workbook)

    def reset_all_painters(self) -> None:
        self._painting_service.reset_all_painters()
