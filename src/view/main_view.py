import tkinter as tk

from controller.feature_controller import FeatureController
from controller.workbook_controller import WorkbookController
from model.app_state import AppState
from view.function_buttons import FunctionButtonSection
from view.output_section import OutputSection
from view.workbook_selector import WorkbookSelector
from view.context_info_table import ContextInfoTable


class MainView:
    def __init__(self, workbook_controller: WorkbookController, feature_controller: FeatureController,
                 app_state: AppState):
        self.workbook_controller = workbook_controller
        self.feature_controller = feature_controller
        self.app_state = app_state

        self.root = tk.Tk()
        self.root.title("Spreadsheet Explorer")
        self.root.geometry("950x600")  # Reduced height for compact layout

        self.icon = tk.PhotoImage(file="assets/spreadsheet_explorer_icon.png")
        self.root.iconphoto(True, self.icon)

        # === Create layout containers ===
        self.selector_frame = tk.Frame(self.root)
        self.middle_frame = tk.Frame(self.root)

        # === Create components ===
        self.output = OutputSection(self.root, app_state=self.app_state, pack=False)
        self.buttons = FunctionButtonSection(self.middle_frame, None, self.feature_controller, self.app_state, pack=False)
        self.workbook_selector = WorkbookSelector(self.selector_frame, self.output, self.workbook_controller, self.app_state, pack=False)
        self.context_table = ContextInfoTable(self.middle_frame, self.app_state)

        # === Layout ===
        self.selector_frame.pack(fill="x", padx=10, pady=(10, 5))
        self.workbook_selector.pack()

        self.selected_range_label = tk.Label(
            self.root,
            text="Selected Range: A1",
            font=("Arial", 12, "bold"),
            anchor="w",
            padx=20
        )
        self.selected_range_label.pack(fill="x", pady=(0, 5))

        self.middle_frame.pack(fill="both", expand=False, padx=10)
        self.buttons.frame.pack(side="left", anchor="n", padx=(0, 10))
        self.context_table.pack(side="left", fill="x", expand=True)

        self.output.frame.pack(fill="x", padx=10, pady=(10, 5))

        self.app_state.selected_cell.add_observer(lambda new_value, old_value: self.selected_range_label.config(
            text=f"Selected Range: {new_value.address if new_value else 'None'}"))

    def run(self):
        self.root.mainloop()
