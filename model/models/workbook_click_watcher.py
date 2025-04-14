import threading
import time

import xlwings

from model.models.spreadsheet.cell_address import CellAddress
from model.services.functionality.interactive_painting.selection_listener.i_selection_listener import ISelectionListener


class WorkbookClickWatcher:
    def __init__(self, connected_workbook):
        self.connected_workbook: xlwings.Book = connected_workbook
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._watch_loop, daemon=True)
        self._listener = None

    def start(self, listener: ISelectionListener):
        self._listener = listener
        self._thread.start()

    def stop(self):
        self._stop_event.set()
        self._thread.join()

    def _watch_loop(self):
        previous_selection = None

        while not self._stop_event.is_set():
            time.sleep(0.5)
            try:
                new_selection = self.connected_workbook.selection
            except Exception as e:
                print(f"Error getting selection: {e}")
                break

            new_cell_address = get_cell_address_from_xlwings(new_selection)

            if new_cell_address != previous_selection and new_cell_address.workbook == self.connected_workbook.name.lower():
                if self._listener:
                    self._listener(previous_selection, new_cell_address)

                previous_selection = new_cell_address

        if self._listener:
            self._listener(previous_selection, None)


def get_cell_address_from_xlwings(cell: xlwings.Range) -> CellAddress:
    return CellAddress(cell.sheet.book.name, cell.sheet.name, cell.address)
