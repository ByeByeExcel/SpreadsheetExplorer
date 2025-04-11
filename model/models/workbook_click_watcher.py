import threading
import time

import xlwings

from model.models.spreadsheet.cell_address import CellAddress
from model.services.functionality.i_selection_listener import ISelectionListener


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
            new_selection = get_cell_address_from_xlwings(self.connected_workbook.selection)

            if new_selection != previous_selection and new_selection.workbook == self.connected_workbook.name:
                if self._listener:
                    self._listener(previous_selection, new_selection)

                previous_selection = new_selection

        self._listener(previous_selection, None)


def get_cell_address_from_xlwings(cell: xlwings.Range) -> CellAddress:
    return CellAddress(cell.sheet.book.name, cell.sheet.name, cell.address)
