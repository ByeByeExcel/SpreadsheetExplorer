from typing import Callable, Optional

from model.domain_model.spreadsheet.i_connected_workbook import IConnectedWorkbook
from model.domain_model.spreadsheet.range_reference import RangeReference


class SelectionMonitoring:
    _POLL_INTERVAL_MS = 100  # 0.1s

    def __init__(self, tk_root, connected_workbook: IConnectedWorkbook,
                 on_selection_change: Callable[[Optional[RangeReference]], None]):
        self._root = tk_root
        self._connected_workbook = connected_workbook
        self._on_selection_change = on_selection_change
        self._last_selection = None
        self._active = False
        self._after_id = None

    def start(self):
        if not self._active:
            self._active = True
            self._poll_selection()

    def stop(self):
        self._active = False
        if self._after_id:
            self._root.after_cancel(self._after_id)
            self._after_id = None
        if self._on_selection_change:
            self._on_selection_change(None)

    def _poll_selection(self):
        try:
            new_selection = self._connected_workbook.get_selected_range_ref()
            if (new_selection != self._last_selection and
                    new_selection.workbook.lower() == self._connected_workbook.name.lower()):
                self._last_selection = new_selection
                if self._on_selection_change:
                    self._on_selection_change(new_selection)
        except Exception as e:
            if '0x800ac472' in str(e):
                # Excel is busy
                pass
            else:
                print(f"[WorkbookClickWatcher] Error getting selection: {e}")
                self.stop()
                raise e

        if self._active:
            self._after_id = self._root.after(self._POLL_INTERVAL_MS, self._poll_selection)
