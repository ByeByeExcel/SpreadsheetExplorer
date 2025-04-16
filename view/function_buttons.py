import logging
import re
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

        self.root_nodes_active = False

        # === Row 0: Dependency Highlighting ===
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
        ).grid(row=0, column=3, padx=(10, 0))

        # === Row 1: Heatmap ===
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
        ).grid(row=1, column=3, padx=(10, 0))

        # === Row 2: Root Nodes ===
        self.btn_root_nodes = tk.Button(
            self.frame,
            text="Show Root Nodes",
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
            command=lambda: self.show_help("Root Nodes", "Toggles visualization of root nodes in the workbook.")
        ).grid(row=2, column=3, padx=(10, 0))

        # === Row 3: Cascade Rename ===
        self.btn_cascade_rename = tk.Button(
            self.frame,
            text="Cascade Rename",
            width=25,
            height=1,
            state=tk.DISABLED,
            command=self.toggle_cascade_input
        )
        self.btn_cascade_rename.grid(row=3, column=0, sticky="w", pady=4)

        self.cascade_submit = tk.Button(
            self.frame,
            text="Submit",
            state=tk.DISABLED,
            command=self.submit_cascade_rename
        )
        self.cascade_submit.grid(row=3, column=1, padx=(5, 0), sticky="w")

        self.cascade_entry = tk.Entry(self.frame, width=20, state=tk.DISABLED)
        self.cascade_entry.grid(row=3, column=2, padx=(5, 0), sticky="w")
        self.cascade_entry.bind("<KeyRelease>", self.validate_cascade_input)

        tk.Button(
            self.frame,
            text="?",
            width=2,
            command=lambda: self.show_help("Cascade Rename", "Enter a new name to trigger cascade renaming.")
        ).grid(row=3, column=3, padx=(10, 0))

    def toggle_dependency_highlighting(self):
        try:
            if not self.app_state.is_active(Feature.DEPENDENCY_HIGHLIGHTING):
                self.feature_controller.start_dependency_highlighting()
                self.dependency_highlighting.config(bg="orange", text="Hide dependents/precedents")
                self.output.write("[Dependency Highlighting] Activated.")
            else:
                self.feature_controller.stop_dependency_highlighting()
                self.dependency_highlighting.config(bg="SystemButtonFace", text="Show dependents/precedents")
                self.output.write("[Dependency Highlighting] Deactivated.")
        except Exception as e:
            self.output.write(f"[ERROR] Dependency Highlighting toggle failed: {e}")

    def toggle_heatmap(self):
        try:
            if not self.app_state.is_active(Feature.DEPENDENTS_HEATMAP):
                self.feature_controller.show_heatmap()
                self.app_state.set_feature_active(Feature.DEPENDENTS_HEATMAP)
                self.btn_heatmap.config(bg="orange", text="Hide Heatmap")
                self.disable_all_except(self.btn_heatmap)
                self.output.write("[Heatmap] Activated.")
            else:
                self.feature_controller.hide_heatmap()
                self.app_state.set_feature_inactive(Feature.DEPENDENTS_HEATMAP)
                self.btn_heatmap.config(bg="SystemButtonFace", text="Show Heatmap")
                self.enable_all_buttons()
                self.output.write("[Heatmap] Deactivated.")
        except Exception as e:
            self.output.write(f"[ERROR] Heatmap toggle failed: {e}")

    def toggle_root_nodes(self):
        try:
            if not self.root_nodes_active:
                self.feature_controller.show_root_nodes()
                self.app_state.set_feature_active(Feature.ROOT_NODES)
                self.btn_root_nodes.config(bg="orange", text="Hide Root Nodes")
                self.disable_all_except(self.btn_root_nodes)
                self.output.write("[Root Nodes] Activated.")
                self.root_nodes_active = True
            else:
                self.feature_controller.hide_root_nodes()
                self.app_state.set_feature_inactive(Feature.ROOT_NODES)
                self.btn_root_nodes.config(bg="SystemButtonFace", text="Show Root Nodes")
                self.enable_all_buttons()
                self.output.write("[Root Nodes] Deactivated.")
                self.root_nodes_active = False
        except Exception as e:
            self.output.write(f"[ERROR] Root Nodes toggle failed: {e}")

    def toggle_cascade_input(self):
        if self.cascade_entry["state"] == tk.NORMAL:
            self.output.write("[Cascade Rename] Cancelled.")
            self.cascade_entry.delete(0, tk.END)
            self.cascade_entry.config(state=tk.DISABLED, bg="white")
            self.cascade_submit.config(state=tk.DISABLED)
        else:
            self.output.write("[Cascade Rename] Input activated.")
            self.cascade_entry.delete(0, tk.END)
            self.cascade_entry.config(state=tk.NORMAL, bg="white")
            self.cascade_submit.config(state=tk.DISABLED)

    def validate_cascade_input(self, event=None):
        value = self.cascade_entry.get().strip()
        if not value:
            self.cascade_entry.config(bg="white")
            self.cascade_submit.config(state=tk.DISABLED)
            return

        if self.is_valid_excel_name(value):
            self.cascade_entry.config(bg="#d9fcd9")  # light green
            self.cascade_submit.config(state=tk.NORMAL)
        else:
            self.cascade_entry.config(bg="#ffd6d6")  # light red
            self.cascade_submit.config(state=tk.DISABLED)

    def is_valid_excel_name(self, name: str) -> bool:
        return re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", name) is not None

    def submit_cascade_rename(self):
        try:
            new_name = self.cascade_entry.get().strip()
            if not new_name:
                self.output.write("[Cascade Rename] No name entered.")
                return

            if not self.is_valid_excel_name(new_name):
                self.output.write("[Cascade Rename] Invalid name. Only letters, numbers, and underscores are allowed. Name must start with a letter or underscore.")
                return

            self.feature_controller.start_cascade_rename(new_name)
            self.output.write(f"[Cascade Rename] Renamed to '{new_name}'.")
        except Exception as e:
            self.output.write(f"[ERROR] Cascade Rename failed: {e}")
        finally:
            self.cascade_entry.delete(0, tk.END)
            self.cascade_entry.config(state=tk.DISABLED, bg="white")
            self.cascade_submit.config(state=tk.DISABLED)

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
        self.dependency_highlighting.config(state=state)
        self.btn_heatmap.config(state=state)
        self.btn_root_nodes.config(state=state)
        self.btn_cascade_rename.config(state=state)

    def pack(self):
        self.frame.pack(fill="x", anchor="w")
