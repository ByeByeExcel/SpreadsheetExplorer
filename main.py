from controller.controller import Controller
from model.services.active_workbook_service import ActiveWorkbookService
from view.main_window import run_view

if __name__ == "__main__":
    active_workbook_service = ActiveWorkbookService()
    controller = Controller(active_workbook_service)

    run_view()
