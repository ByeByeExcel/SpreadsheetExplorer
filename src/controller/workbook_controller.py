from model.services.connected_workbook_service import ConnectedWorkbookService


class WorkbookController:
    def __init__(self, connected_workbook_service: ConnectedWorkbookService):
        self._connected_workbook_service = connected_workbook_service

    def get_open_workbooks(self) -> list[str]:
        return self._connected_workbook_service.connection_service.get_open_workbooks()

    def connect_and_parse_workbook(self, filename: str) -> None:
        self._connected_workbook_service.connect_workbook(filename)
        self._connected_workbook_service.parse_connected_workbook()

    def parse_connected_workbook(self) -> None:
        self._connected_workbook_service.parse_connected_workbook()

    def disconnect_workbook(self) -> None:
        self._connected_workbook_service.disconnect_workbook()

    def set_tk_root(self, tk_root):
        self._connected_workbook_service.set_root(tk_root)
