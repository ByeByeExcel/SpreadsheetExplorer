from dataclasses import dataclass
from typing import Optional

from model.models.spreadsheet.cell_address import CellAddress


@dataclass
class RangeInformation:
    cell_address: CellAddress
    formula: str
    value: str
    precedents_information: Optional[list["RangeInformation"]] = None
    additional_information: Optional[str] = None

    def __repr__(self):
        return (f"<RangeInformation cell_address={self.cell_address}, "
                f"formula={self.formula}, "
                f"value={self.value}, "
                f"additional_information={self.additional_information}, "
                f"precedents_information={self.precedents_information}>")

    def __eq__(self, other):
        if not isinstance(other, RangeInformation):
            return False
        return (self.cell_address == other.cell_address and
                self.formula == other.formula and
                self.value == other.value and
                self.additional_information == other.additional_information and
                self.precedents_information == other.precedents_information)

    def __hash__(self):
        precedents_hashable = tuple(self.precedents_information) if self.precedents_information else ()
        return hash((
            self.cell_address,
            self.formula,
            self.value,
            self.additional_information,
            precedents_hashable
        ))
