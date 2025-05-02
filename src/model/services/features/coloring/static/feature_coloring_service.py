from typing import Type

from model.domain_model.feature import Feature
from model.domain_model.spreadsheet.cell_range import CellRange
from model.domain_model.spreadsheet.i_connected_workbook import IConnectedWorkbook
from model.domain_model.spreadsheet.range_reference import RangeReference
from model.services.app_state_service import AppStateService
from model.services.features.coloring.static.color_strategies.dependents_heatmap import \
    DependentsHeatmap
from model.services.features.coloring.static.color_strategies.i_range_color_strategy import IRangeColorStrategy
from model.services.features.coloring.static.color_strategies.root_node_coloring import \
    RootNodeColoring

FEATURE_TO_COLOR_STRATEGY: dict[Feature, Type[IRangeColorStrategy]] = {
    Feature.DEPENDENTS_HEATMAP: DependentsHeatmap,
    Feature.ROOT_NODES: RootNodeColoring,
}


class FeatureColoringService:
    def __init__(self, app_state: AppStateService):
        self._app_state = app_state

    def show_feature_coloring(self, feature: Feature) -> None:
        if not self._app_state.can_start_feature():
            raise ValueError(f"{feature.name} cannot be started.")
        self._app_state.set_feature_active(feature)

        connected_workbook: IConnectedWorkbook = self._app_state.get_connected_workbook()

        strategy_cls = FEATURE_TO_COLOR_STRATEGY.get(feature)
        if not strategy_cls:
            raise ValueError(f"No strategy registered for feature: {feature}")

        strategy = strategy_cls(connected_workbook)
        ranges = connected_workbook.get_all_cell_ranges()

        new_colors = self._apply_color_strategy_to_range(ranges, strategy)

        initial_colors = (
            self._app_state.get_connected_workbook()
            .initial_to_grayscale_and_set_from_dict_and_return_initial_colors(new_colors)
        )
        self._app_state.store_initial_colors(initial_colors)

    def stop_feature_coloring(self, feature: Feature) -> None:
        self._reset_colors()
        self._app_state.set_feature_inactive(feature)

    def _reset_colors(self) -> None:
        self._app_state.get_connected_workbook().set_colors_from_dict(self._app_state.get_initial_colors())
        self._app_state.clear_initial_colors()

    @staticmethod
    def _apply_color_strategy_to_range(cell_ranges: set[CellRange], color_strategy: IRangeColorStrategy) \
            -> dict[RangeReference, str]:
        color_dict: dict[RangeReference, str] = {}
        for cell_range in cell_ranges:
            color = color_strategy.convert(cell_range)
            if color is not None:
                color_dict[cell_range.reference] = color
        return color_dict
