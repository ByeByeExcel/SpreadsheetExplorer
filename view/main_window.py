import tkinter as tk


def run_view():
    root = tk.Tk()
    root.title("Excel Summary Tool")

    tk.Button(root, text="Load Excel File").pack(pady=10)
    output_label = tk.Label(root, text="", font=("Arial", 12))
    output_label.pack(pady=10)

    root.mainloop()
