from model.services.active_workbook_service import ActiveWorkbookService


class Controller:
    def __init__(self, activeWorkbookService: ActiveWorkbookService):
        self._spreadsheet_service = activeWorkbookService

    def get_open_workbooks(self) -> [str]:
        return self._spreadsheet_service.get_connection_service().get_open_workbooks()

    def connect_and_parse_workbook(self, filename: str) -> None:
        self._spreadsheet_service.connect_and_parse_workbook(filename)

    def is_connected_to_workbook(self) -> bool:
        return self._spreadsheet_service.is_connected_to_workbook()

    def highlight_dependents_precedents(self) -> None:
        if not self._spreadsheet_service.is_connected_to_workbook():
            raise Exception("No workbook is connected.")
        self._spreadsheet_service.highlight_dependents_precedents()

    def stop_watchers(self) -> None:
        if not self._spreadsheet_service.is_connected_to_workbook():
            raise Exception("No workbook is connected.")
        self._spreadsheet_service.stop_watchers()
