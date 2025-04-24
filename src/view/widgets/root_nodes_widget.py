import tkinter as tk
from model.feature import Feature
from view.widgets.base_function_widget import BaseFunctionWidget

class RootNodesWidget(BaseFunctionWidget):
    def __init__(self, master, app_state, feature_controller, output, manager, **kwargs):
        super().__init__(master, app_state, feature_controller, output, **kwargs)
        self.feature = Feature.ROOT_NODES

        self.root_nodes_button = self.initialize_feature_button(
            row=5,
            help_text="Highlight the cells that are not referenced by any other cells."
        )

        self.set_toggle_function(
            self.feature_controller.show_root_nodes,
            self.feature_controller.hide_root_nodes
        )

        manager.register(self.feature, self)

    def enable(self):
        self.root_nodes_button.config(state=tk.NORMAL)

    def disable(self):
        self.root_nodes_button.config(state=tk.DISABLED)

    def set_active_state(self, active):
        from view.widgets.feature_button_texts import FeatureButtonTextManager
        self.root_nodes_button.config(text=FeatureButtonTextManager.get_text(self.feature, active))
