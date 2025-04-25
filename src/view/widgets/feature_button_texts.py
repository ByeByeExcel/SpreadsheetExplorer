from model.feature import Feature

class FeatureButtonTextManager:
    BUTTON_TEXTS = {
        Feature.DEPENDENCY_HIGHLIGHTING: ("Show dependents/precedents", "Hide dependents/precedents"),
        Feature.DEPENDENTS_HEATMAP: ("Show Heatmap", "Hide Heatmap"),
        Feature.ROOT_NODES: ("Show Root Nodes", "Hide Root Nodes"),
        Feature.CASCADE_RENAME: ("Cascade Rename", "Cancel Renaming"),
    }

    @classmethod
    def get_text(cls, feature: Feature, active: bool) -> str:
        return cls.BUTTON_TEXTS.get(feature, ("Show", "Hide"))[1 if active else 0]
