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

        self.root_nodes_active = False

        # === Dependency Highlighting ===
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

        # === Root Nodes Toggle Button ===
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
        ).grid(row=2, column=1)

        # === Cascade Renaming Button ===
        self.btn_cascade_rename = tk.Button(
            self.frame,
            text="Cascade Rename",
            width=25,
            height=1,
            state=tk.DISABLED,
            command=self.toggle_cascade_input
        )
        self.btn_cascade_rename.grid(row=3, column=0, sticky="w", pady=4)

        tk.Button(
            self.frame,
            text="?",
            width=2,
            command=lambda: self.show_help("Cascade Rename", "Enter a new name to trigger cascade renaming.")
        ).grid(row=3, column=1)

        # === Cascade Rename Input Field ===
        self.cascade_input_frame = tk.Frame(self.frame)
        self.cascade_entry = tk.Entry(self.cascade_input_frame, width=20)
        self.cascade_submit = tk.Button(self.cascade_input_frame, text="Submit", command=self.submit_cascade_rename)

        self.cascade_entry.grid(row=0, column=0, padx=(0, 5))
        self.cascade_submit.grid(row=0, column=1)
        self.cascade_input_frame.grid(row=4, column=0, columnspan=2, pady=(0, 8))
        self.cascade_input_frame.grid_remove()  # hidden by default

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
                self.btn_heatmap.config(bg="orange", text="Hide Heatmap")
                self.output.write("[Heatmap] Activated.")
            else:
                self.feature_controller.hide_heatmap()
                self.btn_heatmap.config(bg="SystemButtonFace", text="Show Heatmap")
                self.output.write("[Heatmap] Deactivated.")
        except Exception as e:
            self.output.write(f"[ERROR] Heatmap toggle failed: {e}")

    def toggle_root_nodes(self):
        try:
            if not self.root_nodes_active:
                self.feature_controller.show_root_nodes()
                self.btn_root_nodes.config(bg="orange", text="Hide Root Nodes")
                self.output.write("[Root Nodes] Activated.")
                self.root_nodes_active = True
            else:
                self.feature_controller.hide_root_nodes()
                self.btn_root_nodes.config(bg="SystemButtonFace", text="Show Root Nodes")
                self.output.write("[Root Nodes] Deactivated.")
                self.root_nodes_active = False
        except Exception as e:
            self.output.write(f"[ERROR] Root Nodes toggle failed: {e}")

    def toggle_cascade_input(self):
        if self.cascade_input_frame.winfo_ismapped():
            self.cascade_input_frame.grid_remove()
        else:
            self.cascade_entry.delete(0, tk.END)
            self.cascade_input_frame.grid()

    def submit_cascade_rename(self):
        try:
            new_name = self.cascade_entry.get()
            if new_name.strip():
                self.feature_controller.start_cascade_rename(new_name.strip())
                self.output.write(f"[Cascade Rename] Renamed to '{new_name.strip()}'.")
            else:
                self.output.write("[Cascade Rename] No name entered.")
        except Exception as e:
            self.output.write(f"[ERROR] Cascade Rename failed: {e}")
        finally:
            self.cascade_input_frame.grid_remove()

    def show_help(self, title, description):
        messagebox.showinfo(title, description)

    def set_buttons_state(self, state):
        self.dependency_highlighting.config(state=state)
        self.btn_heatmap.config(state=state)
        self.btn_root_nodes.config(state=state)
        self.btn_cascade_rename.config(state=state)

    def pack(self):
        self.frame.pack(fill="x", anchor="w")
