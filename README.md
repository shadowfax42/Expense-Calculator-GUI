# Profit Calculator GUI

The **Profit Calculator GUI** is a Python-based application built with `tkinter` for calculating and visualizing profit margins based on various expenses and customer payments. It includes features like expense tracking, profit calculation, history management, and chart visualization. The application also supports light and dark themes for better user experience.

---

## Features

- **Expense Calculation**:
  - Input fields for customer name, gear rental cost, travel expenses, hotel expenses, payroll costs, other expenses, customer payment, tax rate, and discount.
  - Automatic calculation of gross expenses, net profit, and profit margin.

- **History Management**:
  - View and manage calculation history.
  - Export history to a CSV file.
  - Clear history with a single click.

- **Chart Visualization**:
  - Pie chart for expense breakdown.
  - Bar chart for gross expenses vs. net profit.

- **Themes**:
  - Toggle between light and dark modes.

- **File Operations**:
  - Save current calculation data to a CSV file.

---

## Requirements

To run this project, you need the following:

- Python 3.x
- Libraries:
  - `tkinter` (included with Python)
  - `matplotlib` (for chart visualization)
  - `csv` (for file operations)


## File Structure

profit-calculator-gui/
├── main.py                # Entry point of the application
├── profit_calculator.py   # Main application logic
├── theme_manager.py       # Handles theme-related functionality
├── history_manager.py     # Manages history-related functionality
├── file_manager.py        # Handles file operations
├── chart_manager.py       # Manages chart creation and updates
├── README.md              # Project documentation
├── screenshots/           # Folder for application screenshots
│   ├── light_mode.png     # Screenshot of the app in light mode
│   └── dark_mode.png      # Screenshot of the app in dark mode