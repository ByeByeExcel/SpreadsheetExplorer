import tkinter as tk
from tkinter import filedialog, messagebox

from spreadsheet_api.xlwings_adapter import ExcelSpreadsheet
from spreadsheet_engine.core import compute_summary


def run_app():
    def load_and_compute():
        filepath = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xlsm")])
        if filepath:
            try:
                sheet = ExcelSpreadsheet(filepath)
                result = compute_summary(sheet)
                output_label.config(
                    text=f"Total Sales: {result['total_sales']}\nItems: {result['num_items']}"
                )
                sheet.close()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    root = tk.Tk()
    root.title("Excel Summary Tool")

    tk.Button(root, text="Load Excel File", command=load_and_compute).pack(pady=10)
    output_label = tk.Label(root, text="", font=("Arial", 12))
    output_label.pack(pady=10)

    root.mainloop()
