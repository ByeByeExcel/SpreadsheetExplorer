from view.main_view import MainView
from controller.controller import Controller
from model.services.active_workbook_service import ActiveWorkbookService

def run_view():
    controller = Controller(ActiveWorkbookService())
    app = MainView(controller)
    app.run()
