import tkinter as tk
from tkinter import messagebox
from model.feature import Feature
from view.widgets.base_function_widget import BaseFunctionWidget
from view.widgets.feature_button_texts import FeatureButtonTextManager


class RootNodesWidget(BaseFunctionWidget):
    def __init__(self, master, app_state, feature_controller, output, manager, **kwargs):
        super().__init__(master, app_state, feature_controller, output, **kwargs)

        self.feature = Feature.ROOT_NODES
        self.manager = manager

        self.button = self.create_button(
            text=FeatureButtonTextManager.get_text(self.feature, False),
            command=self.toggle,
            row=2,
            help_text="Displays cells with no precedents."
        )

        self.manager.register(self.feature, self)

    def toggle(self):
        self.toggle_feature(
            start_func=self.feature_controller.show_root_nodes,
            stop_func=self.feature_controller.hide_root_nodes
        )

    def enable(self):
        self.button.config(state=tk.NORMAL)

    def disable(self):
        self.button.config(state=tk.DISABLED)

    def set_active_state(self, active):
        self.button.config(text=FeatureButtonTextManager.get_text(self.feature, active))
