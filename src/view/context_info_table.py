from tkinter import Frame, ttk
from tkinter.ttk import Treeview, Scrollbar


class ContextInfoTable(Frame):
    def __init__(self, master, app_state):
        super().__init__(master)
        self.app_state = app_state

        self.tree = Treeview(
            self,
            columns=("workbook", "sheet", "cell", "formula", "value"),
            show="headings",
            height=9
        )
        style = ttk.Style(self)
        style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))
        style.configure("Treeview", font=("Helvetica", 10))

        self.tree.heading("workbook", text="Workbook")
        self.tree.heading("sheet", text="Sheet")
        self.tree.heading("cell", text="Cell")
        self.tree.heading("formula", text="Formula")
        self.tree.heading("value", text="Value")

        self.tree.column("workbook", width=50, anchor="w")
        self.tree.column("sheet", width=50, anchor="w")
        self.tree.column("cell", width=50, anchor="center")
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

    def update_table(self, new_value, old_value):
        context_info = new_value
        self.tree.delete(*self.tree.get_children())

        if context_info and context_info.precedents_information:
            for precedent in context_info.precedents_information:
                wb = precedent.cell_address.workbook
                sheet = precedent.cell_address.sheet
                cell = precedent.cell_address.address
                self.tree.insert(
                    "",
                    "end",
                    values=(
                        wb,
                        sheet,
                        cell,
                        precedent.formula or "",
                        precedent.value or ""
                    )
                )
