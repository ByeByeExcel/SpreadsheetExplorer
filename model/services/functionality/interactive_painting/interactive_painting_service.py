from model.models.i_connected_workbook import IConnectedWorkbook
from model.models.workbook_click_watcher import WorkbookClickWatcher
from model.services.functionality.interactive_painting.selection_listener.highlight_precedent_dependent_listener import \
    HighlightCellSelectionListener


class InteractivePaintingService:
    _workbook_click_watchers: [WorkbookClickWatcher] = []

    def highlight_dependents_precedents(self, connected_workbook: IConnectedWorkbook) -> None:
        listener = HighlightCellSelectionListener(connected_workbook)
        watcher = WorkbookClickWatcher(connected_workbook)
        self._workbook_click_watchers.append(watcher)
        watcher.start(listener)

    def stop_all_watchers(self) -> None:
        for watcher in self._workbook_click_watchers:
            watcher.stop()
        self._workbook_click_watchers = []
