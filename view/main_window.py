from controller.feature_controller import FeatureController
from controller.workbook_controller import WorkbookController
from model.app_state import AppState
from model.services.connected_workbook_service import ConnectedWorkbookService
from model.services.functionality.interactive_painting.interactive_painting_service import InteractivePaintingService
from model.services.functionality.one_time_painting.painting_service import PaintingService
from model.services.functionality.renaming_service import RenamingService
from model.services.spreadsheet_connection.excel_connection.excel_connection_service import ExcelConnectionService
from model.services.spreadsheet_connection.i_spreadsheet_connection_service import ISpreadsheetConnectionService
from model.services.spreadsheet_parser.excel_parser_service.excel_parser_service import ExcelParserService
from model.services.spreadsheet_parser.i_spreadsheet_parser_service import ISpreadsheetParserService
from view.main_view import MainView


def run_view():
    app_state: AppState = AppState()

    connection_service: ISpreadsheetConnectionService = ExcelConnectionService()
    parser_service: ISpreadsheetParserService = ExcelParserService()

    connected_workbook_service: ConnectedWorkbookService = ConnectedWorkbookService(connection_service,
                                                                                    parser_service,
                                                                                    app_state)

    interactive_painting_service: InteractivePaintingService = InteractivePaintingService(app_state)
    painting_service: PaintingService = PaintingService()
    renaming_service: RenamingService = RenamingService(app_state)

    workbook_controller = WorkbookController(connected_workbook_service)
    feature_controller = FeatureController(interactive_painting_service, painting_service, renaming_service, app_state)
    app = MainView(workbook_controller, feature_controller, app_state)
    app.run()
