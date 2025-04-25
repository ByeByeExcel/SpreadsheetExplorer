from typing import Callable, Optional

from model.models.i_connected_workbook import IConnectedWorkbook
from model.models.spreadsheet.cell_address import CellAddress


class WorkbookClickWatcher:
    _POLL_INTERVAL_MS = 100  # 0.1s

    def __init__(self, tk_root, connected_workbook: IConnectedWorkbook,
                 listener: Callable[[Optional[CellAddress]], None]):
        self.root = tk_root
        self.connected_workbook = connected_workbook
        self.listener = listener
        self.previous_selection = None
        self._after_id = None
        self._active = False

    def _poll_selection(self):
        try:
            new_cell_address = self.connected_workbook.get_selected_cell()
            if (new_cell_address != self.previous_selection and
                    new_cell_address.workbook.lower() == self.connected_workbook.name.lower()):
                self.previous_selection = new_cell_address
                if self.listener:
                    self.listener(new_cell_address)
        except Exception as e:
            if '0x800ac472' in str(e):
                # Excel is busy
                pass
            else:
                print(f"[WorkbookClickWatcher] Error getting selection: {e}")
                self.stop()
                return

        if self._active:
            self._after_id = self.root.after(self._POLL_INTERVAL_MS, self._poll_selection)

    def start(self):
        if not self._active:
            self._active = True
            self._poll_selection()

    def stop(self):
        self._active = False
        if self._after_id:
            self.root.after_cancel(self._after_id)
            self._after_id = None
        if self.listener:
            self.listener(None)
