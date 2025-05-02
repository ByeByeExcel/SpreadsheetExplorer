from enum import Enum, auto


class Feature(Enum):
    CASCADE_RENAME = auto()
    DEPENDENCY_HIGHLIGHTING = auto()
    DEPENDENTS_HEATMAP = auto()
    ROOT_NODES = auto()
