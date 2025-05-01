from model.domain_model.spreadsheet.range_with_context import RangeWithContext


class ContextInformationManager:
    def __init__(self, context_info_table, feature_controller, app_state):
        self.context_table = context_info_table
        self.feature_controller = feature_controller
        self.app_state = app_state

        app_state.selected_range_with_context.add_observer(self._update_context_table)

    def _safe_get(self, obj, attr, default="-"):
        return getattr(obj, attr, default) or default

    def _update_context_table(self, new_range_with_context: RangeWithContext, _):
        self.context_table.clear_table()

        if not new_range_with_context:
            return

        formula = self._safe_get(new_range_with_context, 'formula')
        value = self._safe_get(new_range_with_context, 'value')
        selected_range = self._safe_get(new_range_with_context.reference, 'reference')

        self.context_table.update_selected_info(selected_range, formula, value)

        for precedent in new_range_with_context.precedents:
            parent_id = self._insert_precedent(precedent)
            self._insert_subprecedents(precedent, parent_id)

    def _insert_precedent(self, precedent, parent=""):
        address = precedent.reference
        return self.context_table.tree.insert(
            parent,
            "end",
            text=f" {self._safe_get(address, 'reference')}",
            values=(
                self._safe_get(address, 'sheet'),
                self._safe_get(address, 'workbook'),
                self._safe_get(precedent, 'formula'),
                self._safe_get(precedent, 'value')
            )
        )

    def _insert_subprecedents(self, precedent, parent_id):
        for subprecedent in precedent.precedents:
            child_id = self._insert_precedent(subprecedent, parent=parent_id)
            self._insert_subprecedents(subprecedent, child_id)
