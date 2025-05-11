import tkinter as tk
from ui.floating_button import create_floating_button

if __name__ == "__main__":
    root = tk.Tk()
    create_floating_button(root)
    root.mainloop()