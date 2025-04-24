from dataclasses import dataclass

from model.models.spreadsheet.cell_address import CellAddress


@dataclass
class Cell:
    def __init__(self, address: CellAddress, value: str, formula: str):
        self.address: CellAddress = address
        self.value: str = value
        self.formula: str = formula

    def __repr__(self):
        return f"<Cell {self.address}: value={self.value}, formula={self.formula}>"

    def __hash__(self):
        return hash((self.address, self.value, self.formula))

    def __eq__(self, other):
        if not isinstance(other, Cell):
            return False
        return (self.address, self.value, self.formula) == (other.address, other.value, other.formula)
