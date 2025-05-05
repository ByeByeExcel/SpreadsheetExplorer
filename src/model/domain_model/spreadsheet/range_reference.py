import functools
import re
from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional


class RangeReferenceType(Enum):
    EXTERNAL = auto()
    CELL = auto()
    RANGE = auto()
    DEFINED_NAME_GLOBAL = auto()
    DEFINED_NAME_LOCAL = auto()


@functools.total_ordering
@dataclass(frozen=True)
class RangeReference:
    workbook: str
    sheet: Optional[str]
    reference: str
    reference_type: RangeReferenceType

    @property
    def formatted_reference(self) -> str:
        if self.reference_type not in {RangeReferenceType.DEFINED_NAME_LOCAL, RangeReferenceType.DEFINED_NAME_GLOBAL}:
            return self.reference.upper()
        return self.reference

    def __lt__(self, other):
        if not isinstance(other, RangeReference):
            return NotImplemented
        return (self.workbook, self.sheet or "", self._address_key(), self.reference_type.value) < \
            (other.workbook, other.sheet or "", other._address_key(), other.reference_type.value)

    def _address_key(self):
        match = re.match(r"([a-z]+)(\d+)$", self.reference)
        if match:
            col, row = match.groups()
            return col, int(row)
        return self.reference, 0  # fallback for named range

    @classmethod
    def from_raw(cls,
                 workbook: str,
                 sheet: Optional[str],
                 address: str,
                 address_type: RangeReferenceType = RangeReferenceType.CELL
                 ) -> "RangeReference":
        normalized_workbook = workbook.lower()
        normalized_sheet = sheet.lower() if sheet else None
        normalized_address = address.replace("$", "").lower()
        return RangeReference(
            normalized_workbook,
            normalized_sheet,
            normalized_address,
            address_type
        )
