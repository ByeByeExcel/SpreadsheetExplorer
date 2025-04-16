import logging
import tkinter as tk
from tkinter import messagebox

from controller.feature_controller import FeatureController
from model.feature import Feature
from model.app_state import AppState


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
        self.btn_func1 = tk.Button(
            self.frame,
            text="See dependents/precedents",
            width=25,
            height=1,
            state=tk.DISABLED,
            command=self.toggle_dependency_highlighting
        )
        self.btn_func1.grid(row=0, column=0, sticky="w", pady=4)

        tk.Button(
            self.frame,
            text="?",
            width=2,
            command=lambda: self.show_help("Function 1", "This function highlights dependents and precedents.")
        ).grid(row=0, column=1)

        self.dependency_highlighting = self.btn_func1

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

        # === Root Node Button ===
        self.btn_root_nodes = tk.Button(
            self.frame,
            text="Root Nodes",
            width=25,
            height=1,
            state=tk.DISABLED,
            command=self.toggle_root_nodes
        )
        self.btn_root_nodes.grid(row=2, column=0, sticky="w", pady=4)

        tk.Button(
            self.frame,
            text="?",
            width=2,
            command=lambda: self.show_help("Function 3", "This function identifies and highlights root nodes.")
        ).grid(row=2, column=1)

        self.btn_cascade_rename = tk.Button(
            self.frame,
            text="Cascade Rename",
            width=25,
            height=1,
            state=tk.DISABLED,
            command=lambda: self.output.write("[Cascade Rename] Coming soon...")
        )
        self.btn_cascade_rename.grid(row=3, column=0, sticky="w", pady=4)

        tk.Button(
            self.frame,
            text="?",
            width=2,
            command=lambda: self.show_help("Function 4", "This function will perform cascade renaming.")
        ).grid(row=3, column=1)

    def toggle_dependency_highlighting(self):
        try:
            if not self.app_state.is_active(Feature.DEPENDENCY_HIGHLIGHTING):
                self.feature_controller.start_dependency_highlighting()
                self.disable_all_except(self.dependency_highlighting)
                self.output.write("[Dependency Highlighting] Activated.")
            else:
                self.feature_controller.stop_dependency_highlighting()
                self.enable_all_buttons()
                self.output.write("[Dependency Highlighting] Deactivated.")
        except Exception as e:
            self.output.write(f"[ERROR] Dependency Highlighting failed: {e}")

    def toggle_heatmap(self):
        try:
            if not self.app_state.is_active(Feature.DEPENDENTS_HEATMAP):
                self.feature_controller.show_heatmap()
                self.btn_heatmap.config(bg="orange", text="Hide Heatmap")
                self.disable_all_except(self.btn_heatmap)
                self.output.write("[Heatmap] Activated.")
            else:
                self.feature_controller.hide_heatmap()
                self.btn_heatmap.config(bg=self.frame.cget("bg"), text="Show Heatmap")
                self.enable_all_buttons()
                self.output.write("[Heatmap] Deactivated.")
        except Exception as e:
            self.output.write(f"[ERROR] Heatmap toggle failed: {e}")

    def toggle_root_nodes(self):
        try:
            if not self.app_state.is_active(Feature.ROOT_NODES):
                self.feature_controller.show_root_nodes()
                self.btn_root_nodes.config(bg="orange", text="Hide Root Nodes")
                self.disable_all_except(self.btn_root_nodes)
                self.output.write("[Root Nodes] Activated.")
            else:
                self.feature_controller.hide_root_nodes()
                self.btn_root_nodes.config(bg=self.frame.cget("bg"), text="Root Nodes")
                self.enable_all_buttons()
                self.output.write("[Root Nodes] Deactivated.")
        except Exception as e:
            self.output.write(f"[ERROR] Root Nodes toggle failed: {e}")

    def disable_all_except(self, active_button):
        for button in [
            self.dependency_highlighting,
            self.btn_heatmap,
            self.btn_root_nodes,
            self.btn_cascade_rename
        ]:
            if button != active_button:
                button.config(state=tk.DISABLED)

    def enable_all_buttons(self):
        self.set_buttons_state(tk.NORMAL)

    def show_help(self, title, description):
        messagebox.showinfo(title, description)

    def set_buttons_state(self, state):
        self.btn_func1.config(state=state)
        self.btn_heatmap.config(state=state)
        self.btn_root_nodes.config(state=state)
        self.btn_cascade_rename.config(state=state)

    def pack(self):
        self.frame.pack(fill="x", anchor="w")
