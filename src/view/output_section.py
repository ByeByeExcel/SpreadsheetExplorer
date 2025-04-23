import tkinter as tk


class OutputSection:
    def __init__(self, master, pack=True, app_state=None):
        self.app_state = app_state
        self.frame = tk.Frame(master, padx=20, pady=10)

        if pack:
            self.pack()

        tk.Label(self.frame, text="Output:", font=("Arial", 11)).pack(anchor="w")

        self.text = tk.Text(self.frame, height=10, bg="#f4f4f4", state=tk.NORMAL)
        self.text.pack(fill="both", expand=True, pady=5)

        clear_button = tk.Button(self.frame, text="Clear Output", command=self.clear_output)
        clear_button.pack(anchor="e", pady=(5, 0))

    def write(self, msg):
        self.text.insert(tk.END, msg + "\n")
        self.text.see(tk.END)

    def clear_output(self):
        self.text.delete("1.0", tk.END)

    def pack(self):
        self.frame.pack(fill="both", expand=True)
