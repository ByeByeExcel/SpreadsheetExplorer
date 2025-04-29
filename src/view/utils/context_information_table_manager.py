class ContextInformationManager:
    def __init__(self, context_info_table, feature_controller, app_state):
        self.context_table = context_info_table
        self.feature_controller = feature_controller
        self.app_state = app_state

        app_state.selected_cell.add_observer(self._update_selected_cell_info)
        app_state.context_information.add_observer(self._update_context_table)

    def _safe_get(self, obj, attr, default="-"):
        return getattr(obj, attr, default) or default

    def _update_selected_cell_info(self, new_value, _):
        selected_range = self._safe_get(new_value, 'address')
        self.context_table.update_selected_info(selected_range, "-", "-")

        if new_value:
            self.feature_controller.start_context_information()
        else:
            self.context_table.clear_table()

    def _update_context_table(self, new_value, _):
        self.context_table.clear_table()

        if not new_value:
            return

        formula = self._safe_get(new_value, 'formula')
        value = self._safe_get(new_value, 'value')
        selected_range = self._safe_get(self.app_state.selected_cell.value, 'address')

        self.context_table.update_selected_info(selected_range, formula, value)

        for precedent in getattr(new_value, 'precedents_information', []):
            parent_id = self._insert_precedent(precedent)
            self._insert_subprecedents(precedent, parent_id)

    def _insert_precedent(self, precedent, parent=""):
        address = precedent.cell_address
        return self.context_table.tree.insert(
            parent,
            "end",
            text=f" {self._safe_get(address, 'address')}",
            values=(
                self._safe_get(address, 'sheet'),
                self._safe_get(address, 'workbook'),
                self._safe_get(precedent, 'formula'),
                self._safe_get(precedent, 'value')
            )
        )

    def _insert_subprecedents(self, precedent, parent_id):
        for subprecedent in getattr(precedent, 'precedents_information', []):
            child_id = self._insert_precedent(subprecedent, parent=parent_id)
            self._insert_subprecedents(subprecedent, child_id)
