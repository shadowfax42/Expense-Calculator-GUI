import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
from theme_manager import ThemeManager
from history_manager import HistoryManager
from file_manager import FileManager
from chart_manager import ChartManager
from utils import normalize_field_name


class ProfitCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Profit Calculator")
        self.root.geometry("900x800")
        self.root.minsize(800, 700)

        # Initialize managers
        self.theme_manager = ThemeManager(self)
        self.history_manager = HistoryManager(self)
        self.file_manager = FileManager(self)
        self.chart_manager = ChartManager(self)

        # App state
        self.dark_mode = False
        self.history = []

        # Store last calculation data for chart updates
        self.last_gear_cost = 0
        self.last_travel_cost = 0
        self.last_hotel_cost = 0
        self.last_payroll_cost = 0
        self.last_other_cost = 0
        self.last_gross = 0
        self.last_net = 0

        # Create UI elements
        self.create_widgets()
        self.theme_manager.update_theme()

    def create_widgets(self):
        # Main container with padding
        main_container = ttk.Frame(self.root, padding="20 20 20 20")
        main_container.pack(fill=tk.BOTH, expand=True)

        # Create header with logo and title
        self.header_frame = tk.Frame(main_container)
        self.header_frame.pack(fill=tk.X, pady=(0, 20))

        # App title with better font
        self.header_label = tk.Label(
            self.header_frame,
            text="Profit Calculator",
            font=("Helvetica", 22, "bold"),
            padx=15,
            pady=15,
        )
        self.header_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Mode toggle with a pill switch (slider)
        self.toggle_var = tk.BooleanVar(value=False)  # Default to light mode
        self.toggle_button = tk.Checkbutton(
            self.header_frame,
            text="Dark Mode",
            variable=self.toggle_var,
            onvalue=True,
            offvalue=False,
            command=self.theme_manager.toggle_mode,
            font=("Helvetica", 10),
            relief="flat",
            indicatoron=False,
            bg="#fff",
            fg="#000",
            selectcolor="#4CAF50",
            activebackground="#f5f5f5",
            activeforeground="#333333",
        )
        self.toggle_button.pack(side=tk.RIGHT, padx=10)

        # Create main content frame with tabs
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Tab 1: Calculator
        self.calculator_tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.calculator_tab, text="Calculator")

        # Tab 2: History
        self.history_tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.history_tab, text="History")

        # Setup calculator tab content
        self.setup_calculator_tab()

        # Setup history tab content
        self.history_manager.setup_history_tab()

        # Status bar
        self.status_bar = tk.Label(
            main_container,
            text="Ready",
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W,
            font=("Helvetica", 9),
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def setup_calculator_tab(self):
        # Split into left (form) and right (results) panes
        calculator_panes = tk.PanedWindow(
            self.calculator_tab, orient=tk.HORIZONTAL)
        calculator_panes.pack(fill=tk.BOTH, expand=True)

        # Left pane: Form container with border and rounded corners
        self.form_container = tk.Frame(calculator_panes, padx=10, pady=10)
        calculator_panes.add(self.form_container, width=400)

        # Create form with labels and entries
        self.form_frame = tk.Frame(self.form_container, padx=15, pady=15)
        self.form_frame.pack(fill=tk.BOTH, expand=True)

        # Form title
        form_title = tk.Label(
            self.form_frame,
            text="Enter Expense Details",
            font=("Helvetica", 14, "bold"),
        )
        form_title.grid(row=0, column=0, columnspan=2,
                        sticky="w", pady=(0, 15))

        # Input fields with better layout and visual cues for required fields
        self.fields = [
            {"name": "Customer Name", "required": True, "type": "text"},
            {"name": "Gear Rental Cost ($)",
             "required": True, "type": "float"},
            {"name": "Travel Expenses ($)",
             "required": False, "type": "float"},
            {"name": "Hotel Expenses ($)", "required": False, "type": "float"},
            {"name": "Payroll Costs ($)", "required": True, "type": "float"},
            {"name": "Other Expenses ($)", "required": False, "type": "float"},
            {"name": "Customer Payment ($)",
             "required": True, "type": "float"},
            {"name": "Tax Rate (%)", "required": False, "type": "float"},
            {"name": "Discount", "required": False,
                "type": "text", "placeholder": "e.g. 10% or $50"},
        ]

        self.entries = {}
        for idx, field in enumerate(self.fields):
            # Create frame for each field
            field_frame = tk.Frame(self.form_frame)
            field_frame.grid(row=idx + 1, column=0, sticky="ew", pady=8)

            # Label with asterisk for required fields
            label_text = field["name"] + (" *" if field["required"] else "")
            label = tk.Label(
                field_frame,
                text=label_text,
                font=("Helvetica", 10),
                anchor="w",
                width=20,
            )
            label.pack(side=tk.LEFT)

            # Entry with validation
            entry = tk.Entry(field_frame, font=(
                "Helvetica", 10), relief="solid", bd=1)
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=3)

            # Add placeholder text
            if "placeholder" in field:
                entry.insert(0, field["placeholder"])
                entry.config(fg="#999999")

                def on_focus_in(event, entry=entry, placeholder=field["placeholder"]):
                    if entry.get() == placeholder:
                        entry.delete(0, tk.END)
                        entry.config(
                            fg=self.theme_manager.get_theme_color("fg_entry"))

                def on_focus_out(event, entry=entry, placeholder=field["placeholder"]):
                    if entry.get() == "":
                        entry.insert(0, placeholder)
                        entry.config(fg="#999999")

                entry.bind("<FocusIn>", on_focus_in)
                entry.bind("<FocusOut>", on_focus_out)

            # Store entry reference
            self.entries[
                field["name"]
                .lower()
                .replace(" ", "_")
                .replace("($)", "")
                .replace("(%)", "")
            ] = entry

        # Buttons frame with improved layout
        button_frame = tk.Frame(self.form_frame)
        button_frame.grid(row=len(self.fields) + 1, column=0, pady=20)

        # Calculate button with icon
        self.calculate_button = tk.Button(
            button_frame,
            text="Calculate",
            command=self.calculate_profit,
            font=("Helvetica", 12, "bold"),
            width=12,
            relief="raised",
            padx=10,
        )
        self.calculate_button.pack(side=tk.LEFT, padx=5)

        # Reset button
        self.reset_button = tk.Button(
            button_frame,
            text="Reset",
            command=self.reset_fields,
            font=("Helvetica", 12),
            width=8,
            relief="raised",
        )
        self.reset_button.pack(side=tk.LEFT, padx=5)

        # Save button
        self.save_button = tk.Button(
            button_frame,
            text="Save",
            command=self.file_manager.save_to_csv,
            font=("Helvetica", 12),
            width=8,
            relief="raised",
        )
        self.save_button.pack(side=tk.LEFT, padx=5)

        # Right pane: Results and charts
        self.results_container = tk.Frame(calculator_panes)
        calculator_panes.add(self.results_container)

        # Results frame
        self.results_frame = tk.Frame(self.results_container, padx=15, pady=15)
        self.results_frame.pack(fill=tk.BOTH, expand=True)

        # Results title
        results_title = tk.Label(
            self.results_frame, text="Results", font=("Helvetica", 14, "bold")
        )
        results_title.pack(anchor="w", pady=(0, 15))

        # Results display
        self.result_frame = tk.Frame(
            self.results_frame, relief="ridge", bd=1, padx=15, pady=15
        )
        self.result_frame.pack(fill=tk.X)

        # Results with better layout
        self.result_gross_label = tk.Label(
            self.result_frame, text="Gross Expenses:", font=("Helvetica", 12)
        )
        self.result_gross_label.grid(row=0, column=0, sticky="w", pady=5)

        self.result_gross_value = tk.Label(
            self.result_frame, text="$0.00", font=("Helvetica", 12, "bold")
        )
        self.result_gross_value.grid(row=0, column=1, sticky="e", pady=5)

        self.result_net_label = tk.Label(
            self.result_frame, text="Net Profit:", font=("Helvetica", 12)
        )
        self.result_net_label.grid(row=1, column=0, sticky="w", pady=5)

        self.result_net_value = tk.Label(
            self.result_frame, text="$0.00", font=("Helvetica", 12, "bold")
        )
        self.result_net_value.grid(row=1, column=1, sticky="e", pady=5)

        self.result_margin_label = tk.Label(
            self.result_frame, text="Profit Margin:", font=("Helvetica", 12)
        )
        self.result_margin_label.grid(row=2, column=0, sticky="w", pady=5)

        self.result_margin_value = tk.Label(
            self.result_frame, text="0%", font=("Helvetica", 12, "bold")
        )
        self.result_margin_value.grid(row=2, column=1, sticky="e", pady=5)

        # Configure grid columns
        self.result_frame.grid_columnconfigure(0, weight=1)
        self.result_frame.grid_columnconfigure(1, weight=1)

        # Charts frame
        self.chart_frame = tk.Frame(self.results_frame)
        self.chart_frame.pack(fill=tk.BOTH, expand=True, pady=20)

    def calculate_profit(self):
        try:
            # Get values (handle required fields)
            customer_name = self.entries[normalize_field_name(
                "Customer Name")].get().strip()
            gear_cost = self.get_float_value("Gear Rental Cost ($)")
            payroll_cost = self.get_float_value("Payroll Costs ($)")
            customer_payment = self.get_float_value("Customer Payment ($)")

            # Check required fields
            if None in [customer_name, gear_cost, payroll_cost, customer_payment]:
                messagebox.showerror(
                    "Error", "Please fill in all required fields marked with *")
                return

            # Get optional values (default to 0)
            travel_cost = self.get_float_value("Travel Expenses ($)", 0)
            hotel_cost = self.get_float_value("Hotel Expenses ($)", 0)
            other_cost = self.get_float_value("Other Expenses ($)", 0)
            tax_rate = self.get_float_value(
                "Tax Rate (%)", 0) / 100  # Convert to decimal

            # Handle discount
            discount = 0
            discount_text = self.entries[normalize_field_name(
                "Discount")].get().strip()
            if discount_text and discount_text != "e.g. 10% or $50":
                if "%" in discount_text:
                    discount_percent = float(discount_text.replace("%", ""))
                    discount = (discount_percent / 100) * customer_payment
                elif "$" in discount_text:
                    discount = float(discount_text.replace("$", ""))
                else:
                    # Try to convert directly to float
                    discount = float(discount_text)

            # Calculate results
            subtotal = gear_cost + travel_cost + hotel_cost + payroll_cost + other_cost
            tax = subtotal * tax_rate
            gross = subtotal + tax - discount
            net = customer_payment - gross

            # Calculate margin percentage
            margin_percent = (net / customer_payment *
                              100) if customer_payment > 0 else 0

            # Update result display
            self.result_gross_value.config(text=f"${gross:.2f}")
            self.result_net_value.config(text=f"${net:.2f}")
            self.result_margin_value.config(text=f"{margin_percent:.1f}%")

            # Color-code net profit based on value
            if net > 0:
                self.result_net_value.config(fg="#388E3C")  # Green for profit
            elif net < 0:
                self.result_net_value.config(fg="#D32F2F")  # Red for loss
            else:
                self.result_net_value.config(
                    fg=self.theme_manager.get_theme_color("fg_result"))

            # Update charts
            self.chart_manager.update_charts(
                gear_cost, travel_cost, hotel_cost, payroll_cost, other_cost, gross, net
            )

            # Add to history
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
            history_item = {
                "date": current_time,
                "customer_name": customer_name,
                "customer": customer_payment,
                "gross": gross,
                "net": net,
                "margin": margin_percent,
            }
            self.history_manager.add_to_history(history_item)

            # Update status
            self.status_bar.config(
                text=f"Calculation completed: {current_time}")

        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")

    def reset_fields(self):
        # Clear all entries
        for field in self.fields:
            field_name = normalize_field_name(field["name"])
            entry = self.entries[field_name]
            entry.delete(0, tk.END)

            # Restore placeholder if applicable
            if "placeholder" in field:
                entry.insert(0, field["placeholder"])
                entry.config(fg="#999999")

        # Clear results
        self.result_gross_value.config(text="$0.00")
        self.result_net_value.config(
            text="$0.00", fg=self.theme_manager.get_theme_color("fg_result"))
        self.result_margin_value.config(text="0%")

        # Clear charts
        self.chart_manager.clear_charts()

        # Update status
        self.status_bar.config(text="Form reset")

    def get_float_value(self, field_name, default=None):
        """Get float value from entry or return default if empty"""
        normalized_field_name = normalize_field_name(field_name)
        if normalized_field_name not in self.entries:
            raise ValueError(f"Field '{field_name}' not found")

        value = self.entries[normalized_field_name].get().strip()
        field_def = None
        for field in self.fields:
            key = normalize_field_name(field["name"])
            if key == normalized_field_name:
                field_def = field
                break

        if field_def and "placeholder" in field_def and value == field_def["placeholder"]:
            return default

        if not value:
            return default

        try:
            return float(value)
        except ValueError:
            raise ValueError(
                f"Invalid number in {field_name.replace('_', ' ').title()}")
