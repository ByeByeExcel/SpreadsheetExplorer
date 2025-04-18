import logging
import tkinter as tk
from tkinter import messagebox

from controller.feature_controller import FeatureController
from model.app_state import AppState
from model.feature import Feature


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
        self.output = output
        self.feature_controller = feature_controller
        self.app_state = app_state
        self.frame = tk.Frame(master, padx=20)

        if pack:
            self.pack()

        self.buttons: dict[Feature, tk.Button] = {}

        # === Row 0: Dependency Highlighting ===
        self.buttons[Feature.DEPENDENCY_HIGHLIGHTING] = self._create_feature_button(
            row=0,
            feature=Feature.DEPENDENCY_HIGHLIGHTING,
            command=self.toggle_dependency_highlighting,
            help_text="This function highlights dependents and precedents."
        )

        # === Row 1: Heatmap ===
        self.buttons[Feature.DEPENDENTS_HEATMAP] = self._create_feature_button(
            row=1,
            feature=Feature.DEPENDENTS_HEATMAP,
            command=self.toggle_heatmap,
            help_text="Toggles a heatmap view of the spreadsheet."
        )

        # === Row 2: Root Nodes ===
        self.buttons[Feature.ROOT_NODES] = self._create_feature_button(
            row=2,
            feature=Feature.ROOT_NODES,
            command=self.toggle_root_nodes,
            help_text="Displays cells with no precedents."
        )

        # === Row 3: Cascade Rename ===
        self.cascade_rename_input = tk.Entry(self.frame, width=20, state=tk.DISABLED)
        self.cascade_rename_submit = tk.Button(
            self.frame, text="Submit", width=10, state=tk.DISABLED, command=self._submit_cascade_rename
        )
        self.btn_cascade_rename = tk.Button(
            self.frame,
            text=FeatureButtonTextManager.get_text(Feature.CASCADE_RENAME, False),
            width=25,
            command=self._toggle_cascade_rename
        )
        self.btn_cascade_rename.grid(row=3, column=0, pady=6, sticky="w")
        self.cascade_rename_input.grid(row=3, column=1, padx=6)
        self.cascade_rename_submit.grid(row=3, column=2)
        tk.Button(
            self.frame, text="?", width=2,
            command=lambda: self.show_help("Cascade Rename", "Rename the selected cell and all its dependencies.")
        ).grid(row=3, column=3, padx=(10, 0))

        self.app_state.active_feature.add_observer(lambda new, old: self.update_buttons())
        self.app_state.is_connected_to_workbook.add_observer(lambda new, old: self.update_buttons())

        self.update_buttons()

    def pack(self):
        self.frame.pack(anchor="w", pady=10)

    def _create_feature_button(self, row, feature: Feature, command, help_text):
        btn = tk.Button(self.frame, text="", width=25, state=tk.DISABLED, command=command)
        btn.grid(row=row, column=0, sticky="w", pady=4)

        tk.Button(
            self.frame,
            text="?",
            width=2,
            command=lambda: self.show_help(feature.name, help_text)
        ).grid(row=row, column=3, padx=(10, 0))

        return btn

    def update_buttons(self):
        connected = self.app_state.is_connected_to_workbook.value
        active_feature = self.app_state.active_feature.value

        for feature, button in self.buttons.items():
            is_active = feature == active_feature
            if not connected:
                button.config(state=tk.DISABLED)
            elif active_feature is None or is_active:
                button.config(state=tk.NORMAL)
            else:
                button.config(state=tk.DISABLED)

            button.config(text=FeatureButtonTextManager.get_text(feature, is_active))

        can_rename = connected and active_feature is None
        self.btn_cascade_rename.config(state=tk.NORMAL if can_rename else tk.DISABLED)
        if not can_rename:
            self._reset_cascade_rename_ui()

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
            self.output.write(f"[ERROR] {str(e)}")

    def _toggle_cascade_rename(self):
        if self.cascade_rename_input["state"] == tk.DISABLED:
            self.cascade_rename_input.config(state=tk.NORMAL)
            self.cascade_rename_submit.config(state=tk.DISABLED)
            self.btn_cascade_rename.config(
                text=FeatureButtonTextManager.get_text(Feature.CASCADE_RENAME, True)
            )
            self.cascade_rename_input.delete(0, tk.END)
            selected = self.app_state.selected_cell.value
            if selected:
                address = getattr(selected, "address", str(selected))
                self.cascade_rename_input.insert(0, f"rename {address}".strip())
            self.cascade_rename_input.bind("<KeyRelease>", self._on_rename_text_change)
        else:
            self._reset_cascade_rename_ui()

    def _on_rename_text_change(self, event):
        value = self.cascade_rename_input.get().strip()
        self.cascade_rename_submit.config(state=tk.NORMAL if value else tk.DISABLED)

    def _submit_cascade_rename(self):
        rename_text = self.cascade_rename_input.get().strip()
        if rename_text:
            self.output.write(f"[Cascade Rename] Submitted: {rename_text}")
            self._reset_cascade_rename_ui()

    def _reset_cascade_rename_ui(self):
        self.cascade_rename_input.config(state=tk.DISABLED)
        self.cascade_rename_submit.config(state=tk.DISABLED)
        self.btn_cascade_rename.config(
            text=FeatureButtonTextManager.get_text(Feature.CASCADE_RENAME, False)
        )
        self.cascade_rename_input.unbind("<KeyRelease>")

    def show_help(self, title, text):
        messagebox.showinfo(title, text)
