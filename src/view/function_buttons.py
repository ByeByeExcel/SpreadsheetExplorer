import logging
import re
import sys
import tkinter as tk
from tkinter import messagebox

from controller.feature_controller import FeatureController
from model.app_state import AppState
from model.feature import Feature

VALID_NAME_REGEX = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
CELL_REF_REGEX = re.compile(r"^[A-Za-z]{1,3}[0-9]{1,7}$")


class FeatureButtonTextManager:
    BUTTON_TEXTS = {
        Feature.DEPENDENCY_HIGHLIGHTING: ("Show dependents/precedents", "Hide dependents/precedents"),
        Feature.DEPENDENTS_HEATMAP: ("Show Heatmap", "Hide Heatmap"),
        Feature.ROOT_NODES: ("Show Root Nodes", "Hide Root Nodes"),
        Feature.CASCADE_RENAME: ("Cascade Rename", "Cancel Renaming"),
    }

    @classmethod
    def get_text(cls, feature: Feature, active: bool) -> str:
        return cls.BUTTON_TEXTS.get(feature, ("Show", "Hide"))[1 if active else 0]


class FunctionButtonSection:
    def __init__(self, master, output, feature_controller: FeatureController, app_state: AppState, pack=True):
        self.output = output if output else sys.stdout
        self.feature_controller = feature_controller
        self.app_state = app_state
        self.frame = tk.Frame(master, padx=20)
        self.frame.grid_columnconfigure(1, weight=1)

        if pack:
            self.pack()

        self.buttons: dict[Feature, tk.Button] = {}

        # Dependency Highlighting
        self.buttons[Feature.DEPENDENCY_HIGHLIGHTING] = self._create_feature_button(
            row=0,
            feature=Feature.DEPENDENCY_HIGHLIGHTING,
            command=self.toggle_dependency_highlighting,
            help_text="This function highlights dependents and precedents."
        )

        # Heatmap
        self.buttons[Feature.DEPENDENTS_HEATMAP] = self._create_feature_button(
            row=1,
            feature=Feature.DEPENDENTS_HEATMAP,
            command=self.toggle_heatmap,
            help_text="Toggles a heatmap view of the spreadsheet."
        )

        # Root Nodes
        self.buttons[Feature.ROOT_NODES] = self._create_feature_button(
            row=2,
            feature=Feature.ROOT_NODES,
            command=self.toggle_root_nodes,
            help_text="Displays cells with no precedents."
        )

        # Cascade Rename
        self.btn_cascade_rename = self._create_feature_button(
            row=3,
            feature=Feature.CASCADE_RENAME,
            command=self._toggle_cascade_rename,
            help_text="Rename the selected cell and all its dependencies."
        )
        self.buttons[Feature.CASCADE_RENAME] = self.btn_cascade_rename

        # Input & submit under cascade rename
        self.cascade_rename_input = tk.Entry(self.frame, width=25, state=tk.DISABLED)
        self.cascade_rename_input.grid(row=4, column=1, padx=10, pady=(0, 0), sticky="ew")
        self.cascade_rename_input.bind("<KeyRelease>", self._on_rename_text_change)

        self.cascade_rename_submit = tk.Button(self.frame, text="Submit", width=25, state=tk.DISABLED,
                                               command=self._submit_cascade_rename)
        self.cascade_rename_submit.grid(row=5, column=1, sticky="ew")

        self.app_state.active_feature.add_observer(lambda new, old: self.update_buttons())
        self.app_state.is_connected_to_workbook.add_observer(lambda new, old: self.update_buttons())
        self.app_state.is_analyzing.add_observer(lambda new, old: self.update_buttons())

        self.update_buttons()

    def pack(self):
        self.frame.pack(anchor="w", pady=10)

    def _create_feature_button(self, row, feature: Feature, command, help_text):
        help_button = tk.Button(self.frame, text="?", width=2, command=lambda: self.show_help(feature.name, help_text))
        help_button.grid(row=row, column=0, padx=(0, 5), sticky="w")

        btn = tk.Button(self.frame, text="", width=25, state=tk.DISABLED, command=command)
        btn.grid(row=row, column=1, sticky="w", pady=4)

        return btn

    def update_buttons(self):
        connected = self.app_state.is_connected_to_workbook.value
        active_feature = self.app_state.active_feature.value
        is_analyzing = self.app_state.is_analyzing.value

        for feature, button in self.buttons.items():
            is_active = feature == active_feature
            if not connected or is_analyzing:
                button.config(state=tk.DISABLED)
            elif active_feature is None or is_active:
                button.config(state=tk.NORMAL)
            else:
                button.config(state=tk.DISABLED)

            button.config(text=FeatureButtonTextManager.get_text(feature, is_active))

        self._update_cascade_rename_ui()

    def toggle_dependency_highlighting(self):
        self._toggle_feature(
            Feature.DEPENDENCY_HIGHLIGHTING,
            self.feature_controller.start_dependency_highlighting,
            self.feature_controller.stop_dependency_highlighting
        )

    def toggle_heatmap(self):
        self._toggle_feature(
            Feature.DEPENDENTS_HEATMAP,
            self.feature_controller.show_heatmap,
            self.feature_controller.hide_heatmap
        )

    def toggle_root_nodes(self):
        self._toggle_feature(
            Feature.ROOT_NODES,
            self.feature_controller.show_root_nodes,
            self.feature_controller.hide_root_nodes
        )

    def _toggle_feature(self, feature: Feature, start_func, stop_func):
        try:
            if self.app_state.is_feature_active(feature):
                stop_func()
            else:
                start_func()
        except ValueError as e:
            logging.error(str(e))
            if self.output:
                self.output.write(f"[ERROR] {str(e)}")

    def _toggle_cascade_rename(self):
        if self.app_state.is_feature_active(Feature.CASCADE_RENAME):
            self.feature_controller.stop_cascade_rename()
        else:
            logging.debug("Cascade rename button clicked: activating mode")
            self.feature_controller.start_cascade_rename()

    def _on_rename_text_change(self, _):
        value = self.cascade_rename_input.get().strip()
        is_valid = bool(VALID_NAME_REGEX.match(value)) and not CELL_REF_REGEX.match(value)

        if is_valid:
            self.cascade_rename_input.config(bg="#d0ffd0")
            self.cascade_rename_submit.config(state=tk.NORMAL)
        else:
            self.cascade_rename_input.config(bg="#ffd0d0")
            self.cascade_rename_submit.config(state=tk.DISABLED)

    def _submit_cascade_rename(self):
        rename_text = self.cascade_rename_input.get().strip()
        selected = self.app_state.selected_cell.value

        if not self.app_state.is_feature_active(Feature.CASCADE_RENAME):
            self.output.write("[ERROR] Rename failed: Cascade rename mode is not active.")
            return

        if not selected:
            self.output.write("[ERROR] No cell selected for renaming.")
            return

        if not rename_text:
            self.output.write("[ERROR] Rename input is empty.")
            return

        if not VALID_NAME_REGEX.match(rename_text) or CELL_REF_REGEX.match(rename_text):
            if self.output:
                self.output.write(
                    "[ERROR] Invalid name format. Use only letters, digits, or underscores, and do not start with a digit or use Excel cell references.")
            return

        try:
            self.feature_controller.cascade_rename(rename_text)
            if self.output:
                self.output.write(f"[Cascade Rename] Submitted: {selected.address} → {rename_text}")
        except ValueError as e:
            if self.output:
                self.output.write(f"[ERROR] Rename failed: {str(e)}")

    def _update_cascade_rename_ui(self):
        if self.app_state.is_feature_active(Feature.CASCADE_RENAME):
            self.cascade_rename_input.config(state=tk.NORMAL, bg="white")
            self.cascade_rename_submit.config(state=tk.NORMAL)
        else:
            self.cascade_rename_input.delete(0, tk.END)
            self.cascade_rename_input.config(state=tk.DISABLED, bg="SystemButtonFace")
            self.cascade_rename_submit.config(state=tk.DISABLED)

    def show_help(self, title, text):
        messagebox.showinfo(title, text)
