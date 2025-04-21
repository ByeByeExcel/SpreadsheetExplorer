import tkinter as tk
from tkinter import ttk
import threading


class WorkbookSelector:
    def __init__(self, master, button_section, output, workbook_controller, app_state, pack=True):
        self.master = master
        self.output = output
        self.app_state = app_state
        self.workbook_controller = workbook_controller

        self.frame = tk.Frame(master, padx=20)

        # Label and Dropdown
        tk.Label(self.frame, text="Select an open Excel workbook:").pack(anchor="w")
        self.dropdown = ttk.Combobox(self.frame, state="readonly", width=50)
        self.dropdown.pack(fill="x", pady=(0, 10))

        # Unified button row
        button_row = tk.Frame(self.frame)
        self.refresh_button = tk.Button(button_row, text="Refresh Workbook List", command=self.refresh_workbooks)
        self.analyze_button = tk.Button(button_row, text="Analyze Workbook", command=self.analyze_workbook)
        self.reanalyze_button = tk.Button(button_row, text="Reanalyze Workbook", command=self.reanalyze_workbook)
        self.disconnect_button = tk.Button(button_row, text="Disconnect Workbook", command=self.disconnect_workbook)

        for btn in [self.refresh_button, self.analyze_button, self.reanalyze_button, self.disconnect_button]:
            btn.pack(side="left", padx=5)

        button_row.pack(anchor="center", pady=(0, 10))
        separator = tk.Frame(self.frame, height=1, bd=0, relief="groove", bg="#ccc")
        separator.pack(fill="x", padx=0, pady=(5, 10))

        # Observe state changes
        self.app_state.is_connected_to_workbook.add_observer(lambda *_: self.update_button_states())
        self.app_state.active_feature.add_observer(lambda new, old: self.update_button_states())

        # Refresh list on init
        self.refresh_workbooks()
        self.update_button_states()

        if pack:
            self.pack()

    def pack(self):
        self.frame.pack(anchor="w", pady=(10, 5), fill="x")

    def refresh_workbooks(self):
        try:
            self.output.write("[INFO] Refreshing workbook list...")
            workbooks = self.workbook_controller.get_open_workbooks()
            self.dropdown["values"] = workbooks
            if workbooks:
                self.dropdown.set(workbooks[0])
            else:
                self.dropdown.set("")
            self.output.write(f"[INFO] Found {len(workbooks)} workbook(s).")
        except Exception as e:
            self.output.write(f"[ERROR] Failed to refresh workbooks: {str(e)}")

    def analyze_workbook(self):
        selected = self.dropdown.get()
        if selected:
            def run():
                self.workbook_controller.connect_and_parse_workbook(selected)
                self.output.write(f"[INFO] '{selected}' analyzed")

            threading.Thread(target=run).start()
        else:
            self.output.write("[ERROR] No workbook selected.")

    def reanalyze_workbook(self):
        selected = self.app_state.get_connected_workbook()
        if selected:
            self.output.write(f"[INFO] Reanalysis of '{selected}' started.")
            threading.Thread(target=self.workbook_controller.parse_connected_workbook).start()
        else:
            self.output.write("[ERROR] Unable to complete reanalysis: no workbook connected.")

    def disconnect_workbook(self):
        selected = self.app_state.get_connected_workbook()
        if selected:
            threading.Thread(target=self.workbook_controller.disconnect_workbook).start()
            self.output.write(f"[INFO] '{selected}' disconnected.")
        else:
            self.output.write("[ERROR] Could not disconnect.")

    def update_button_states(self):
        connected = self.app_state.is_connected_to_workbook.value
        feature_active = self.app_state.active_feature.value is not None

        def set(w, e): w.config(state=tk.NORMAL if e else tk.DISABLED)

        dropdown_state, states = (
            ("disabled", {b: False for b in
                          [self.refresh_button, self.analyze_button, self.reanalyze_button, self.disconnect_button]})
            if feature_active else
            ("readonly", {self.refresh_button: True, self.analyze_button: True, self.reanalyze_button: False,
                          self.disconnect_button: False})
            if not connected else
            ("disabled", {self.refresh_button: False, self.analyze_button: False, self.reanalyze_button: True,
                          self.disconnect_button: True})
        )

        self.dropdown.config(state=dropdown_state)
        for b, enabled in states.items(): set(b, enabled)
