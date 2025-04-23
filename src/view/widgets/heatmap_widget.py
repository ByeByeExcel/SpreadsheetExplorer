import tkinter as tk
from model.feature import Feature
from view.widgets.base_function_widget import BaseFunctionWidget
from view.widgets.feature_button_texts import FeatureButtonTextManager


class HeatmapWidget(BaseFunctionWidget):
    def __init__(self, master, app_state, feature_controller, output, manager, **kwargs):
        super().__init__(master, app_state, feature_controller, output, **kwargs)

        self.feature = Feature.DEPENDENTS_HEATMAP
        self.manager = manager
        self._toggling = False

        self.button = self.create_button(
            text=FeatureButtonTextManager.get_text(self.feature, False),
            command=self.toggle,
            row=1,
            help_text="Toggles a heatmap view of the spreadsheet."
        )

        self.manager.register(self.feature, self)

    def toggle(self):
        self.toggle_feature(
            start_func=self.feature_controller.show_heatmap,
            stop_func=self.feature_controller.hide_heatmap
        )

    def enable(self):
        self.button.config(state=tk.NORMAL)

    def disable(self):
        self.button.config(state=tk.DISABLED)

    def set_active_state(self, active):
        self.button.config(text=FeatureButtonTextManager.get_text(self.feature, active))
