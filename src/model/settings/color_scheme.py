from enum import Enum


class ColorRole(Enum):
    DEPENDENT = "dependent"
    HEATMAP_0 = "heatmap_0"
    HEATMAP_1 = "heatmap_1"
    PRECEDENT = "precedent"
    ROOT_NODE = "root_node"


ColorScheme: dict[ColorRole, str] = {
    ColorRole.DEPENDENT: "#99ff99",  # light green
    ColorRole.HEATMAP_0: "#ffffcc",  # soft yellow
    ColorRole.HEATMAP_1: "#ff4444",  # bold red
    ColorRole.PRECEDENT: "#ff9999",  # light red
    ColorRole.ROOT_NODE: "#cce5ff"
}
