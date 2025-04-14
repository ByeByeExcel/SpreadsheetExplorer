import threading
import time
from typing import Callable, Optional

from model.models.i_connected_workbook import IConnectedWorkbook
from model.models.spreadsheet.cell_address import CellAddress


class WorkbookClickWatcher:
    _POLL_INTERVAL_SECONDS = 0.1

    def __init__(self, connected_workbook, listener: Callable[[Optional[CellAddress]], None]):
        self.connected_workbook: IConnectedWorkbook = connected_workbook
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._watch_loop, daemon=True)
        self._listener = listener

    def start(self):
        self._thread.start()

    def stop(self):
        self._stop_event.set()
        self._thread.join()

    def _watch_loop(self):
        previous_selection = None

        while not self._stop_event.is_set():
            time.sleep(self._POLL_INTERVAL_SECONDS)
            try:
                new_cell_address = self.connected_workbook.get_selected_cell()
            except Exception as e:
                print(f"Error getting selection: {e}")
                break

            if new_cell_address != previous_selection and new_cell_address.workbook == self.connected_workbook.name.lower():
                if self._listener:
                    self._listener(new_cell_address)

                previous_selection = new_cell_address

        if self._listener:
            self._listener(None)
