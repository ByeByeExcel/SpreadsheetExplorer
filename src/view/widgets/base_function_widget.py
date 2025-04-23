import tkinter as tk
from tkinter import messagebox


class BaseFunctionWidget(tk.Frame):
    def __init__(self, master, app_state, feature_controller, output, **kwargs):
        super().__init__(master, **kwargs)
        self.app_state = app_state
        self.feature_controller = feature_controller
        self.output = output
        self._toggling = False

    def create_button(self, text, command, row, help_text=None, column=1):
        if help_text:
            help_button = tk.Button(self, text="?", width=2)
            help_button.grid(row=row, column=0, sticky="w", padx=(0, 5))
            self._add_tooltip(help_button, help_text)

        button = tk.Button(self, text=text, command=command, width=25)
        button.grid(row=row, column=column, padx=10, pady=(0, 0), sticky="ew")
        return button

    def toggle_feature(self, start_func, stop_func):
        if self._toggling:
            return

        self._toggling = True
        try:
            active_before = self.app_state.active_feature.value
            print(f"[DEBUG] Active feature BEFORE toggle: {active_before.name if active_before else 'None'}")

            if self.app_state.is_feature_active(self.feature):
                stop_func()
                self.after(1, lambda: self.app_state.set_feature_inactive(self.feature))
            else:
                if not self.app_state.can_start_feature():
                    raise ValueError("Cannot start feature — another is active or workbook not connected.")

                start_func()
                self.after(1, self._safe_activate)
        except Exception as e:
            messagebox.showerror("Feature Toggle Error", str(e))
        finally:
            self._toggling = False

    def _safe_activate(self):
        if not self.app_state.is_feature_active(self.feature):
            self.app_state.set_feature_active(self.feature)
        else:
            print(f"[DEBUG] Skipped redundant activation for {self.feature.name}")

    def _add_tooltip(self, widget, text):
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
