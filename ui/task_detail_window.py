import tkinter as tk
from tkinter import messagebox
from ui.custom_text_dialog import ask_formatted_string  # Ensure it's still imported

open_detail_windows = {}

def show_task_details(parent, manager, task_index, refresh_callback):
    task = manager.tasks[task_index]
    title = task["title"]

    key = f"{manager.filename}:{title}"
    if key in open_detail_windows and open_detail_windows[key].winfo_exists():
        open_detail_windows[key].destroy()
        del open_detail_windows[key]
        return

    detail_win = tk.Toplevel(parent)
    detail_win.title(title)

    x = parent.winfo_x()
    y = parent.winfo_y()
    detail_win.geometry(f"500x550+{x+100}+{y+100}")
    detail_win.transient(parent)
    detail_win.focus_force()
    detail_win.lift()
    detail_win.attributes("-topmost", True)
    detail_win.after(200, lambda: detail_win.attributes("-topmost", False))

    open_detail_windows[key] = detail_win

    tk.Label(detail_win, text=title, font=("Arial", 18)).pack(pady=10)

    details_listbox = tk.Listbox(
        detail_win,
        font=("Arial", 12),
        selectbackground="lightblue",
        activestyle="none",
        height=15,
    )
    details_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

    def refresh_details():
        details_listbox.delete(0, tk.END)
        for detail in task.get("details", []):
            details_listbox.insert(tk.END, f" • {detail}")

    def add_detail():
        new_detail = ask_formatted_string(detail_win, "New Detail")
        if new_detail:
            if "details" not in task:
                task["details"] = []
            task["details"].append(new_detail)
            manager.save()
            refresh_details()

    def edit_detail():
        selected = details_listbox.curselection()
        if selected:
            index = selected[0]
            current = task["details"][index]
            new = ask_formatted_string(detail_win, "Edit Detail", initial=current)
            if new:
                task["details"][index] = new
                manager.save()
                refresh_details()

    def delete_detail():
        selected = details_listbox.curselection()
        if selected:
            index = selected[0]
            if messagebox.askyesno("Delete", f"Delete this detail?", parent=detail_win):
                task["details"].pop(index)
                manager.save()
                refresh_details()

    button_frame = tk.Frame(detail_win)
    button_frame.pack(pady=10)

    tk.Button(
        button_frame, text="Add", bg="lightgreen", width=10, command=add_detail
    ).grid(row=0, column=0, padx=10)
    tk.Button(
        button_frame, text="Edit", bg="lightyellow", width=10, command=edit_detail
    ).grid(row=0, column=1, padx=10)
    tk.Button(
        button_frame, text="Delete", bg="lightcoral", width=10, command=delete_detail
    ).grid(row=0, column=2, padx=10)

    def on_close_detail():
        if key in open_detail_windows:
            del open_detail_windows[key]
        detail_win.destroy()
        refresh_callback()

    detail_win.protocol("WM_DELETE_WINDOW", on_close_detail)
    refresh_details()
