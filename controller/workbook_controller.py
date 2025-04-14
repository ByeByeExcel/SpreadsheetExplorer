from model.services.connected_workbook_service import ConnectedWorkbookService


class WorkbookController:
    def __init__(self, activeWorkbookService: ConnectedWorkbookService):
        self._spreadsheet_service = activeWorkbookService

    def get_open_workbooks(self) -> [str]:
        return self._spreadsheet_service.get_connection_service().get_open_workbooks()

    def connect_and_parse_workbook(self, filename: str) -> None:
        self._spreadsheet_service.connect_and_parse_workbook(filename)

    def is_connected_to_workbook(self) -> bool:
        return self._spreadsheet_service.is_connected_to_workbook()
