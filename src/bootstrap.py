from controller.feature_controller import FeatureController
from controller.workbook_controller import WorkbookController
from model.services.service_registry import ServiceRegistry
from view.main_view import MainView


def run_app():
    """Entry point to initialize services, controllers, and launch the main UI."""
    services = ServiceRegistry()
    app = build_main_view(services)
    app.run()


def build_main_view(services: ServiceRegistry) -> MainView:
    workbook_controller = WorkbookController(
        services.connected_workbook_service,
        services.connection_service
    )

    feature_controller = FeatureController(
        services.selection_coloring_service,
        services.feature_coloring_service,
        services.renaming_service,
        services.app_state
    )
    return MainView(workbook_controller, feature_controller, services.app_state)
