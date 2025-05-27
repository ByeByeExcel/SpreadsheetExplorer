from abc import ABC, abstractmethod
from typing import Iterable, Optional

from model.domain_model.spreadsheet.range_reference import RangeReference
from model.domain_model.spreadsheet.workbook import Workbook


class IConnectedWorkbook(ABC, Workbook):

    @abstractmethod
    def get_selected_range_ref(self) -> RangeReference:
        pass

    @abstractmethod
    def get_range_color(self, range_ref: RangeReference) -> str:
        pass

    @abstractmethod
    def set_ranges_color(self, range_refs: Iterable[RangeReference], color: str):
        pass

    @abstractmethod
    def set_colors_from_dict(self, colors: dict[RangeReference, str]):
        pass

    @abstractmethod
    def set_formula(self, range_ref: RangeReference, formula: str):
        pass

    @abstractmethod
    def disable_screen_updating(self):
        pass

    @abstractmethod
    def enable_screen_updating(self):
        pass

    @abstractmethod
    def add_name(self, range_ref: RangeReference, new_name: str) -> None:
        pass

    @abstractmethod
    def get_names(self) -> dict[str, str]:
        pass

    @abstractmethod
    def resolve_defined_name(self, name: str) -> Optional[RangeReference]:
        pass

    @abstractmethod
    def get_used_range(self) -> Iterable[tuple[RangeReference, str, str]]:
        pass

    @abstractmethod
    def resolve_range_reference(self, ref: RangeReference) -> tuple[str, str]:
        pass

    @abstractmethod
    def get_workbook_name(self) -> str:
        pass

    @abstractmethod
    def grayscale_colors_and_return_initial_colors(self) -> dict[RangeReference, str]:
        pass

    @abstractmethod
    def initial_to_grayscale_and_set_from_dict_and_return_initial_colors(
            self, new_colors: dict[RangeReference, str]
    ) -> dict[RangeReference, str]:
        pass
