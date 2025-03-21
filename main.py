
import tkinter as tk
from dotenv import load_dotenv, find_dotenv
import os
from profit_calculator import ProfitCalculatorApp


load_dotenv(find_dotenv())

if __name__ == "__main__":
    root = tk.Tk()
    app = ProfitCalculatorApp(root)
    ICON_PATH = os.environ.get("ICON_PATH", "")
    root.iconbitmap(ICON_PATH)
    root.mainloop()
