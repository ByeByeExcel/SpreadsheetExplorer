from model.models.i_connected_workbook import IConnectedWorkbook
from model.services.functionality.one_time_painting.cell_to_color_converter.dependents_heatmap import DependentsHeatmap
from model.services.functionality.one_time_painting.one_time_painting_executor import OneTimePaintingExecutor


class PaintingService:
    _one_time_painters: [OneTimePaintingExecutor] = []

    def show_heatmap(self, connected_workbook: IConnectedWorkbook) -> None:
        painter = OneTimePaintingExecutor(connected_workbook,
                                          connected_workbook.get_all_cells(),
                                          DependentsHeatmap(connected_workbook))
        self._one_time_painters.append(painter)
        painter.paint()

    def reset_all_painters(self) -> None:
        for painter in self._one_time_painters:
            painter.reset()
        self._one_time_painters.clear()
