from model.models.spreadsheet.cell_address import CellAddress


class Cell:
    def __init__(self, address: str, value: str, formula: str):
        self.address: str = address
        self.value: str = value
        self.formula: str = formula

    def __repr__(self):
        return f"<Cell {self.address}: value={self.value}, formula={self.formula}>"


class Worksheet:
    def __init__(self, name: str, cells: dict[str, Cell]):
        self.name: str = name
        self.cells: dict[str, Cell] = cells

    def __repr__(self):
        return f"<Worksheet {self.name}: {len(self.cells)} cells>"


class Workbook:
    def __init__(self):
        super().__init__()
        self.worksheets: dict[str, Worksheet] = {}
        self.cell_dependencies: CellDependencies = CellDependencies()

    def __repr__(self):
        return f"<SpreadsheetWorkbook: {len(self.worksheets)} sheet(s)>"


class CellDependencies:
    def __init__(self):
        self.precedents: dict[CellAddress, set[CellAddress]] = {}
        self.dependents: dict[CellAddress, set[CellAddress]] = {}
