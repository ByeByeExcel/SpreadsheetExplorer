import re


class CellAddress:
    def __init__(self, workbook: str, sheet: str, address: str):
        self.workbook: str = workbook.lower()
        self.sheet: str = sheet.lower()
        self.address: str = address.replace("$", "").lower()

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

    @classmethod
    def from_excel_ref(cls, ref: str):
        match = re.match(r"'?\[(.*?)](.*?)'?!(.+)", ref)
        if match:
            workbook, sheet, address = match.groups()
            return cls(workbook, sheet, address)

        raise ValueError(f"Invalid reference: {ref}")
