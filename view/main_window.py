from controller.feature_controller import FeatureController
from model.services.functionality.interactive_painting.interactive_painting_service import InteractivePaintingService
from model.services.functionality.one_time_painting.painting_service import PaintingService
from model.services.spreadsheet_connection.excel_connection.excel_connection_service import ExcelConnectionService
from model.services.spreadsheet_connection.i_spreadsheet_connection_service import ISpreadsheetConnectionService
from model.services.spreadsheet_parser.excel_parser_service.excel_parser_service import ExcelParserService
from model.services.spreadsheet_parser.i_spreadsheet_parser_service import ISpreadsheetParserService
from view.main_view import MainView
from controller.workbook_controller import WorkbookController
from model.services.connected_workbook_service import ConnectedWorkbookService


def run_view():
    # Initialize the connection and parser services
    connection_service: ISpreadsheetConnectionService = ExcelConnectionService()
    parser_service: ISpreadsheetParserService = ExcelParserService()

    # Create the connected workbook service
    connected_workbook_service: ConnectedWorkbookService = ConnectedWorkbookService(connection_service, parser_service)

    interactive_painting_service: InteractivePaintingService = InteractivePaintingService()
    painting_service: PaintingService = PaintingService()

    workbook_controller = WorkbookController(connected_workbook_service)
    feature_controller = FeatureController(connected_workbook_service, interactive_painting_service, painting_service)
    app = MainView(workbook_controller, feature_controller)
    app.run()
