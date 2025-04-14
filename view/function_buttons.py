import logging
import tkinter as tk
from tkinter import messagebox

from controller.feature_controller import FeatureController


class FunctionButtonSection:
    def __init__(self, master, output, feature_controller: FeatureController, pack=True):
        self.output = output
        self.feature_controller = feature_controller
        self.frame = tk.Frame(master, padx=20)

        if pack:
            self.pack()

        logging.debug("FunctionButtonSection initialized with controller: %s", self.feature_controller)

        # === Function 1 ===
        self.btn_func1 = tk.Button(
            self.frame,
            text="See dependents/precedents",
            width=25,
            height=1,
            state=tk.DISABLED,
            command=self.run_highlight_dependents
        )
        self.btn_func1.grid(row=0, column=0, sticky="w", pady=4)

        tk.Button(
            self.frame,
            text="?",
            width=2,
            command=lambda: self.show_help("Function 1", "This function highlights dependents and precedents.")
        ).grid(row=0, column=1)

        # === Heatmap Toggle Button ===
        self.heatmap_active = False
        self.btn_heatmap = tk.Button(
            self.frame,
            text="Show Heatmap",
            width=25,
            height=1,
            state=tk.DISABLED,
            command=self.toggle_heatmap
        )
        self.btn_heatmap.grid(row=1, column=0, sticky="w", pady=4)

        tk.Button(
            self.frame,
            text="?",
            width=2,
            command=lambda: self.show_help("Heatmap", "Toggles a heatmap view of the spreadsheet.")
        ).grid(row=1, column=1)

        # === Function 3 placeholder ===
        self.btn_func3 = tk.Button(
            self.frame,
            text="Function 3",
            width=25,
            height=1,
            state=tk.DISABLED,
            command=lambda: self.output.write("[Function 3] Coming soon...")
        )
        self.btn_func3.grid(row=2, column=0, sticky="w", pady=4)

        tk.Button(
            self.frame,
            text="?",
            width=2,
            command=lambda: self.show_help("Function 3", "Coming soon.")
        ).grid(row=2, column=1)

    def run_highlight_dependents(self):
        try:
            print("[DEBUG] Button clicked: Function 1")
            self.output.write("[DEBUG] Running highlight_dependents_precedents...")
            self.feature_controller.interactive_highlight_dependents_precedents()
            self.output.write("[Highlighting] Highlighted dependents and precedents.")
        except Exception as e:
            self.output.write(f"[ERROR] Highlighting failed: {e}")

    def toggle_heatmap(self):
        try:
            if not self.heatmap_active:
                self.feature_controller.show_heatmap()
                self.btn_heatmap.config(bg="orange", text="Hide Heatmap")
                self.output.write("[Heatmap] Activated.")
            else:
                self.feature_controller.reset_all_painters()
                self.btn_heatmap.config(bg=self.frame.cget("bg"), text="Show Heatmap")
                self.output.write("[Heatmap] Deactivated.")
            self.heatmap_active = not self.heatmap_active
        except Exception as e:
            self.output.write(f"[ERROR] Heatmap toggle failed: {e}")

    def show_help(self, title, description):
        messagebox.showinfo(title, description)

    def set_buttons_state(self, state):
        self.btn_func1.config(state=state)
        self.btn_heatmap.config(state=state)
        self.btn_func3.config(state=state)

    def pack(self):
        self.frame.pack(fill="x", anchor="w")
