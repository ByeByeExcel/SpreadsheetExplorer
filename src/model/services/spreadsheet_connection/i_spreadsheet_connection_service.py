from abc import ABC, abstractmethod

from model.domain_model.i_connected_workbook import IConnectedWorkbook


class ISpreadsheetConnectionService(ABC):
    @abstractmethod
    def get_open_workbooks(self):
        pass

    @abstractmethod
    def connect_to_workbook(self, filename: str) -> IConnectedWorkbook:
        pass
