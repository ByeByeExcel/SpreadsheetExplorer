import tkinter as tk


class ToolTip:
    def __init__(self, widget, text, wraplength=300, timeout=7000):
        self.widget = widget
        self.text = text
        self.wraplength = wraplength
        self.timeout = timeout
        self.tip_window = None

        self.widget.bind("<Enter>", self.show_tip)
        self.widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        if self.tip_window or not self.text:
            return

        x = self.widget.winfo_rootx() + self.widget.winfo_width() // 2 + 25
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 10

        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")

        label = tk.Label(
            tw,
            text=self.text,
            justify="left",
            background="#ffffe0",
            relief="solid",
            borderwidth=1,
            font=("Arial", 10),
            wraplength=self.wraplength
        )
        label.pack(ipadx=5, ipady=3)

        tw.after(self.timeout, self.hide_tip)

    def hide_tip(self, event=None):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None
