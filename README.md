# Profit Calculator GUI

The **Profit Calculator GUI** is a Python-based desktop application built with `tkinter` for calculating and visualizing profit margins based on various expenses and customer payments. It provides an intuitive interface for users to input expenses, calculate profits, and view historical data. The application also supports light and dark themes for better user experience.

---

## Story Behind the Project

My partner runs a small media company, and I noticed that he was using his phone calculator to prepare most of his quotes. I thought a dedicated desktop application could help streamline his workflow, making it easier to manage project costs and keep track of quotes for video and photo shoots. This application was designed to provide a more efficient and organized way to handle pricing and profitability calculations.

---

## Features

- **Expense Calculation**:
  - Input fields for customer name, gear rental cost, travel expenses, hotel expenses, payroll costs, other expenses, customer payment, tax rate, and discount.
  - Automatic calculation of gross expenses, net profit, and profit margin.

- **History Management**:
  - View and manage calculation history in a table format.
  - Save history entries to a CSV file.
  - Save history entries to a PDF file.
  - Clear all history entries with a single click.

- **Chart Visualization**:
  - **Pie Chart**: Breakdown of expenses (gear, travel, hotel, payroll, other).
  - **Bar Chart**: Comparison of gross expenses and net profit.

- **Themes**:
  - Toggle between **Light Mode** and **Dark Mode** using a switch in the header.

- **File Operations**:
  - Save the current calculation data to a CSV file.
  - Export the history to a PDF file.

---

## Requirements

To run this project, you need the following:

- **Python 3.x**
- **Libraries**:
  - `tkinter` (included with Python)
  - `matplotlib` (for chart visualization)
  - `csv` (for file operations)
  - `fpdf` (for PDF export)

---

## Running the Application

To create the executable file, use the following command:

```
python -m PyInstaller main.py --onefile -w --icon=images\zm.ico
```

The compiled version of the Tkinter application can be found in `dist/main.exe`. Simply double-click `main.exe` to launch the Profit Calculator GUI without needing to install Python or dependencies.

Sample output files can be found in the `output` folder.

