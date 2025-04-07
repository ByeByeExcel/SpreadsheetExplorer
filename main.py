from controller.controller import Controller
from model.services.active_workbook_service import ActiveWorkbookService
from view.main_window import run_view

if __name__ == "__main__":
    activeWorkbookService = ActiveWorkbookService()
    controller = Controller(activeWorkbookService)

    run_view()
