from model.feature import Feature
from view.widgets.base_function_widget import BaseFunctionWidget


class RootNodesWidget(BaseFunctionWidget):
    def __init__(self, master, app_state, feature_controller, output, manager, **kwargs):
        super().__init__(master, app_state, feature_controller, output, **kwargs)
        self.feature = Feature.ROOT_NODES

        self.button = self.initialize_feature_button(row=5)

        self.set_toggle_function(
            self.feature_controller.show_root_nodes,
            self.feature_controller.hide_root_nodes
        )

        manager.register(self.feature, self)
