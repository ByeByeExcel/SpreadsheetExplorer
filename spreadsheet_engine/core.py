def compute_summary(spreadsheet):
    return {
        "total_sales": spreadsheet.get_value("B2"),
        "num_items": spreadsheet.get_value("B3")
    }
