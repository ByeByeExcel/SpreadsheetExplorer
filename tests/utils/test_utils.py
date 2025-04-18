import pytest

from model.utils.utils import convert_to_absolute_range, get_row_col_from_address


# --- Tests for get_row_col_from_address ---

@pytest.mark.parametrize("input_address, expected", [
    ("A1", ("A", 1)),
    ("B12", ("B", 12)),
    ("AA100", ("AA", 100)),
    ("$C$3", ("C", 3)),
    ("$Z999", ("Z", 999)),
])
def test_get_row_col_from_address_valid(input_address, expected):
    assert get_row_col_from_address(input_address) == expected


@pytest.mark.parametrize("input_address", [
    "123",  # no column
    "ABC",  # no row
    "A1B",  # invalid pattern
    "$$A$1",  # too many $
    "A$",  # no row
    "",  # empty string
    "1A",  # invalid order
    "Name4"  # column limit
    "B9293423",  # row limit
])
def test_get_row_col_from_address_invalid(input_address):
    with pytest.raises(ValueError):
        get_row_col_from_address(input_address)


# --- Tests for convert_to_absolute_address ---

@pytest.mark.parametrize("input_address, expected", [
    ("A1", "$A$1"),
    ("$B$2", "$B$2"),
    ("Z99", "$Z$99"),
])
def test_convert_to_absolute_address_valid(input_address, expected):
    assert convert_to_absolute_address(input_address) == expected


@pytest.mark.parametrize("input_address", [
    "XYZ",  # no row
    "123",  # no column
    "AB$",  # invalid
    "",  # empty
])
def test_convert_to_absolute_address_invalid(input_address):
    with pytest.raises(ValueError):
        convert_to_absolute_address(input_address)


# --- Tests for convert_to_absolute_range ---

@pytest.mark.parametrize("input_range, expected", [
    ("A1", "$A$1"),
    ("A1:B2", "$A$1:$B$2"),
    ("$C$3:D4", "$C$3:$D$4"),
])
def test_convert_to_absolute_range_valid(input_range, expected):
    assert convert_to_absolute_range(input_range) == expected


@pytest.mark.parametrize("input_range", [
    "",  # empty
    "123",  # no column
    "A1:",  # missing end
    ":B2",  # missing start
    "A1:B",  # incomplete end
    "X:Y:Z",  # too many colons
])
def test_convert_to_absolute_range_invalid(input_range):
    # Invalid addresses should raise inside convert_to_absolute_address
    with pytest.raises(ValueError):
        convert_to_absolute_range(input_range)


@pytest.mark.parametrize("formula, target_cell, new_name, expected", [
    # standard
    ("=A1+B1", "A1", "Start", "=Start+B1"),
    ("=SUM(A1:B1)", "A1", "Start", "=SUM(Start:B1)"),
    ("=IF(A1>0,A1,0)", "A1", "val", "=IF(val>0,val,0)"),

    # absolute ref
    ("=$A$1+B1", "A1", "Start", "=Start+B1"),
    ("=$A$1+$B$2", "B2", "Other", "=$A$1+Other"),

    # ensure, that not part of the address is replaced
    ("=A10+A1", "A1", "X", "=A10+X"),
    ("=A11", "A1", "Z", "=A11"),

    # several instances
    ("=A1+A1+A1", "A1", "val", "=val+val+val"),
    ("=A1+3+sum(A$1-3)* $a1", "A1", "val", "=val+3+sum(val-3)* val"),

    # upper / lowercase
    ("=a1+A1", "A1", "X", "=X+X"),
    ("=Sum(A1:B2)", "B2", "End", "=Sum(A1:End)"),
])
def test_replace_cell_reference_in_formula(formula, target_cell, new_name, expected):
    assert replace_cell_reference_in_formula(formula, target_cell, new_name) == expected


@pytest.mark.parametrize("formula, target_cell, new_name", [
    ("=A1+B1", "", "X"),  # leer
    ("=A1+B1", "1A", "X"),  # Zahl vor Buchstabe
    ("=A1+B1", "AB", "X"),  # keine Zeile
    ("=A1+B1", "123", "X"),  # keine Spalte
    ("=A1+B1", "$$A$1", "X"),  # ungültige Form mit Dollarzeichen
    ("=A1+B1", "A", "X"),  # unvollständig
    ("=A1+B1", "!!", "X"),  # Sonderzeichen
])
def test_replace_cell_reference_invalid_target(formula, target_cell, new_name):
    with pytest.raises(ValueError):
        replace_cell_reference_in_formula(formula, target_cell, new_name)
