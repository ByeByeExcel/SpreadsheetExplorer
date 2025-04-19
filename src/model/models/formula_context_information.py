from dataclasses import dataclass
from typing import Optional

from model.models.spreadsheet.cell_address import CellAddress


@dataclass
class RangeInformation:
    def __init__(self, cell_address: CellAddress, formula: str, value: str,
                 additional_information: Optional[str] = None):
        self.cell_address: CellAddress = cell_address
        self.formula: str = formula
        self.value: str = value
        self.additional_information: Optional[str] = additional_information

    def __repr__(self):
        return (f"<RangeInformation cell_address={self.cell_address},"
                f"formula={self.formula},"
                f"value={self.value},"
                f"additional_information={self.additional_information}>")

    def __eq__(self, other):
        if not isinstance(other, RangeInformation):
            return False
        return (self.cell_address == other.cell_address and
                self.formula == other.formula and
                self.value == other.value and
                self.additional_information == other.additional_information)

    def __hash__(self):
        return hash((self.cell_address, self.formula, self.value, self.additional_information))


@dataclass
class FormulaContextInformation:
    def __init__(self, selected_address: CellAddress, precedents_information: list[RangeInformation]):
        self.selected_address: CellAddress = selected_address
        self.precedents_information: list[RangeInformation] = precedents_information

    def __repr__(self):
        return (f"<FormulaContextInformation selected_address={self.selected_address},"
                f"precedents_information={self.precedents_information}>")

    def __eq__(self, other):
        if not isinstance(other, FormulaContextInformation):
            return False
        return (self.selected_address == other.selected_address and
                self.precedents_information == other.precedents_information)

    def __hash__(self):
        return hash((self.selected_address, tuple(self.precedents_information)))
