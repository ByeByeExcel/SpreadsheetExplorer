from enum import Enum, auto
from typing import Optional

from model.utils.utils import get_row_col_from_address


class CellAddressType(Enum):
    EXTERNAL = auto()
    CELL = auto()
    RANGE = auto()
    DEFINED_NAME_GLOBAL = auto()
    DEFINED_NAME_LOCAL = auto()


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
        return str(self) == str(other)

    def __hash__(self):
        return hash(str(self))

    def full_address(self) -> str:
        return str(self)

    def is_range(self) -> bool:
        return ":" in self.address

    def is_cell_reference(self) -> bool:
        if self.is_range():
            parts = self.address.split(":")
            try:
                get_row_col_from_address(parts[0])
                get_row_col_from_address(parts[1])
                return True
            except ValueError:
                return False
        else:
            try:
                get_row_col_from_address(self.address)
                return True
            except ValueError:
                return False
