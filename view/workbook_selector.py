import tkinter as tk
from tkinter import ttk

class WorkbookSelector:
    def __init__(self, master, function_buttons, output, pack=True):
        self.controller = self._get_controller()
        self.output = output
        self.function_buttons = function_buttons
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
        tk.Button(button_frame, text="Connect", command=self.connect_to_workbook).pack(side="left", padx=10)


        # Only refresh if output is already provided (prevents startup crash)
        if self.output:
            self.refresh_workbook_list()

        separator = ttk.Separator(self.frame, orient="horizontal")
        separator.pack(fill="x", pady=(15, 0))

    def _get_controller(self):
        from controller.controller import Controller
        from model.services.active_workbook_service import ActiveWorkbookService
        return Controller(ActiveWorkbookService())

    def refresh_workbook_list(self):
        try:
            workbooks = self.controller.get_open_workbooks()
            if not workbooks:
                self.output.write("[INFO] No open workbooks found.")
                return

            menu = self.workbook_dropdown["menu"]
            menu.delete(0, "end")
            for wb in workbooks:
                menu.add_command(label=wb, command=lambda w=wb: self.workbook_var.set(w))
            self.workbook_var.set(workbooks[0])
            self.output.write(f"[INFO] Found {len(workbooks)} workbook(s).")
        except Exception as e:
            self.output.write(f"[ERROR] Failed to fetch workbooks: {e}")

    def connect_to_workbook(self):
        selected = self.workbook_var.get()
        if selected:
            self.function_buttons.set_buttons_state(tk.NORMAL)
            self.output.write(f"[CONNECTED] Workbook selected: '{selected}'")
        else:
            self.function_buttons.set_buttons_state(tk.DISABLED)
            self.output.write("[WARNING] No workbook selected.")

    def pack(self):
        self.frame.pack(fill="x")
