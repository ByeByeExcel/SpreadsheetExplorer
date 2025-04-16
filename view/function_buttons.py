import logging
import tkinter as tk
from tkinter import messagebox

from controller.feature_controller import FeatureController
from model.app_state import AppState
from model.feature import Feature


class FunctionButtonSection:
    def __init__(self, master, output, feature_controller: FeatureController, app_state: AppState, pack=True):
        self.output = output
        self.feature_controller = feature_controller
        self.app_state = app_state
        self.frame = tk.Frame(master, padx=20)

        if pack:
            self.pack()

        logging.debug("FunctionButtonSection initialized with controller: %s", self.feature_controller)

        # === Function 1 ===
        self.dependency_highlighting = tk.Button(
            self.frame,
            text="Show dependents/precedents",
            width=25,
            height=1,
            state=tk.DISABLED,
            command=self.toggle_dependency_highlighting
        )
        self.dependency_highlighting.grid(row=0, column=0, sticky="w", pady=4)

        tk.Button(
            self.frame,
            text="?",
            width=2,
            command=lambda: self.show_help("Function 1", "This function highlights dependents and precedents.")
        ).grid(row=0, column=1)

        # === Heatmap Toggle Button ===
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

    def toggle_dependency_highlighting(self):
        try:
            if not self.app_state.is_active(Feature.DEPENDENCY_HIGHLIGHTING):
                self.feature_controller.start_dependency_highlighting()
                self.dependency_highlighting.config(bg="orange", text="Hide dependents/precedents")
                self.output.write("[Dependency Highlighting] Activated.")
            else:
                self.feature_controller.stop_dependency_highlighting()
                self.dependency_highlighting.config(bg=self.frame.cget("bg"), text="Show dependents/precedents")
                self.output.write("[Dependency Highlighting] Deactivated.")
        except Exception as e:
            self.output.write(f"[ERROR] Dependency Highlighting toggle failed: {e}")

    def toggle_heatmap(self):
        try:
            if not self.app_state.is_active(Feature.DEPENDENTS_HEATMAP):
                self.feature_controller.show_heatmap()
                self.btn_heatmap.config(bg="orange", text="Hide Heatmap")
                self.output.write("[Heatmap] Activated.")
            else:
                self.feature_controller.hide_heatmap()
                self.btn_heatmap.config(bg=self.frame.cget("bg"), text="Show Heatmap")
                self.output.write("[Heatmap] Deactivated.")
        except Exception as e:
            self.output.write(f"[ERROR] Heatmap toggle failed: {e}")

    def set_buttons_state(self, state):
        self.dependency_highlighting.config(state=state)
        self.btn_heatmap.config(state=state)
        self.btn_func3.config(state=state)

    def pack(self):
        self.frame.pack(fill="x", anchor="w")

    @staticmethod
    def show_help(title, description):
        messagebox.showinfo(title, description)
