from model.services.app_state_service import AppStateService
from model.services.connected_workbook_service import ConnectedWorkbookService
from model.services.features.coloring.interactive.selection_coloring_service import SelectionColoringService
from model.services.features.coloring.static.feature_coloring_service import FeatureColoringService
from model.services.features.context_generation.selection_context_service import SelectionContextService
from model.services.features.renaming.renaming_service import RenamingService
from model.services.spreadsheet_connection.excel.excel_connection_service import ExcelConnectionService
from model.services.spreadsheet_connection.i_spreadsheet_connection_service import ISpreadsheetConnectionService


class ServiceRegistry:
    def __init__(self):
        self.app_state = AppStateService()

        # Connection services
        self.connection_service: ISpreadsheetConnectionService = ExcelConnectionService()
        self.connected_workbook_service = ConnectedWorkbookService(self.connection_service, self.app_state)

        # Feature services
        self.selection_coloring_service = SelectionColoringService(self.app_state)
        self.selection_context_service = SelectionContextService(self.app_state)
        self.feature_coloring_service = FeatureColoringService(self.app_state)
        self.renaming_service = RenamingService(self.app_state)
