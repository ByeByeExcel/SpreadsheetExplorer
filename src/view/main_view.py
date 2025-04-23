import tkinter as tk

from controller.feature_controller import FeatureController
from controller.workbook_controller import WorkbookController
from model.app_state import AppState
from view.function_buttons_section import FunctionButtonSection
from view.output_section import OutputSection
from view.workbook_selector import WorkbookSelector
from view.context_info_table import ContextInfoTable


class MainView:
    def __init__(self, workbook_controller: WorkbookController, feature_controller: FeatureController,
                 app_state: AppState):
        self.workbook_controller = workbook_controller
        self.feature_controller = feature_controller
        self.app_state = app_state

        # ✅ Set initial AppState values
        self.app_state.is_connected_to_workbook.set_value(False)
        self.app_state.is_analyzing.set_value(False)
        self.app_state.active_feature.set_value(None)

        self.root = tk.Tk()
        self.root.title("Spreadsheet Explorer")
        self.root.geometry("950x600")

        self.icon = tk.PhotoImage(file="assets/spreadsheet_explorer_icon.png")
        self.root.iconphoto(True, self.icon)

        self.selector_frame = tk.Frame(self.root)
        self.middle_frame = tk.Frame(self.root)

        self.output = OutputSection(self.root, app_state=self.app_state, pack=False)
        self.buttons = FunctionButtonSection(
            self.middle_frame,
            None,
            self.feature_controller,
            self.app_state,
            pack=False
        )
        self.workbook_selector = WorkbookSelector(
            self.selector_frame,
            self.output,
            self.workbook_controller,
            self.app_state,
            pack=False
        )
        self.context_table = ContextInfoTable(self.middle_frame, self.app_state)

        self.selector_frame.pack(fill="x", padx=10, pady=(10, 5))
        self.workbook_selector.pack()

        self.selected_range_label = tk.Label(
            self.root,
            text="Selected Range: None",
            font=("Arial", 12, "bold"),
            anchor="w",
            padx=20
        )
        self.selected_range_label.pack(fill="x", pady=(0, 5))
        self.app_state.selected_cell.add_observer(self._update_selected_range_label)

        self.middle_frame.pack(fill="both", expand=True)
        self.middle_frame.grid_columnconfigure(0, weight=0)
        self.middle_frame.grid_columnconfigure(1, weight=1)

        self.buttons.frame.grid(row=0, column=0, sticky="n", padx=(10, 20))
        self.context_table.grid(row=0, column=1, sticky="nsew", padx=(0, 10), pady=(0, 10))

        self.output.frame.pack(fill="x", padx=10, pady=(5, 10))

        self.buttons.manager.update_widgets()

    def _update_selected_range_label(self, new_cell, _):
        text = f"Selected Range: {new_cell.address}" if new_cell else "Selected Range: None"
        self.selected_range_label.config(text=text)

    def run(self):
        self.root.mainloop()
