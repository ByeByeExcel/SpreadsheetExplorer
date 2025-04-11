from abc import abstractmethod, ABC

from model.models.spreadsheet.cell_address import CellAddress


class ISelectionListener(ABC):
    @abstractmethod
    def __call__(self, old_cell: CellAddress, new_cell: CellAddress) -> None:
        pass
