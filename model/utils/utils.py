import re
from typing import Tuple


def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))


def get_row_col_from_address(address: str) -> tuple[str, int]:
    match = re.fullmatch(r"(\$?[A-Za-z]+)(\$?\d+)", address)
    if not match:
        raise ValueError(f"Invalid address format: {address}")

    col_str, row_str = match.groups()
    col = col_str.replace("$", "").upper()
    row = int(row_str.replace("$", ""))

    # Convert column letters to number (e.g., A=1, Z=26, AA=27, ..., XFD=16384)
    col_num = 0
    for char in col:
        col_num = col_num * 26 + (ord(char.upper()) - ord('A') + 1)

    # Check limits
    if not (1 <= col_num <= 16384):
        raise ValueError(f"Invalid column: {col} (max = XFD)")
    if not (1 <= row <= 1048576):
        raise ValueError(f"Invalid row: {row} (max = 1048576)")

    return col, row


def convert_to_absolute_range(address: str) -> str:
    if not address:
        raise ValueError(f"Invalid address format: {address}")
    if ":" in address:
        start, end = address.split(":")
        return f"{convert_to_absolute_address(start)}:{convert_to_absolute_address(end)}"
    else:
        return f"{convert_to_absolute_address(address)}"


def convert_to_absolute_address(address: str) -> str:
    col, row = get_row_col_from_address(address)
    return f"${col}${row}"


def replace_cell_reference_in_formula(formula: str, target_cell: str, new_name: str) -> str:
    col, row = get_row_col_from_address(target_cell)

    pattern = rf"(?<![A-Z0-9$])(\$?{col}\$?{row})(?![0-9A-Z])"

    return re.sub(pattern, new_name, formula, flags=re.IGNORECASE)


def column_number_to_letter(n: int) -> str:
    result = ''
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        result = chr(65 + remainder) + result
    return result


def generate_addresses(start_row: int, start_col: int, shape: Tuple[int, int]) -> list[list[str]]:
    n_rows, n_cols = shape
    grid = [
        [
            f"{column_number_to_letter(start_col + col)}{start_row + row}"
            for col in range(n_cols)
        ]
        for row in range(n_rows)
    ]
    return grid
