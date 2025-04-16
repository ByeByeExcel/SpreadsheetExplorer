from model.feature import Feature
from model.models.i_connected_workbook import IConnectedWorkbook
from model.services.functionality.one_time_painting.cell_to_color_converter.dependents_heatmap import DependentsHeatmap
from model.services.functionality.one_time_painting.cell_to_color_converter.root_node_highlighter import \
    RootNodeHighlighter
from model.services.functionality.one_time_painting.one_time_painting_executor import OneTimePaintingExecutor


class PaintingService:
    def __init__(self, app_state):
        self._app_state = app_state

    def show_heatmap(self, connected_workbook: IConnectedWorkbook) -> None:
        if not self._app_state.check_feature_startable(Feature.DEPENDENTS_HEATMAP):
            raise ValueError("Heatmap cannot be started.")
        self._app_state.set_feature_active(Feature.DEPENDENTS_HEATMAP)

        painter = OneTimePaintingExecutor(connected_workbook.get_all_cells(), DependentsHeatmap(connected_workbook))
        new_colors = painter.get_color_dict()
        initial_colors = self._app_state.connected_workbook.initial_to_grayscale_and_set_from_dict_and_return_initial_colors(
            new_colors)
        self._app_state.store_initial_colors(initial_colors)

    def show_root_nodes(self, connected_workbook: IConnectedWorkbook) -> None:
        if not self._app_state.check_feature_startable(Feature.ROOT_NODES):
            raise ValueError("Root nodes cannot be started.")
        self._app_state.set_feature_active(Feature.ROOT_NODES)

        painter = OneTimePaintingExecutor(connected_workbook.get_all_cells(), RootNodeHighlighter(connected_workbook))
        new_colors = painter.get_color_dict()

        initial_colors = self._app_state.connected_workbook.initial_to_grayscale_and_set_from_dict_and_return_initial_colors(
            new_colors)
        self._app_state.store_initial_colors(initial_colors)

    def stop_heatmap(self) -> None:
        self._reset_colors()
        self._app_state.set_feature_inactive(Feature.DEPENDENTS_HEATMAP)

    def stop_root_nodes(self) -> None:
        self._reset_colors()
        self._app_state.set_feature_inactive(Feature.ROOT_NODES)

    def _reset_colors(self) -> None:
        self._app_state.connected_workbook.set_colors_from_dict(self._app_state.initial_colors)
        self._app_state.initial_colors.clear()
