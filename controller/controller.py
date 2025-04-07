from model.services.active_workbook_service import ActiveWorkbookService


class Controller:
    def __init__(self, activeWorkbookService: ActiveWorkbookService):
        self._spreadsheet_service = activeWorkbookService

    def get_open_workbooks(self) -> [str]:
        return self._spreadsheet_service.get_connection_service().get_open_workbooks()

    def connect_to_workbook(self, filename: str) -> None:
        self._spreadsheet_service.get_connection_service().connect_to_workbook(filename)
