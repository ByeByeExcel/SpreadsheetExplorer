from model.feature import Feature
from model.models.i_connected_workbook import IConnectedWorkbook
from model.services.functionality.one_time_painting.cell_to_color_converter.dependents_heatmap import DependentsHeatmap
from model.services.functionality.one_time_painting.cell_to_color_converter.root_node_highlighter import \
    RootNodeHighlighter
from model.services.functionality.one_time_painting.one_time_painting_executor import OneTimePaintingExecutor


class PaintingService:
    def __init__(self, app_state):
        self._app_state = app_state
        self._one_time_painters: dict[Feature, OneTimePaintingExecutor] = {}

    def show_heatmap(self, connected_workbook: IConnectedWorkbook) -> None:
        if not self._app_state.check_feature_startable(Feature.DEPENDENCY_HIGHLIGHTING):
            raise ValueError("Heatmap cannot be started.")
        self._app_state.set_feature_active(Feature.DEPENDENTS_HEATMAP)

        initial_colors = self._app_state.connected_workbook.grayscale_colors_and_return_initial_colors()
        self._app_state.store_initial_colors(initial_colors)

        painter = OneTimePaintingExecutor(connected_workbook,
                                          connected_workbook.get_all_cells(),
                                          DependentsHeatmap(connected_workbook))
        self._one_time_painters[Feature.DEPENDENTS_HEATMAP] = painter
        painter.paint()

    def show_root_nodes(self, connected_workbook: IConnectedWorkbook) -> None:
        if not self._app_state.check_feature_startable(Feature.DEPENDENCY_HIGHLIGHTING):
            raise ValueError("Root nodes cannot be started.")
        initial_colors = self._app_state.connected_workbook.grayscale_colors_and_return_initial_colors()
        self._app_state.store_initial_colors(initial_colors)

        painter = OneTimePaintingExecutor(connected_workbook,
                                          connected_workbook.get_all_cells(),
                                          RootNodeHighlighter(connected_workbook))
        self._one_time_painters[Feature.ROOT_NODES] = painter
        painter.paint()

    def stop_heatmap(self) -> None:
        self.stop_feature(Feature.DEPENDENTS_HEATMAP)
        self._app_state.connected_workbook.set_colors_from_dict(self._app_state.initial_colors)
        self._app_state.initial_colors.clear()
        self._app_state.set_feature_inactive(Feature.DEPENDENTS_HEATMAP)

    def stop_root_nodes(self) -> None:
        self.stop_feature(Feature.ROOT_NODES)
        self._app_state.connected_workbook.set_colors_from_dict(self._app_state.initial_colors)
        self._app_state.initial_colors.clear()
        self._app_state.set_feature_inactive(Feature.ROOT_NODES)

    def stop_all(self) -> None:
        for feature in self._one_time_painters.keys():
            self.stop_feature(feature)

    def stop_feature(self, feature: Feature) -> None:
        painter = self._one_time_painters.pop(feature, None)
        if painter:
            painter.reset()
