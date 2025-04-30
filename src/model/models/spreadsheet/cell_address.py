import functools
import re
from enum import Enum, auto
from typing import Optional


class CellAddressType(Enum):
    EXTERNAL = auto()
    CELL = auto()
    RANGE = auto()
    DEFINED_NAME_GLOBAL = auto()
    DEFINED_NAME_LOCAL = auto()


@functools.total_ordering
class CellAddress:
    def __init__(self, workbook: str, sheet: Optional[str], address: str,
                 address_type: CellAddressType = CellAddressType.CELL):
        self.workbook: str = workbook.lower()
        self.sheet: Optional[str] = sheet.lower() if sheet else None
        self.address: str = address.replace("$", "").lower()
        self.address_type: CellAddressType = address_type

    def __repr__(self):
        return f"<CellAddress '[{self.workbook}]{self.sheet}'!{self.address}>"

    def __str__(self):
        return f"'[{self.workbook}]{self.sheet}'!{self.address}"

    def __eq__(self, other):
        if not isinstance(other, CellAddress):
            return NotImplemented
        return (self.workbook, self.sheet, self.address, self.address_type) == \
            (other.workbook, other.sheet, other.address, other.address_type)

    def __hash__(self):
        return hash(str(self))

    def __lt__(self, other):
        if not isinstance(other, CellAddress):
            return NotImplemented
        return (self.workbook, self.sheet or "", self._address_key(), self.address_type.value) < \
            (other.workbook, other.sheet or "", other._address_key(), other.address_type.value)

    def _address_key(self):
        match = re.match(r"([a-z]+)(\d+)$", self.address)
        if match:
            col, row = match.groups()
            return col, int(row)
        return self.address, 0  # fallback for unexpected formats
