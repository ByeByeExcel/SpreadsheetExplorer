from dataclasses import dataclass

from model.domain_model.spreadsheet.range_reference import RangeReference


@dataclass(frozen=True)
class CellRange:
    reference: RangeReference
    value: str
    formula: str
