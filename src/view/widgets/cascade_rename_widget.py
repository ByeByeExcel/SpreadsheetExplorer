import re
import tkinter as tk
from tkinter import messagebox

from model.domain_model.feature import Feature
from view.widgets.base_function_widget import BaseFunctionWidget

VALID_NAME_REGEX = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
CELL_REF_REGEX = re.compile(r"^[A-Za-z]{1,3}[0-9]{1,7}$")


class CascadeRenameWidget(BaseFunctionWidget):
    def __init__(self, master, app_state, feature_controller, output, manager, **kwargs):
        super().__init__(master, app_state, feature_controller, output, **kwargs)

        self.feature = Feature.CASCADE_RENAME
        self.manager = manager
        self._toggling = False

        self.button = self.initialize_feature_button(row=3)

        self.rename_input = tk.Entry(self, width=25, state=tk.DISABLED)
        self.rename_input.grid(row=4, column=1, padx=10, sticky="ew")
        self.rename_input.bind("<KeyRelease>", self._on_text_change)

        self.submit_button = tk.Button(self, text="Submit new name", width=25, state=tk.DISABLED, command=self._submit)
        self.submit_button.grid(row=5, column=1, padx=10, sticky="ew")

        self.manager.register(self.feature, self)

    def toggle(self):
        try:
            if self.app_state.is_feature_active(self.feature):
                self.feature_controller.deactivate_cascade_rename()
                self.log(f"[INFO] Stopped feature: {self.feature.name}")
            else:
                if not self.app_state.can_start_feature():
                    raise ValueError("Cannot start feature — another is active or workbook not connected.")
                self.feature_controller.activate_cascade_rename()
                self.log(f"[INFO] Started feature: {self.feature.name}")
        except Exception as e:
            self._handle_error("Cascade Rename toggle failed", e)

    def _submit(self):
        try:
            new_name = self.rename_input.get().strip()
            if not new_name:
                raise ValueError("Name cannot be empty.")
            if not (VALID_NAME_REGEX.fullmatch(new_name) and not CELL_REF_REGEX.fullmatch(new_name)):
                raise ValueError("Invalid name. Use only valid identifiers, not Excel cell references.")

            self.feature_controller.cascade_rename(new_name)
            self.log(f"[INFO] Cascade renaming to '{new_name}'")

            self.after(1, self._cleanup_after_rename)
        except ValueError as e:
            self._handle_error("Rename submission failed", e)

    def _cleanup_after_rename(self):
        self.feature_controller.deactivate_cascade_rename()
        self.app_state.set_feature_inactive(self.feature)
        self.rename_input.delete(0, tk.END)
        self.rename_input.config(state=tk.DISABLED, bg="SystemButtonFace")
        self.submit_button.config(state=tk.DISABLED)
        self.log("[INFO] Deactivating Cascade Rename after rename")

    def _on_text_change(self, _):
        text = self.rename_input.get().strip()
        valid = VALID_NAME_REGEX.fullmatch(text) and not CELL_REF_REGEX.fullmatch(text)

        color = "#d0ffd0" if valid else "#ffd0d0"
        state = tk.NORMAL if valid else tk.DISABLED

        self.rename_input.config(bg=color)
        self.submit_button.config(state=state)

    def set_active_state(self, active):
        super().set_active_state(active)
        self.rename_input.config(state=tk.NORMAL if active else tk.DISABLED)
        if active:
            self._on_text_change(None)
        else:
            self.rename_input.delete(0, tk.END)
            self.rename_input.config(bg="SystemButtonFace")
            self.submit_button.config(state=tk.DISABLED)

    def _handle_error(self, context, error):
        error_msg = f"[ERROR] {context}: {error}"
        self.log(error_msg)
        messagebox.showerror(context, str(error))
