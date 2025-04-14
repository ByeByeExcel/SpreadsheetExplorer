from model.models.i_connected_workbook import IConnectedWorkbook
from model.models.spreadsheet.spreadsheet_classes import CellDependencies
from model.services.spreadsheet_connection.i_spreadsheet_connection_service import ISpreadsheetConnectionService
from model.services.spreadsheet_parser.i_spreadsheet_parser_service import ISpreadsheetParserService


class ConnectedWorkbookService:
    _connected_workbooks: dict[str, IConnectedWorkbook] = {}

    def __init__(self, connection_service: ISpreadsheetConnectionService, parser_service: ISpreadsheetParserService):
        self._connection_service: ISpreadsheetConnectionService = connection_service
        self._parser_service: ISpreadsheetParserService = parser_service

    def get_connection_service(self) -> ISpreadsheetConnectionService:
        return self._connection_service

    def get_parser_service(self) -> ISpreadsheetParserService:
        return self._parser_service

    def get_connected_workbooks(self) -> dict[str, IConnectedWorkbook]:
        return self._connected_workbooks

    def get_connected_workbook(self, filename: str) -> IConnectedWorkbook:
        return self._connected_workbooks.get(filename)

    def is_connected_to_workbook(self) -> bool:
        return bool(self._connected_workbooks)

    def connect_and_parse_workbook(self, filename: str) -> None:
        connected_workbook: IConnectedWorkbook = self._connection_service.connect_to_workbook(filename)
        if not connected_workbook:
            raise Exception(f"Error connecting workbook '{filename}'")
        dependencies: CellDependencies = self._parser_service.get_dependencies(connected_workbook.fullpath)
        connected_workbook.cell_dependencies = dependencies
        self._connected_workbooks[connected_workbook.name] = connected_workbook
