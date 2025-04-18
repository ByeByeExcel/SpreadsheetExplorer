from abc import abstractmethod, ABC

from src.model.models.spreadsheet.cell_address import CellAddress


class ISelectionObserver(ABC):
    @abstractmethod
    def __call__(self, old_cell: CellAddress, new_cell: CellAddress) -> None:
        pass
