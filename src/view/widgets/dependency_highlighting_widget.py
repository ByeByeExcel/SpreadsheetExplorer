from model.feature import Feature
from view.widgets.base_function_widget import BaseFunctionWidget


class DependencyHighlightingWidget(BaseFunctionWidget):
    def __init__(self, master, app_state, feature_controller, output, manager, **kwargs):
        super().__init__(master, app_state, feature_controller, output, **kwargs)
        self.feature = Feature.DEPENDENCY_HIGHLIGHTING

        self.button = self.initialize_feature_button(row=2)

        self.set_toggle_function(
            self.feature_controller.start_dependency_highlighting,
            self.feature_controller.stop_dependency_highlighting
        )

        manager.register(self.feature, self)
