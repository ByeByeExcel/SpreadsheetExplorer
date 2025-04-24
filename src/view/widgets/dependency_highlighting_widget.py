import tkinter as tk
from model.feature import Feature
from view.widgets.base_function_widget import BaseFunctionWidget

class DependencyHighlightingWidget(BaseFunctionWidget):
    def __init__(self, master, app_state, feature_controller, output, manager, **kwargs):
        super().__init__(master, app_state, feature_controller, output, **kwargs)
        self.feature = Feature.DEPENDENCY_HIGHLIGHTING

        self.highlight_button = self.initialize_feature_button(
            row=2,
            help_text="Highlight all the cells that directly or indirectly influence the selected cell."
        )

        self.set_toggle_function(
            self.feature_controller.start_dependency_highlighting,
            self.feature_controller.stop_dependency_highlighting
        )

        manager.register(self.feature, self)

    def enable(self):
        self.highlight_button.config(state=tk.NORMAL)

    def disable(self):
        self.highlight_button.config(state=tk.DISABLED)

    def set_active_state(self, active):
        from view.widgets.feature_button_texts import FeatureButtonTextManager
        self.highlight_button.config(text=FeatureButtonTextManager.get_text(self.feature, active))
