from src.controller.feature_controller import FeatureController
from src.controller.workbook_controller import WorkbookController
from src.model.app_state import AppState
from src.model.services.connected_workbook_service import ConnectedWorkbookService
from src.model.services.functionality.interactive_painting.interactive_painting_service import \
    InteractivePaintingService
from src.model.services.functionality.one_time_painting.painting_service import PaintingService
from src.model.services.functionality.renaming_service import RenamingService
from src.model.services.spreadsheet_connection.excel_connection.excel_connection_service import ExcelConnectionService
from src.model.services.spreadsheet_connection.i_spreadsheet_connection_service import ISpreadsheetConnectionService
from src.view.main_view import MainView


def run_view():
    app_state: AppState = AppState()

    connection_service: ISpreadsheetConnectionService = ExcelConnectionService()

    connected_workbook_service: ConnectedWorkbookService = ConnectedWorkbookService(connection_service, app_state)

    interactive_painting_service: InteractivePaintingService = InteractivePaintingService(app_state)
    painting_service: PaintingService = PaintingService(app_state)
    renaming_service: RenamingService = RenamingService(app_state)

    workbook_controller = WorkbookController(connected_workbook_service)
    feature_controller = FeatureController(interactive_painting_service, painting_service, renaming_service, app_state)
    app = MainView(workbook_controller, feature_controller, app_state)
    app.run()
