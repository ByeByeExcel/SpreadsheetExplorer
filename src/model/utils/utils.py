import re

import openpyxl.utils


def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))


def get_row_col_from_address(address: str) -> tuple[str, int]:
    return openpyxl.utils.cell.coordinate_from_string(address)


def convert_to_absolute_range(address: str) -> str:
    if ":" in address:
        start, end = address.split(":")
        return f"{convert_to_absolute_address(start)}:{convert_to_absolute_address(end)}"
    return f"{convert_to_absolute_address(address)}"


def convert_to_absolute_address(address: str) -> str:
    return openpyxl.utils.absolute_coordinate(address)

def replace_cell_reference_in_formula(formula: str, target_cell: str, new_name: str) -> str:
    min_col, min_row, max_col, max_row = openpyxl.utils.cell.range_boundaries(target_cell)
    min_col_str = openpyxl.utils.cell.get_column_letter(min_col)
    max_col_str = openpyxl.utils.cell.get_column_letter(max_col)

    if min_col == max_col and min_row == max_row:
        pattern = rf"(?<![A-Z0-9$'])" \
                  rf"(\$?{min_col_str}\$?{min_row})" \
                  rf"(?![A-Z0-9])"
    else:
        pattern = rf"(?<![A-Z0-9$'])" \
                  rf"((?:'[^']+'|[A-Za-z0-9_]+)!?)?" \
                  rf"\$?{min_col_str}\$?{min_row}:\$?{max_col_str}\$?{max_row}" \
                  rf"(?![A-Z0-9])"

    return re.sub(pattern, new_name, formula, flags=re.IGNORECASE)
