import csv
import os
from tkinter import messagebox, filedialog
from fpdf import FPDF
from utils import normalize_field_name


class FileManager:
    def __init__(self, app):
        self.app = app

    def save_to_csv(self):
        try:
            customer_name = self.app.entries[normalize_field_name(
                "Customer Name")].get().strip()
            gear_cost = self.app.get_float_value("Gear Rental Cost ($)", 0)
            travel_cost = self.app.get_float_value("Travel Expenses ($)", 0)
            hotel_cost = self.app.get_float_value("Hotel Expenses ($)", 0)
            payroll_cost = self.app.get_float_value("Payroll Costs ($)", 0)
            other_cost = self.app.get_float_value("Other Expenses ($)", 0)
            customer_payment = self.app.get_float_value(
                "Customer Payment ($)", 0)
            tax_rate = self.app.get_float_value("Tax Rate (%)", 0)
            discount = self.app.entries[normalize_field_name(
                "Discount")].get().strip()

            # Get results
            gross_text = self.app.result_gross_value.cget(
                "text").replace("$", "")
            net_text = self.app.result_net_value.cget("text").replace("$", "")
            margin_text = self.app.result_margin_value.cget(
                "text").replace("%", "")
            gross = float(gross_text) if gross_text else 0
            net = float(net_text) if net_text else 0
            margin = float(margin_text) if margin_text else 0

            # Get file path
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
            if not file_path:
                return

            # Save to CSV
            with open(file_path, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([
                    "Customer Name",
                    "Gear Rental",
                    "Travel",
                    "Hotel",
                    "Payroll",
                    "Other",
                    "Customer Payment",
                    "Tax Rate",
                    "Discount",
                    "Gross",
                    "Net",
                    "Margin %",
                ])
                writer.writerow([
                    customer_name,
                    gear_cost,
                    travel_cost,
                    hotel_cost,
                    payroll_cost,
                    other_cost,
                    customer_payment,
                    tax_rate,
                    discount,
                    gross,
                    net,
                    margin,
                ])

            # Update status
            self.app.status_bar.config(
                text=f"Data saved to {os.path.basename(file_path)}")
            messagebox.showinfo("Success", "Data saved successfully!")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")

    def export_to_pdf(self, history):
        """Export history to a PDF file."""
        if not history:
            messagebox.showwarning("Warning", "No history to export.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if not file_path:
            return

        try:
            # Create PDF with landscape orientation
            pdf = FPDF(orientation="L")  # Landscape mode
            pdf.add_page()
            # Use a smaller font size to fit more data
            pdf.set_font("Arial", size=11)

            # Add title
            pdf.cell(0, 10, txt="Calculation History", ln=True, align="C")

            # Define column widths (adjust as needed)
            # Wider columns for better readability
            col_widths = [40, 50, 50, 50, 40, 40]

            # Add table headers
            headers = ["Date", "Customer Name", "Customer Payment",
                       "Gross Expenses", "Net Profit", "Margin %"]
            for i, header in enumerate(headers):
                pdf.cell(col_widths[i], 10, txt=header, border=1)
            pdf.ln()

            # Add table rows
            for item in history:
                pdf.cell(col_widths[0], 10, txt=item["date"], border=1)
                pdf.cell(col_widths[1], 10,
                         txt=item["customer_name"], border=1)
                pdf.cell(col_widths[2], 10,
                         txt=f"${item['customer']:.2f}", border=1)
                pdf.cell(col_widths[3], 10,
                         txt=f"${item['gross']:.2f}", border=1)
                pdf.cell(col_widths[4], 10,
                         txt=f"${item['net']:.2f}", border=1)
                pdf.cell(col_widths[5], 10,
                         txt=f"{item['margin']:.1f}%", border=1)
                pdf.ln()

            # Save PDF
            pdf.output(file_path)
            messagebox.showinfo(
                "Success", "History exported to PDF successfully!")
            self.app.status_bar.config(
                text=f"History exported to {os.path.basename(file_path)}")
        except Exception as e:
            messagebox.showerror(
                "Error", f"Failed to export history: {str(e)}")
