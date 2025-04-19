from abc import abstractmethod, ABC
from typing import Optional

from model.models.spreadsheet.cell_address import CellAddress


class ISelectionObserver(ABC):
    @abstractmethod
    def __call__(self, new_cell: Optional[CellAddress], old_cell: Optional[CellAddress]) -> None:
        pass

    @abstractmethod
    def stop(self) -> None:
        pass

    @abstractmethod
    def initialize(self, initial_value: CellAddress) -> None:
        pass
