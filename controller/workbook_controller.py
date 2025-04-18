from model.services.connected_workbook_service import ConnectedWorkbookService


class WorkbookController:
    def __init__(self, connected_workbook_service: ConnectedWorkbookService):
        self._connected_workbook_service = connected_workbook_service

    def get_open_workbooks(self) -> list[str]:
        return self._connected_workbook_service.get_connection_service().get_open_workbooks()

    def connect_and_parse_workbook(self, filename: str) -> None:
        self._connected_workbook_service.connect_and_parse_workbook(filename)


    def disconnect_workbook(self) -> None:
        self._connected_workbook_service.disconnect_workbook()