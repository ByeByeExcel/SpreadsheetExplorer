import tkinter as tk
from tkinter import ttk


class WorkbookSelector:
    def __init__(self, master, function_buttons, output, controller, pack=True):
        self.controller = controller
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
        tk.Button(button_frame, text="Analyze Workbook", command=self.analyze_workbook).pack(side="left", padx=10)

        # Separator moved here so it's at the bottom
        ttk.Separator(self.frame, orient="horizontal").pack(fill="x", pady=(15, 0))

        self.refresh_workbook_list()

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

    def analyze_workbook(self):
        selected = self.workbook_var.get()
        if selected:
            try:
                self.output.write(f"[DEBUG] Selected workbook: {selected}")
                self.controller.connect_and_parse_workbook(selected)
                self.function_buttons.set_buttons_state(tk.NORMAL)
                self.output.write(f"[ANALYZED] Workbook '{selected}' loaded and parsed.")
            except Exception as e:
                self.output.write(f"[ERROR] Could not analyze workbook: {e}")
        else:
            self.function_buttons.set_buttons_state(tk.DISABLED)
            self.output.write("[WARNING] No workbook selected.")

    def pack(self):
        self.frame.pack(fill="x")
