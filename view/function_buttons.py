import tkinter as tk
from tkinter import messagebox

class FunctionButtonSection:
    def __init__(self, master, output, pack=True):
        self.output = output
        self.frame = tk.Frame(master, padx=20)
        if pack:
            self.pack()

        # Function 1
        self.btn_func1 = tk.Button(self.frame, text="Function 1", width=20, height=1,
                                   state=tk.DISABLED, command=lambda: self.output.write("[Function 1] Coming soon..."))
        self.btn_func1.grid(row=0, column=0, sticky="w", pady=4)
        tk.Button(self.frame, text="?", width=2, command=lambda: self.show_help("Function 1", "This function will later summarize your data.")).grid(row=0, column=1)

        # Function 2 with input
        self.func2_input_var = tk.StringVar()
        self.btn_func2 = tk.Button(self.frame, text="Function 2", width=20, height=1,
                                   state=tk.DISABLED, command=self.activate_func2_input)
        self.btn_func2.grid(row=1, column=0, sticky="w", pady=4)
        tk.Button(self.frame, text="?", width=2, command=lambda: self.show_help("Function 2", "This function accepts input from the user.")).grid(row=1, column=1)

        self.entry_func2 = tk.Entry(self.frame, textvariable=self.func2_input_var, width=20, state=tk.DISABLED)
        self.entry_func2.grid(row=1, column=2, padx=(10, 0))
        self.btn_accept_func2 = tk.Button(self.frame, text="Accept", state=tk.DISABLED, command=self.handle_func2_input)
        self.btn_accept_func2.grid(row=1, column=3, padx=5)

        # Function 3
        self.btn_func3 = tk.Button(self.frame, text="Function 3", width=20, height=1,
                                   state=tk.DISABLED, command=lambda: self.output.write("[Function 3] Coming soon..."))
        self.btn_func3.grid(row=2, column=0, sticky="w", pady=4)
        tk.Button(self.frame, text="?", width=2, command=lambda: self.show_help("Function 3", "This function will perform export operations.")).grid(row=2, column=1)

    def activate_func2_input(self):
        self.entry_func2.config(state=tk.NORMAL)
        self.btn_accept_func2.config(state=tk.NORMAL)
        self.func2_input_var.set("")
        self.output.write("[Function 2] Awaiting input...")

    def handle_func2_input(self):
        value = self.func2_input_var.get().strip()
        if value:
            self.output.write(f"[Function 2] Received input: {value}")
        else:
            self.output.write("[Function 2] No input entered.")

    def show_help(self, title, description):
        messagebox.showinfo(title, description)

    def set_buttons_state(self, state):
        self.btn_func1.config(state=state)
        self.btn_func2.config(state=state)
        self.btn_func3.config(state=state)
        self.entry_func2.config(state=tk.DISABLED)
        self.btn_accept_func2.config(state=tk.DISABLED)

    def pack(self):
        self.frame.pack(fill="x", anchor="w")
