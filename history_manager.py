import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import csv
import os
from fpdf import FPDF


class HistoryManager:
    def __init__(self, app):
        self.app = app
        self.history = []

    def setup_history_tab(self):
        # History view
        history_frame = tk.Frame(self.app.history_tab, padx=10, pady=10)
        history_frame.pack(fill=tk.BOTH, expand=True)

        # History title
        history_title = tk.Label(
            history_frame,
            text="Calculation History",
            font=("Helvetica", 14, "bold"),
        )
        history_title.pack(anchor="w", pady=(0, 15))

        # Create treeview for history
        columns = ("date", "customer_name", "customer",
                   "gross", "net", "margin")
        self.history_tree = ttk.Treeview(
            history_frame,
            columns=columns,
            show="headings",
            style="Custom.Treeview"  # Use a custom style for dark mode
        )

        # Define headings
        self.history_tree.heading("date", text="Date")
        self.history_tree.heading("customer_name", text="Customer Name")
        self.history_tree.heading("customer", text="Customer Payment")
        self.history_tree.heading("gross", text="Gross Expenses")
        self.history_tree.heading("net", text="Net Profit")
        self.history_tree.heading("margin", text="Margin %")

        # Define columns
        self.history_tree.column("date", width=150)
        self.history_tree.column("customer_name", width=150)
        self.history_tree.column("customer", width=150)
        self.history_tree.column("gross", width=150)
        self.history_tree.column("net", width=150)
        self.history_tree.column("margin", width=100)

        # Create scrollbar
        history_scroll = ttk.Scrollbar(
            history_frame,
            orient="vertical",
            command=self.history_tree.yview
        )
        self.history_tree.configure(yscrollcommand=history_scroll.set)

        # Pack tree and scrollbar
        self.history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        history_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Action buttons
        history_buttons = tk.Frame(history_frame)
        history_buttons.pack(fill=tk.X, pady=10)

        export_btn = tk.Button(
            history_buttons,
            text="Export to CSV",
            command=self.export_history,
            font=("Helvetica", 10),
        )
        export_btn.pack(side=tk.RIGHT, padx=5)

        export_pdf_btn = tk.Button(
            history_buttons,
            text="Export to PDF",
            command=self.export_to_pdf,
            font=("Helvetica", 10),
        )
        export_pdf_btn.pack(side=tk.RIGHT, padx=5)

        clear_btn = tk.Button(
            history_buttons,
            text="Clear History",
            command=self.clear_history,
            font=("Helvetica", 10),
        )
        clear_btn.pack(side=tk.RIGHT, padx=5)

        # Apply dark mode styling if enabled
        self.update_history_theme()

    def add_to_history(self, item):
        self.history.append(item)
        self.update_history_view()

    def export_history(self):
        if not self.history:
            messagebox.showwarning("Warning", "No history to export.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            return

        try:
            with open(file_path, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Date", "Customer Name", "Customer Payment",
                                "Gross Expenses", "Net Profit", "Margin %"])
                for item in self.history:
                    writer.writerow([
                        item["date"],
                        item["customer_name"],
                        f"${item['customer']:.2f}",
                        f"${item['gross']:.2f}",
                        f"${item['net']:.2f}",
                        f"{item['margin']:.1f}%",
                    ])
            messagebox.showinfo("Success", "History exported successfully!")
            self.app.status_bar.config(
                text=f"History exported to {os.path.basename(file_path)}")
        except Exception as e:
            messagebox.showerror(
                "Error", f"Failed to export history: {str(e)}")

    def export_to_pdf(self):
        """Export history to a PDF file."""
        if not self.history:
            messagebox.showwarning("Warning", "No history to export.")
            return

        # Pass the history data to the FileManager
        self.app.file_manager.export_to_pdf(self.history)

    def clear_history(self):
        if not self.history:
            messagebox.showwarning("Warning", "No history to clear.")
            return

        if messagebox.askyesno("Confirm", "Are you sure you want to clear all history?"):
            self.history.clear()
            self.update_history_view()
            self.app.status_bar.config(text="History cleared")
            messagebox.showinfo("Success", "Calculation history cleared.")

    def update_history_view(self):
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)

        for item in self.history:
            self.history_tree.insert("", "end", values=(
                item["date"],
                item["customer_name"],
                f"${item['customer']:.2f}",
                f"${item['gross']:.2f}",
                f"${item['net']:.2f}",
                f"{item['margin']:.1f}%",
            ))

        self.app.status_bar.config(
            text=f"History updated ({len(self.history)} records)")

    def update_history_theme(self):
        if self.app.dark_mode:
            # Dark mode colors
            bg_color = "#121212"
            fg_color = "white"
            self.history_tree.configure(style="Custom.Treeview")
            style = ttk.Style()
            style.configure("Custom.Treeview",
                            background=bg_color,
                            foreground=fg_color,
                            fieldbackground=bg_color)
            style.map("Custom.Treeview",
                      background=[("selected", "#333333")],
                      foreground=[("selected", "white")])
        else:
            # Light mode colors
            bg_color = "white"
            fg_color = "black"
            self.history_tree.configure(style="Custom.Treeview")
            style = ttk.Style()
            style.configure("Custom.Treeview",
                            background=bg_color,
                            foreground=fg_color,
                            fieldbackground=bg_color)
            style.map("Custom.Treeview",
                      background=[("selected", "#f0f0f0")],
                      foreground=[("selected", "black")])
