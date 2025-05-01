from dataclasses import dataclass
from typing import Optional

from model.domain_model.spreadsheet.cell_range import CellRange


@dataclass(frozen=True)
class RangeWithContext(CellRange):
    precedents: Optional[list["RangeWithContext"]]
    context_information: Optional[str] = None
