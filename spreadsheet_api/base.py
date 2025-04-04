from abc import ABC, abstractmethod


class SpreadsheetInterface(ABC):
    @abstractmethod
    def get_value(self, cell: str):
        pass

    @abstractmethod
    def set_value(self, cell: str, value):
        pass

    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def close(self):
        pass
