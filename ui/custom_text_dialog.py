import tkinter as tk
from tkinter import simpledialog

class CustomTextDialog(simpledialog.Dialog):
    def __init__(self, parent, title, initial_value=""):
        self.initial_value = initial_value
        self.result = None
        super().__init__(parent, title)

    def body(self, master):
        self.text = tk.Text(master, wrap=tk.WORD, font=("Arial", 12), height=6, width=40)
        self.text.pack(padx=10, pady=(10, 5))
        self.text.insert(tk.END, self.initial_value)

        bar = tk.Frame(master)
        bar.pack(pady=5)

        tk.Button(bar, text="Bold", command=self.make_bold).pack(side=tk.LEFT, padx=5)
        tk.Button(bar, text="Underline", command=self.make_underline).pack(side=tk.LEFT, padx=5)

        self.text.tag_configure("bold", font=("Arial", 12, "bold"))
        self.text.tag_configure("underline", font=("Arial", 12, "underline"))
        return self.text

    def make_bold(self):
        try:
            start, end = self.text.tag_ranges(tk.SEL)
            self.text.tag_add("bold", start, end)
        except:
            pass

    def make_underline(self):
        try:
            start, end = self.text.tag_ranges(tk.SEL)
            self.text.tag_add("underline", start, end)
        except:
            pass

    def apply(self):
        self.result = self.text.get("1.0", tk.END).strip()

def ask_formatted_string(parent, title, initial=""):
    dialog = CustomTextDialog(parent, title, initial)
    return dialog.result
