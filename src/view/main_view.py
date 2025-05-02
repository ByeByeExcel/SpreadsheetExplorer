import tkinter as tk

from controller.feature_controller import FeatureController
from controller.workbook_controller import WorkbookController
from model.services.app_state_service import AppStateService
from view.function_buttons_section import FunctionButtonSection
from view.output_section import OutputSection
from view.utils.context_information_table_manager import ContextInformationManager
from view.widgets.context_info_table_widget import ContextInfoTable
from view.workbook_selector import WorkbookSelector


class MainView:
    def __init__(self, workbook_controller: WorkbookController, feature_controller: FeatureController,
                 app_state: AppStateService):
        self.workbook_controller = workbook_controller
        self.feature_controller = feature_controller
        self.app_state = app_state

        self.root = tk.Tk()
        self.workbook_controller.set_tk_root(self.root)
        self.root.title("Spreadsheet Explorer")
        self.root.geometry("1050x600")

        self.icon = tk.PhotoImage(file="assets/spreadsheet_explorer_icon.png")
        self.root.iconphoto(True, self.icon)

        self.selector_frame = tk.Frame(self.root)
        self.middle_frame = tk.Frame(self.root)

        self.output = OutputSection(self.root, app_state=self.app_state, pack=False)

        self.buttons = FunctionButtonSection(self.middle_frame, self.output, self.feature_controller, self.app_state,
                                             pack=False)

        self.workbook_selector = WorkbookSelector(
            self.selector_frame,
            self.output,
            self.workbook_controller,
            self.app_state,
            pack=False
        )

        self.context_table = ContextInfoTable(self.middle_frame)

        self.context_manager = ContextInformationManager(
            self.context_table,
            self.feature_controller,
            self.app_state
        )

        self.selector_frame.pack(fill="x", padx=10, pady=(10, 5))
        self.workbook_selector.pack()

        self.middle_frame.pack(fill="both", expand=False, padx=10)

        self.buttons.frame.pack(side="left", anchor="n", padx=(0, 10))
        self.context_table.pack(side="left", fill="both", expand=True)

        self.output.frame.pack(fill="x", padx=10, pady=(10, 5))

    def run(self):
        self.root.mainloop()
