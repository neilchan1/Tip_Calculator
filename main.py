import tkinter as tk
from gui import TipCalculatorApp

def exit():
    root_window.destroy()

if __name__ == "__main__":
    root_window = tk.Tk()
    app = TipCalculatorApp(root_window)
    root_window.protocol("WM_DELETE_WINDOW_", exit)
    root_window.mainloop()