import tkinter as tk
from tkinter import simpledialog, messagebox
import json
import os

# --- File persistence ---
DATA_FILE = "tasks.json"
open_detail_windows = {}  # Track open subtask windows by task title


def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks():
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

# --- App State ---
tasks = load_tasks()
is_popup_open = False
popup_window = None

# --- Show Task Detail Window ---
def show_task_details(task, refresh_callback):
    title = task["title"]

    # Toggle: If already open, close it
    if title in open_detail_windows and open_detail_windows[title].winfo_exists():
        open_detail_windows[title].destroy()
        del open_detail_windows[title]
        return

    detail_win = tk.Toplevel()
    detail_win.title(title)
    detail_win.geometry("400x400")
    open_detail_windows[title] = detail_win

    tk.Label(detail_win, text=task["title"], font=("Arial", 18, "bold")).pack(pady=10)
    details_listbox = tk.Listbox(detail_win, font=("Arial", 12))
    details_listbox.pack(fill=tk.BOTH, expand=True)

    def refresh_details():
        details_listbox.delete(0, tk.END)
        for detail in task["details"]:
            details_listbox.insert(tk.END, detail)

    def add_detail():
        new_detail = simpledialog.askstring("New Detail", "Enter detail:")
        if new_detail:
            task["details"].append(new_detail)
            save_tasks()
            refresh_details()

    def edit_detail():
        selected = details_listbox.curselection()
        if selected:
            index = selected[0]
            current = task["details"][index]
            new = simpledialog.askstring("Edit Detail", "Edit:", initialvalue=current)
            if new:
                task["details"][index] = new
                save_tasks()
                refresh_details()

    def delete_detail():
        selected = details_listbox.curselection()
        if selected:
            index = selected[0]
            task["details"].pop(index)
            save_tasks()
            refresh_details()

    button_frame = tk.Frame(detail_win)
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="➕", font=("Arial", 14), bg="lightgreen", command=add_detail).grid(row=0, column=0, padx=10)
    tk.Button(button_frame, text="✏️", font=("Arial", 14), bg="lightyellow", command=edit_detail).grid(row=0, column=1, padx=10)
    tk.Button(button_frame, text="❌", font=("Arial", 14), bg="lightcoral", command=delete_detail).grid(row=0, column=2, padx=10)

    def on_close_detail():
        if title in open_detail_windows:
            del open_detail_windows[title]
        detail_win.destroy()
        refresh_callback()

    detail_win.protocol("WM_DELETE_WINDOW", on_close_detail)
    refresh_details()

# --- Show To-Do List Popup ---
def show_todo_popup():
    global is_popup_open, popup_window

    if is_popup_open:
        popup_window.destroy()
        is_popup_open = False
        return

    is_popup_open = True
    popup_window = tk.Toplevel()
    popup_window.title("To-Do List")
    popup_window.geometry("600x400")

    frame = tk.Frame(popup_window)
    frame.pack(fill=tk.BOTH, expand=True)

    listbox = tk.Listbox(frame, font=("Arial", 12))
    listbox.pack(fill=tk.BOTH, expand=True)

    def refresh_list():
        listbox.delete(0, tk.END)
        for task in tasks:
            listbox.insert(tk.END, task["title"])

    def add_task():
        title = simpledialog.askstring("New Task", "Enter task title:")
        if title:
            tasks.append({"title": title, "details": []})
            save_tasks()
            refresh_list()

    def edit_task():
        selected = listbox.curselection()
        if selected:
            index = selected[0]
            current_title = tasks[index]["title"]
            new_title = simpledialog.askstring("Edit Task", "New title:", initialvalue=current_title)
            if new_title:
                tasks[index]["title"] = new_title
                save_tasks()
                refresh_list()

    def delete_task():
        selected = listbox.curselection()
        if selected:
            index = selected[0]
            task_title = tasks[index]["title"]
            if task_title in open_detail_windows:
                open_detail_windows[task_title].destroy()
                del open_detail_windows[task_title]
            if messagebox.askyesno("Delete", f"Delete '{task_title}'?"):
                tasks.pop(index)
                save_tasks()
                refresh_list()

    def open_task_details(event):
        selected = listbox.curselection()
        if selected:
            index = selected[0]
            show_task_details(tasks[index], refresh_list)

    listbox.bind("<Double-1>", open_task_details)

    tk.Button(popup_window, text="➕ Add", command=add_task).pack(fill=tk.X)
    tk.Button(popup_window, text="✏️ Edit", command=edit_task).pack(fill=tk.X)
    tk.Button(popup_window, text="❌ Delete", command=delete_task).pack(fill=tk.X)

    def on_close():
        global is_popup_open
        is_popup_open = False
        popup_window.destroy()

    popup_window.protocol("WM_DELETE_WINDOW", on_close)
    refresh_list()

# --- Floating Button ---
root = tk.Tk()
root.overrideredirect(True)
root.geometry("50x50+100+100")
root.wm_attributes("-topmost", 1)

canvas = tk.Canvas(root, width=50, height=50, highlightthickness=0, bg='white')
canvas.pack()
canvas.create_oval(5, 5, 45, 45, fill="dodgerblue", outline="")
canvas.create_text(25, 25, text="📋", fill="white", font=("Arial", 16))

def on_click(event): show_todo_popup()
def start_move(event): root.x = event.x; root.y = event.y
def do_move(event): root.geometry(f"+{event.x_root - root.x}+{event.y_root - root.y}")

canvas.bind("<Button-1>", on_click)
canvas.bind("<ButtonPress-3>", start_move)
canvas.bind("<B3-Motion>", do_move)

root.mainloop()
