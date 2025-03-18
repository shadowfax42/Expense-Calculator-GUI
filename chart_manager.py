import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk


class ChartManager:
    def __init__(self, app):
        self.app = app

    def update_charts(self, gear_cost, travel_cost, hotel_cost, payroll_cost, other_cost, gross, net):
        # Clear previous charts
        for widget in self.app.chart_frame.winfo_children():
            widget.destroy()

        # Determine chart colors based on theme
        if self.app.dark_mode:
            plt.style.use("dark_background")
            chart_bg_color = "#121212"  # Dark background
            text_color = "white"  # White text for dark mode
            bar_colors = ["#E57373", "#81C784"]  # Red and green for bars
        else:
            plt.style.use("default")
            chart_bg_color = "#ffffff"  # Light background
            text_color = "black"  # Black text for light mode
            bar_colors = ["#E57373", "#81C784"]  # Red and green for bars

        # Create frame for charts
        charts_row = tk.Frame(self.app.chart_frame)
        charts_row.pack(fill=tk.BOTH, expand=True)

        # Expenses breakdown chart
        expenses = [gear_cost, travel_cost,
                    hotel_cost, payroll_cost, other_cost]
        expense_labels = ["Gear", "Travel", "Hotel", "Payroll", "Other"]

        # Filter out zero values for cleaner pie chart
        filtered_expenses = []
        filtered_labels = []
        for amount, label in zip(expenses, expense_labels):
            if amount > 0:
                filtered_expenses.append(amount)
                filtered_labels.append(label)

        if sum(filtered_expenses) > 0:  # Only create pie chart if there are expenses
            # Set figure background
            fig1, ax1 = plt.subplots(figsize=(5, 4), facecolor=chart_bg_color)
            wedges, texts, autotexts = ax1.pie(
                filtered_expenses,
                labels=filtered_labels,
                autopct="%1.1f%%",
                startangle=90,
                shadow=False,
                textprops={"color": text_color},  # Set text color
            )

            # Enhance pie chart appearance
            ax1.set_title("Expense Breakdown", fontsize=12,
                          pad=20, color=text_color)
            plt.setp(autotexts, size=9, weight="bold", color=text_color)
            ax1.axis("equal")

            # Set axes background color
            ax1.set_facecolor(chart_bg_color)

            # Create canvas
            canvas1 = FigureCanvasTkAgg(fig1, master=charts_row)
            canvas1.draw()
            canvas1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Revenue vs Expenses bar chart
        # Set figure background
        fig2, ax2 = plt.subplots(figsize=(5, 4), facecolor=chart_bg_color)
        categories = ["Gross Expenses", "Net Profit"]
        values = [gross, net]

        # Create bars with colors based on profit/loss
        colors = [bar_colors[0], bar_colors[1] if net >= 0 else bar_colors[0]]
        ax2.bar(categories, values, color=colors)
        ax2.set_title("Profit Analysis", fontsize=12, pad=20, color=text_color)
        ax2.set_ylabel("Amount ($)", color=text_color)
        ax2.tick_params(axis="x", colors=text_color)
        ax2.tick_params(axis="y", colors=text_color)

        # Add value labels on bars
        for i, v in enumerate(values):
            ax2.text(
                i,
                v / 2,
                f"${v:.2f}",
                ha="center",
                va="center",
                fontweight="bold",
                color=text_color,
            )

        # Set axes background color
        ax2.set_facecolor(chart_bg_color)

        # Create canvas
        canvas2 = FigureCanvasTkAgg(fig2, master=charts_row)
        canvas2.draw()
        canvas2.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def clear_charts(self):
        for widget in self.app.chart_frame.winfo_children():
            widget.destroy()
