import tkinter as tk
from ui.todo_popup import show_todo_popup

def create_floating_button(root):
    root.overrideredirect(True)
    root.geometry("50x50+100+100")
    root.wm_attributes("-topmost", 1)

    canvas = tk.Canvas(root, width=50, height=50, highlightthickness=0, bg="white")
    canvas.pack()
    canvas.create_oval(5, 5, 45, 45, fill="dodgerblue", outline="")
    canvas.create_oval(8, 8, 42, 42, outline="yellow", width=2)
    canvas.create_text(25, 25, text="DO", fill="white", font=("Arial", 10, "bold"))

    def on_click(event):
        show_todo_popup(root)

    def start_move(event):
        root.x = event.x
        root.y = event.y

    def do_move(event):
        root.geometry(f"+{event.x_root - root.x}+{event.y_root - root.y}")

    canvas.bind("<Button-1>", on_click)
    canvas.bind("<ButtonPress-3>", start_move)
    canvas.bind("<B3-Motion>", do_move)
