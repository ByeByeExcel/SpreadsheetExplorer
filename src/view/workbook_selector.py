import tkinter as tk
from tkinter import ttk

from src.controller.workbook_controller import WorkbookController


class WorkbookSelector:
    def __init__(self, master, function_buttons, output, workbook_controller: WorkbookController, app_state, pack=True):
        self.workbook_controller = workbook_controller
        self.output = output
        self.function_buttons = function_buttons
        self.app_state = app_state

        self.frame = tk.Frame(master, padx=20, pady=10)
        if pack:
            self.pack()

        tk.Label(self.frame, text="Select an open Excel workbook:", font=("Arial", 12)).pack(anchor="w")

        self.workbook_var = tk.StringVar()
        self.workbook_dropdown = tk.OptionMenu(self.frame, self.workbook_var, "")
        self.workbook_dropdown.config(width=55)
        self.workbook_dropdown.pack(pady=(5, 0))

        button_frame = tk.Frame(self.frame)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Refresh Workbook List", command=self.refresh_workbook_list).pack(side="left", padx=10)

        self.analyze_button = tk.Button(button_frame, text="Analyze Workbook", command=self.analyze_workbook)
        self.analyze_button.pack(side="left", padx=10)

        # Separator at bottom
        ttk.Separator(self.frame, orient="horizontal").pack(fill="x", pady=(15, 0))

        self.refresh_workbook_list()

        # Observer: log when connection state changes
        self.app_state.is_connected_to_workbook.add_observer(self._on_connection_change)

    def refresh_workbook_list(self):
        try:
            workbooks = self.workbook_controller.get_open_workbooks()
            if not workbooks:
                self.output.write("[INFO] No open workbooks found.")
                self.analyze_button.config(state=tk.DISABLED)
                return

            menu = self.workbook_dropdown["menu"]
            menu.delete(0, "end")
            for wb in workbooks:
                menu.add_command(label=wb, command=lambda w=wb: self.workbook_var.set(w))
            self.workbook_var.set(workbooks[0])

            self.analyze_button.config(state=tk.NORMAL)
            self.output.write(f"[INFO] Found {len(workbooks)} workbook(s).")
        except Exception as e:
            self.output.write(f"[ERROR] Failed to fetch workbooks: {e}")
            self.analyze_button.config(state=tk.DISABLED)

    def analyze_workbook(self):
        selected = self.workbook_var.get()
        if selected:
            try:
                self.workbook_controller.connect_and_parse_workbook(selected)

                self.output.write(f"[ANALYZED] Workbook '{selected}' loaded and parsed.")
            except Exception as e:
                self.output.write(f"[ERROR] Could not analyze workbook: {e}")
                self.app_state.is_connected_to_workbook.set_value(False)
        else:
            self.output.write("[WARNING] No workbook selected.")
            self.app_state.is_connected_to_workbook.set_value(False)

    def _on_connection_change(self, new_value, old_value):
        if new_value:
            self.output.write("[INFO] Workbook is now connected and ready.")
        else:
            self.output.write("[INFO] Workbook disconnected or failed to load.")

    def pack(self):
        self.frame.pack(fill="x")
