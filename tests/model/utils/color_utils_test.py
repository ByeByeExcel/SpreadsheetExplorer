from model.utils.color_utils import interpolate_color, get_hex_color_from_tuple, rgb_to_grayscale


def test_interpolate_color_midpoint():
    color1 = '#000000'
    color2 = '#ffffff'
    result = interpolate_color(color1, color2, 0.5)
    assert result.lower() == '#7f7f7f'


def test_interpolate_color_clamping():
    color1 = '#000000'
    color2 = '#ffffff'
    result_below = interpolate_color(color1, color2, -1)
    result_above = interpolate_color(color1, color2, 2)
    assert result_below.lower() == '#000000'
    assert result_above.lower() == '#ffffff'


def test_get_hex_color_from_valid_tuple():
    rgb = (255, 0, 0)
    result = get_hex_color_from_tuple(rgb)
    assert result.lower() == '#ff0000'


def test_get_hex_color_from_invalid_input():
    assert get_hex_color_from_tuple((255,)) is None
    assert get_hex_color_from_tuple('not_a_tuple') is None


def test_rgb_to_grayscale_valid():
    rgb = (255, 0, 0)
    gray = rgb_to_grayscale(rgb)
    expected = int(0.299 * 255 + 0.587 * 0 + 0.114 * 0)
    assert gray == (expected, expected, expected)


def test_rgb_to_grayscale_invalid():
    assert rgb_to_grayscale((255,)) is None
    assert rgb_to_grayscale('not_a_tuple') is None
