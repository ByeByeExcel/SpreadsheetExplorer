from model.domain_model.feature import Feature


class FeatureButtonTextManager:
    _texts = {
        Feature.DEPENDENCY_HIGHLIGHTING: {
            "inactive": "Show Inputs & Outputs of Selected Cell",
            "active": "Hide Inputs & Outputs of Selected Cell",
            "help": "Color all cells that influence (precedents) or are influenced by (dependents) the selected cell — helping you understand the spreadsheet’s data flow. Inputs (precedents) are shown in blue, outputs (dependents) in orange."
        },
        Feature.DEPENDENTS_HEATMAP: {
            "inactive": "Show Cell Usage Heatmap",
            "active": "Hide Cell Usage Heatmap",
            "help": "Color all cells that are used by other cells (how much a cell is reused)."
        },
        Feature.ROOT_NODES: {
            "inactive": "Show Final Output Cells",
            "active": "Hide Final Output Cells",
            "help": "Highlight all cells that are the end points of calculation chains."
        },
        Feature.CASCADE_RENAME: {
            "inactive": "Rename Cell & Update Formulas",
            "active": "Cancel Renaming",
            "help": "Experimental feature: rename the selected cell and automatically update all formulas depending on it."
        },
    }

    @staticmethod
    def get_button_text(feature, active: bool):
        if active:
            return FeatureButtonTextManager._texts[feature]["active"]
        else:
            return FeatureButtonTextManager._texts[feature]["inactive"]

    @staticmethod
    def get_help_text(feature):
        return FeatureButtonTextManager._texts[feature]["help"]
