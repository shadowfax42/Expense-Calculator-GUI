import tkinter as tk
import matplotlib.pyplot as plt


class ThemeManager:
    def __init__(self, app):
        self.app = app
        self.dark_mode = False
        self.themes = {
            "light": {
                "bg_main": "#ffffff",
                "bg_header": "#888888",
                "title_color": "#FFD700",  # Yellow/Mustard color
                "bg_form": "#ffffff",
                "bg_entry": "#ffffff",
                "bg_button_primary": "#4CAF50",
                "bg_button_secondary": "#FF9800",
                "bg_button_tertiary": "#2196F3",
                "fg_header": "#333333",
                "fg_label": "#333333",
                "fg_entry": "#333333",
                "fg_button": "#ffffff",
                "fg_result": "#333333",
                "border": "#dddddd",
                "insert": "#333333",
                "toggle_bg": "#cccccc",
                "toggle_active": "#4CAF50",
            },
            "dark": {
                "bg_main": "#121212",
                "bg_header": "#333333",
                "title_color": "#FFD700",  # Yellow/Mustard color
                "bg_form": "#1e1e1e",
                "bg_entry": "#333333",
                "bg_button_primary": "#388E3C",
                "bg_button_secondary": "#E65100",
                "bg_button_tertiary": "#0D47A1",
                "fg_header": "#ffffff",
                "fg_label": "#ffffff",
                "fg_entry": "#ffffff",
                "fg_button": "#ffffff",
                "fg_result": "#ffffff",
                "border": "#555555",
                "insert": "#ffffff",
                "toggle_bg": "#555555",
                "toggle_active": "#ffffff",
            },
        }

    def get_theme_color(self, key):
        theme = "dark" if self.dark_mode else "light"
        return self.themes[theme][key]

    def update_theme(self):
        theme = "dark" if self.dark_mode else "light"
        colors = self.themes[theme]

        # Update root
        self.app.root.config(bg=colors["bg_main"])

        # Update header
        self.app.header_frame.config(bg=colors["bg_header"])
        self.app.header_label.config(
            bg=colors["bg_header"], fg=colors["title_color"])

        # Update toggle button
        self.update_toggle_button()

        # Update form container
        self.app.form_container.config(bg=colors["bg_main"])
        self.app.form_frame.config(bg=colors["bg_form"])

        # Update form elements
        for widget in self.app.form_frame.winfo_children():
            if isinstance(widget, tk.Label):
                widget.config(bg=colors["bg_form"], fg=colors["fg_label"])
            elif isinstance(widget, tk.Frame):
                widget.config(bg=colors["bg_form"])
                for child in widget.winfo_children():
                    if isinstance(child, tk.Label):
                        child.config(bg=colors["bg_form"],
                                     fg=colors["fg_label"])
                    elif isinstance(child, tk.Entry):
                        child.config(
                            bg=colors["bg_entry"],
                            fg=(colors["fg_entry"] if child.cget(
                                "fg") != "#999999" else "#999999"),
                            insertbackground=colors["insert"],
                            highlightbackground=colors["border"],
                            highlightcolor=colors["border"],
                        )

        # Update buttons
        self.app.calculate_button.config(
            bg=colors["bg_button_primary"],
            fg=colors["fg_button"],
            activebackground=colors["bg_button_primary"],
            activeforeground=colors["fg_button"],
        )
        self.app.reset_button.config(
            bg=colors["bg_button_secondary"],
            fg=colors["fg_button"],
            activebackground=colors["bg_button_secondary"],
            activeforeground=colors["fg_button"],
        )
        self.app.save_button.config(
            bg=colors["bg_button_tertiary"],
            fg=colors["fg_button"],
            activebackground=colors["bg_button_tertiary"],
            activeforeground=colors["fg_button"],
        )

        # Update results container
        self.app.results_container.config(bg=colors["bg_main"])
        self.app.results_frame.config(bg=colors["bg_form"])

        # Update result widgets
        for widget in self.app.results_frame.winfo_children():
            if isinstance(widget, tk.Label):
                widget.config(bg=colors["bg_form"], fg=colors["fg_label"])
            elif isinstance(widget, tk.Frame):
                widget.config(bg=colors["bg_form"])
                for child in widget.winfo_children():
                    if isinstance(child, tk.Label):
                        child.config(bg=colors["bg_form"],
                                     fg=colors["fg_result"])

        # Update result frame
        self.app.result_frame.config(
            bg=colors["bg_form"], highlightbackground=colors["border"])

        # Update status bar
        self.app.status_bar.config(bg=colors["bg_main"], fg=colors["fg_label"])

        # Update history tab
        if hasattr(self.app, "history_tab"):
            for widget in self.app.history_tab.winfo_children():
                if isinstance(widget, tk.Frame):
                    widget.config(bg=colors["bg_form"])
                    for child in widget.winfo_children():
                        if isinstance(child, tk.Label):
                            child.config(
                                bg=colors["bg_form"], fg=colors["fg_label"])
                        elif isinstance(child, tk.Frame):
                            child.config(bg=colors["bg_form"])
                            for btn in child.winfo_children():
                                if isinstance(btn, tk.Button):
                                    btn.config(
                                        bg=colors["bg_button_tertiary"],
                                        fg=colors["fg_button"],
                                        activebackground=colors["bg_button_tertiary"],
                                        activeforeground=colors["fg_button"],
                                    )

        # Update matplotlib style for charts
        plt.style.use("default" if theme == "light" else "dark_background")

    def toggle_mode(self):
        self.dark_mode = not self.dark_mode
        self.update_theme()

    def update_toggle_button(self):
        toggle_color = self.get_theme_color("toggle_bg")
        active_color = self.get_theme_color("toggle_active")
        self.app.toggle_button.config(
            bg=toggle_color, activebackground=active_color)
