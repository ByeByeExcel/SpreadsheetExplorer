import tkinter as tk
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
        self.buttons = FunctionButtonSection(self.root, self.output, pack=False)
        self.workbook_selector = WorkbookSelector(self.root, self.buttons, self.output, pack=False)

        # === Pack components in correct top-down order ===
        self.workbook_selector.pack()

        # 🆕 Selected Range Label (hardcoded for now)
        self.selected_range_label = tk.Label(
            self.root,
            text="Selected Range: A1",  # Static placeholder
            font=("Arial", 12, "bold"),
            anchor="w",
            padx=20
        )
        self.selected_range_label.pack(fill="x", pady=(0, 10))

        # Function buttons and output
        self.buttons.pack()
        self.output.pack()

    def run(self):
        self.root.mainloop()
