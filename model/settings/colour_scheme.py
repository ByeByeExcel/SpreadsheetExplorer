from enum import Enum


class ColorRole(Enum):
    PRECEDENT = "precedent"
    DEPENDENT = "dependent"
    HEATMAP_0 = "heatmap_0"
    HEATMAP_1 = "heatmap_1"


ColourScheme: dict[ColorRole, str] = {
    ColorRole.PRECEDENT: "#ff9999",  # light red
    ColorRole.DEPENDENT: "#99ff99",  # light green
    ColorRole.HEATMAP_0: "#ffffcc",  # soft yellow
    ColorRole.HEATMAP_1: "#ff4444",  # bold red
}
