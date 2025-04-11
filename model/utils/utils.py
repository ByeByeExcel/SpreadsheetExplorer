from typing import Optional

import webcolors


def get_hex_color_from_tuple(color) -> Optional[str]:
    if isinstance(color, tuple) and len(color) == 3:
        rgb: tuple[int, int, int] = (int(color[0]), int(color[1]), int(color[2]))
        return webcolors.rgb_to_hex(rgb)
    return None
