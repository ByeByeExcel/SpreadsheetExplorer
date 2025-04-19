from dataclasses import dataclass

from model.models.spreadsheet.cell_address import CellAddress, CellAddressType


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


@dataclass
class Worksheet:
    def __init__(self, name: str, cells: dict[CellAddress, Cell]):
        self.name: str = name
        self.cells: dict[CellAddress, Cell] = cells

    def __repr__(self):
        return f"<Worksheet {self.name}: {len(self.cells)} cells>"


@dataclass
class Workbook:
    def __init__(self):
        super().__init__()
        self.worksheets: dict[str, Worksheet] = {}
        self.cell_dependencies: CellDependencies = CellDependencies()

    def __repr__(self):
        return f"<SpreadsheetWorkbook: {len(self.worksheets)} sheet(s)>"

    def get_all_cells(self) -> set[Cell]:
        cells: set[Cell] = set()
        for sheet in self.worksheets.values():
            cells.update(sheet.cells.values())
        return cells

    def get_cell(self, cell_address: CellAddress) -> Cell | None:
        worksheet = self.worksheets.get(cell_address.sheet)
        if worksheet:
            return worksheet.cells.get(cell_address)
        return None


@dataclass
class CellDependencies:
    def __init__(self):
        self.precedents: dict[CellAddress, set[CellAddress]] = {}
        self.dependents: dict[CellAddress, set[CellAddress]] = {}

    def resolve_dependents(self, cell: CellAddress, resolved_dependents: set[CellAddress]) -> set[CellAddress]:
        for dependent in self.dependents.get(cell, set()):
            if dependent.address_type == CellAddressType.CELL:
                resolved_dependents.add(dependent)
            elif dependent.address_type != CellAddressType.EXTERNAL:
                resolved_dependents.update(self.resolve_dependents(dependent, resolved_dependents))
        return resolved_dependents

    def resolve_precedents(self, cell: CellAddress, resolved_precedents: set[CellAddress]) -> set[CellAddress]:
        for precedent in self.precedents.get(cell, set()):
            if precedent.address_type == CellAddressType.CELL:
                resolved_precedents.add(precedent)
            elif precedent.address_type != CellAddressType.EXTERNAL:
                resolved_precedents.update(self.resolve_precedents(precedent, resolved_precedents))
        return resolved_precedents
