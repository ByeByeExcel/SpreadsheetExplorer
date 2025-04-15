from typing import cast, Optional

import webcolors

from model.utils.utils import clamp


def interpolate_color(color1: str, color2: str, t: float) -> str:
    t = clamp(t, 0, 1)
    rgb1 = webcolors.hex_to_rgb(color1)
    rgb2 = webcolors.hex_to_rgb(color2)

    interpolated = tuple(
        int((1 - t) * c1 + t * c2)
        for c1, c2 in zip(rgb1, rgb2)
    )
    return webcolors.rgb_to_hex(cast(tuple[int, int, int], interpolated))


def get_hex_color_from_tuple(color) -> Optional[str]:
    if isinstance(color, tuple) and len(color) == 3:
        rgb: tuple[int, int, int] = (int(color[0]), int(color[1]), int(color[2]))
        return webcolors.rgb_to_hex(rgb)
    return None


def rgb_to_grayscale(rgb: tuple) -> Optional[tuple[int, int, int]]:
    if not isinstance(rgb, tuple) or len(rgb) != 3:
        return None
    r, g, b = rgb
    r = clamp(r, 0, 255)
    return r, r, r
