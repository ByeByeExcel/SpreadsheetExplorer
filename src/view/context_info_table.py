from tkinter import Frame, ttk
from tkinter.ttk import Treeview, Scrollbar


class ContextInfoTable(Frame):
    def __init__(self, master, app_state):
        super().__init__(master)
        self.app_state = app_state

        self.tree = Treeview(
            self,
            columns=("cell", "sheet", "workbook", "formula", "value"),
            show="tree headings",
            height=9
        )
        style = ttk.Style(self)
        style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))
        style.configure("Treeview", font=("Helvetica", 10))
        style.configure("Treeview", indent=10)  # Decrease default indent (default is ~20)

        self.tree.heading("cell", text="Cell")
        self.tree.heading("sheet", text="Sheet")
        self.tree.heading("workbook", text="Workbook")
        self.tree.heading("formula", text="Formula")
        self.tree.heading("value", text="Value")

        self.tree.column("#0", width=40, anchor="center")
        self.tree.column("cell", width=50, anchor="center")
        self.tree.column("sheet", width=50, anchor="w")
        self.tree.column("workbook", width=50, anchor="w")
        self.tree.column("formula", width=90, anchor="w")
        self.tree.column("value", width=55, anchor="e")

        scrollbar = Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Subscribe to context information updates
        self.app_state.context_information.add_observer(self.update_table)

    def update_table(self, new_value, _):
        context_info = new_value
        self.tree.delete(*self.tree.get_children())

        def add_precedents_to_tree(precedents, parent="", level=""):
            num: int = 1
            for precedent in precedents:
                wb = precedent.cell_address.workbook
                sheet = precedent.cell_address.sheet
                cell = precedent.cell_address.address
                item_id = self.tree.insert(
                    parent,
                    "end",
                    text=f"{level}{num}",
                    values=(
                        cell,
                        sheet,
                        wb,
                        precedent.formula or "",
                        precedent.value or ""
                    )
                )
                if precedent.precedents_information:
                    add_precedents_to_tree(precedent.precedents_information, item_id, f"{level}{num}.")
                num += 1

        if context_info and context_info.precedents_information:
            add_precedents_to_tree(context_info.precedents_information)
