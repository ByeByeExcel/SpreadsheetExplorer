from abc import abstractmethod, ABC

from model.models.spreadsheet.cell_address import CellAddress


class ISelectionObserver(ABC):
    @abstractmethod
    def __call__(self, old_cell: CellAddress, new_cell: CellAddress) -> None:
        pass

    @abstractmethod
    def stop(self) -> None:
        pass

    @abstractmethod
    def initialize(self, initial_value: CellAddress) -> None:
        pass
