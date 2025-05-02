from model.domain_model.feature import Feature
from model.services.app_state_service import AppStateService
from view.widgets.base_function_widget import BaseFunctionWidget


class FeatureButtonManager:
    def __init__(self, app_state: AppStateService):
        self.app_state = app_state
        self.widgets: dict[Feature, object] = {}
        self._updating = False

        self.app_state.active_feature.add_observer(lambda new, old: self.update_widgets())
        self.app_state.is_connected_to_workbook.add_observer(lambda new, old: self.update_widgets())
        self.app_state.is_analyzing.add_observer(lambda new, old: self.update_widgets())

    def register(self, feature: Feature, widget: BaseFunctionWidget):
        self.widgets[feature] = widget

    def update_widgets(self):
        if self._updating:
            return

        self._updating = True
        try:
            connected = self.app_state.is_connected_to_workbook.value
            active_feature = self.app_state.active_feature.value
            is_analyzing = self.app_state.is_analyzing.value

            for feature, widget in self.widgets.items():
                is_active = feature == active_feature

                if not connected or is_analyzing:
                    widget.disable()
                elif active_feature is None or is_active:
                    widget.enable()
                else:
                    widget.disable()

                widget.set_active_state(is_active)
        finally:
            self._updating = False
