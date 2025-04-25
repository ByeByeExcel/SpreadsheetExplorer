from model.feature import Feature
from view.widgets.base_function_widget import BaseFunctionWidget


class HeatmapWidget(BaseFunctionWidget):
    def __init__(self, master, app_state, feature_controller, output, manager, **kwargs):
        super().__init__(master, app_state, feature_controller, output, **kwargs)
        self.feature = Feature.DEPENDENTS_HEATMAP

        self.button = self.initialize_feature_button(
            row=1,
            help_text="Visualize the density of formula usage with a color gradient."
        )

        self.set_toggle_function(
            self.feature_controller.show_heatmap,
            self.feature_controller.hide_heatmap
        )

        manager.register(self.feature, self)
