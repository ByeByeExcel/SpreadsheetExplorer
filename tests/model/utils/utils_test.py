from model.utils.utils import clamp


def test_clamp_within_bounds():
    assert clamp(5, 1, 10) == 5


def test_clamp_below_min():
    assert clamp(-5, 0, 10) == 0


def test_clamp_above_max():
    assert clamp(15, 0, 10) == 10


def test_clamp_on_edges():
    assert clamp(0, 0, 10) == 0
    assert clamp(10, 0, 10) == 10
