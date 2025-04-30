# view/widgets/context_info_table_widget.py

import tkinter as tk
from tkinter import ttk


class ContextInfoTable(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#f8f8f8", bd=1, relief="flat")

        # === Fonts ===
        bold_font = ("Arial", 14, "bold")
        normal_font = ("Arial", 14)

        # === Info Labels (Top) ===
        self.info_frame = tk.Frame(self, bg="#f8f8f8")
        self.info_frame.pack(fill="x", pady=(5, 5), padx=5)

        self.selected_range_var = tk.StringVar(value="-")
        self.formula_var = tk.StringVar(value="-")
        self.value_var = tk.StringVar(value="-")

        self.selected_range_title = tk.Label(self.info_frame, text="Selected Range:", anchor="w", font=bold_font,
                                             bg="#f8f8f8")
        self.selected_range_value = tk.Label(self.info_frame, textvariable=self.selected_range_var, anchor="w",
                                             font=normal_font, bg="#f8f8f8")

        self.formula_title = tk.Label(self.info_frame, text="Formula:", anchor="w", font=bold_font, bg="#f8f8f8")
        self.formula_value = tk.Label(self.info_frame, textvariable=self.formula_var, anchor="w", font=normal_font,
                                      bg="#f8f8f8")

        self.value_title = tk.Label(self.info_frame, text="Value:", anchor="w", font=bold_font, bg="#f8f8f8")
        self.value_value = tk.Label(self.info_frame, textvariable=self.value_var, anchor="w", font=normal_font,
                                    bg="#f8f8f8")

        self.selected_range_title.pack(side="left", padx=(0, 2))
        self.selected_range_value.pack(side="left", padx=(0, 10))
        self.formula_title.pack(side="left", padx=(0, 2))
        self.formula_value.pack(side="left", padx=(0, 10))
        self.value_title.pack(side="left", padx=(0, 2))
        self.value_value.pack(side="left", padx=(0, 10))

        self.precedents_label = tk.Label(
            self,
            text="Precedents (Inputs) of Selected Cell",
            anchor="w",
            font=normal_font,
            bg="#f8f8f8"
        )
        self.precedents_label.pack(fill="x", pady=(0, 5), padx=5)

        self.tree = ttk.Treeview(self, columns=("sheet", "workbook", "formula", "value"), show="tree headings")
        self.tree.heading("#0", text="Cell")
        self.tree.heading("sheet", text="Sheet")
        self.tree.heading("workbook", text="Workbook")
        self.tree.heading("formula", text="Formula")
        self.tree.heading("value", text="Value")

        self.tree.column("#0", width=120, anchor="w")
        self.tree.column("sheet", width=80, anchor="w")
        self.tree.column("workbook", width=80, anchor="w")
        self.tree.column("formula", width=125, anchor="w")
        self.tree.column("value", width=100, anchor="w")

        self.tree.pack(fill="both", expand=True, padx=5, pady=(0, 5))

    def update_selected_info(self, selected_range, formula, value):
        self.selected_range_var.set(selected_range)
        self.formula_var.set(formula)
        self.value_var.set(value)

    def clear_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
