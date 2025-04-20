import tkinter as tk

from controller.feature_controller import FeatureController
from controller.workbook_controller import WorkbookController  # adjust if needed
from model.app_state import AppState
from view.function_buttons import FunctionButtonSection
from view.output_section import OutputSection
from view.workbook_selector import WorkbookSelector


class MainView:
    def __init__(self, workbook_controller: WorkbookController, feature_controller: FeatureController,
                 app_state: AppState):
        self.workbook_controller = workbook_controller
        self.feature_controller = feature_controller
        self.app_state = app_state

        self.root = tk.Tk()
        self.root.title("Spreadsheet Explorer")
        self.root.geometry("750x550")

        self.icon = tk.PhotoImage(file="assets/spreadsheet_explorer_icon.png")
        self.root.iconphoto(True, self.icon)

        # === Create components but delay layout ===
        self.output = OutputSection(self.root, pack=False)
        self.buttons = FunctionButtonSection(self.root, self.output, self.feature_controller, self.app_state,
                                             pack=False)
        self.workbook_selector = WorkbookSelector(self.root, self.buttons, self.output, self.workbook_controller,self.app_state,
                                                  pack=False)

        # === Pack components in correct top-down order ===
        self.workbook_selector.pack()

        # Selected range (static for now)
        self.selected_range_label = tk.Label(
            self.root,
            text="Selected Range: A1",
            font=("Arial", 12, "bold"),
            anchor="w",
            padx=20
        )
        self.selected_range_label.pack(fill="x", pady=(0, 10))

        self.buttons.pack()

        self.output.pack()

        self.app_state.selected_cell.add_observer(lambda new_value, old_value: self.selected_range_label.config(
            text=f"Selected Range: {new_value.address if new_value else 'None'}"))

    def run(self):
        self.root.mainloop()
