import tkinter as tk
from doctest import master
from tkinter import ttk

from view.output_section import OutputSection
from view.function_buttons import FunctionButtonSection
from view.workbook_selector import WorkbookSelector


class MainView:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Excel Summary Tool")
        self.root.geometry("650x550")

        # === Create components but delay layout ===
        self.output = OutputSection(self.root, pack=False)
        ttk.Separator(self.root, orient="horizontal").pack(fill="x", padx=20, pady=(5, 10))
        self.buttons = FunctionButtonSection(self.root, self.output, pack=False)
        self.workbook_selector = WorkbookSelector(self.root, self.buttons, self.output, pack=False)

        # === Now pack them in correct visual order ===
        self.workbook_selector.pack()
        self.buttons.pack()
        self.output.pack()

    def run(self):
        self.root.mainloop()
