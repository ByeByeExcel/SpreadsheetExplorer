import tkinter as tk
from tkinter import messagebox


def _add_tooltip(widget, text):
    tooltip = tk.Toplevel(widget)
    tooltip.withdraw()
    tooltip.overrideredirect(True)
    tooltip_label = tk.Label(tooltip, text=text, background="lightyellow", relief="solid", borderwidth=1, padx=4,
                             pady=2, wraplength=250)
    tooltip_label.pack()

    def enter(event):
        tooltip.geometry(f"+{event.x_root + 10}+{event.y_root + 10}")
        tooltip.deiconify()

    def leave(event):
        tooltip.withdraw()

    widget.bind("<Enter>", enter)
    widget.bind("<Leave>", leave)


class BaseFunctionWidget(tk.Frame):
    def __init__(self, master, app_state, feature_controller, output, **kwargs):
        super().__init__(master, **kwargs)
        self.feature = None
        self.app_state = app_state
        self.feature_controller = feature_controller
        self.output = output
        self._start_func = None
        self._stop_func = None

    def create_button(self, text, command, row, help_text=None, column=1):
        if help_text:
            help_button = tk.Button(self, text="?", width=2)
            help_button.grid(row=row, column=0, sticky="w", padx=(0, 5))
            _add_tooltip(help_button, help_text)

        button = tk.Button(self, text=text, command=command, width=25)
        button.grid(row=row, column=column, padx=10, pady=(0, 0), sticky="ew")
        return button

    def initialize_feature_button(self, row, help_text):
        from view.widgets.feature_button_texts import FeatureButtonTextManager
        return self.create_button(
            text=FeatureButtonTextManager.get_text(self.feature, False),
            command=self.toggle,
            row=row,
            help_text=help_text
        )

    def set_toggle_function(self, start_func, stop_func):
        self._start_func = start_func
        self._stop_func = stop_func

    def toggle(self):
        self.toggle_feature(self._start_func, self._stop_func)

    def toggle_feature(self, start_func, stop_func):
        try:
            if self.app_state.is_feature_active(self.feature):
                stop_func()
                self.log(f"[INFO] Stopped feature: {self.feature.name}")
            else:
                if not self.app_state.can_start_feature():
                    raise ValueError("Cannot start feature — another is active or workbook not connected.")
                start_func()
                self.log(f"[INFO] Started feature: {self.feature.name}")
        except Exception as e:
            self.log(f"[ERROR] Feature toggle failed: {e}")
            messagebox.showerror("Feature Toggle Error", str(e))

    def log(self, message: str):
        if self.output:
            self.output.write(message)
        else:
            print(message)
