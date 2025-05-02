from abc import abstractmethod, ABC
from typing import Optional

from model.domain_model.spreadsheet.range_reference import RangeReference


class ISelectionObserver(ABC):
    @abstractmethod
    def __call__(self, new_range_ref: Optional[RangeReference], old_range_ref: Optional[RangeReference]) -> None:
        pass

    @abstractmethod
    def stop(self) -> None:
        pass

    @abstractmethod
    def initialize(self, initial_range_ref: RangeReference) -> None:
        pass
