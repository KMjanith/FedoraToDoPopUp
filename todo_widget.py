# import tkinter as tk
# from tkinter import simpledialog, messagebox
# import json
# import os
# from tkinter import ttk

# # --- File persistence ---
# DATA_FILE = "tasks.json"
# open_detail_windows = {}  # Track open subtask windows by task title


# def load_tasks():
#     if os.path.exists(DATA_FILE):
#         with open(DATA_FILE, "r") as f:
#             return json.load(f)
#     return []


# def save_tasks():
#     with open(DATA_FILE, "w") as f:
#         json.dump(tasks, f, indent=2)


# # --- App State ---
# tasks = load_tasks()
# is_popup_open = False
# popup_window = None


# # --- Show Task Detail Window ---
# def show_task_details(task, refresh_callback):
#     title = task["title"]

#     if title in open_detail_windows and open_detail_windows[title].winfo_exists():
#         open_detail_windows[title].destroy()
#         del open_detail_windows[title]
#         return
    
#     detail_win = tk.Toplevel(popup_window)
#     detail_win.title(title)

#     # Position and force on top of popup
#     x = popup_window.winfo_x()
#     y = popup_window.winfo_y()
#     detail_win.geometry(f"400x400+{x+100}+{y+100}")
#     # detail_win.lift()
#     # detail_win.attributes("-topmost", 1)
#     # detail_win.after(100, lambda: detail_win.attributes("-topmost", 1))
    
#     # Make it act like a child window of popup_window
#     detail_win.transient(popup_window)
#     detail_win.focus_force()  # politely ask for focus

#     # Briefly raise it, then remove topmost to avoid OS notifications
#     detail_win.lift()
#     detail_win.attributes("-topmost", True)
#     detail_win.after(200, lambda: detail_win.attributes("-topmost", False))

#     open_detail_windows[title] = detail_win

#     tk.Label(detail_win, text=task["title"], font=("Arial", 18, "bold")).pack(pady=10)
#     details_listbox = tk.Listbox(detail_win, font=("Arial", 12))
#     details_listbox.pack(fill=tk.BOTH, expand=True, padx=10)

#     def refresh_details():
#         details_listbox.delete(0, tk.END)
#         for detail in task["details"]:
#             details_listbox.insert(tk.END, detail)

#     def add_detail():
#         new_detail = simpledialog.askstring("New Detail", "Enter detail:")
#         if new_detail:
#             task["details"].append(new_detail)
#             save_tasks()
#             refresh_details()

#     def edit_detail():
#         selected = details_listbox.curselection()
#         if selected:
#             index = selected[0]
#             current = task["details"][index]
#             new = simpledialog.askstring("Edit Detail", "Edit:", initialvalue=current)
#             if new:
#                 task["details"][index] = new
#                 save_tasks()
#                 refresh_details()

#     def delete_detail():
#         selected = details_listbox.curselection()
#         if selected:
#             index = selected[0]
#             task["details"].pop(index)
#             save_tasks()
#             refresh_details()

#     button_frame = tk.Frame(detail_win)
#     button_frame.pack(pady=10)

#     tk.Button(button_frame, text="Add", bg="lightgreen", command=add_detail).grid(
#         row=0, column=0, padx=10, pady=5
#     )
#     tk.Button(button_frame, text="Edit", bg="lightyellow", command=edit_detail).grid(
#         row=0, column=1, padx=10, pady=5
#     )
#     tk.Button(button_frame, text="Delete", bg="lightcoral", command=delete_detail).grid(
#         row=0, column=2, padx=10, pady=5
#     )

#     def on_close_detail():
#         if title in open_detail_windows:
#             del open_detail_windows[title]
#         detail_win.destroy()
#         refresh_callback()

#     detail_win.protocol("WM_DELETE_WINDOW", on_close_detail)
#     refresh_details()


# # --- Show To-Do List Popup ---
# def show_todo_popup():
#     global is_popup_open, popup_window

#     if is_popup_open:
#         popup_window.destroy()
#         is_popup_open = False
#         return

#     is_popup_open = True
#     popup_window = tk.Toplevel()
#     popup_window.title("To-Do List")
#     x = root.winfo_x()
#     y = root.winfo_y()
#     popup_window.geometry(f"800x500+{x+60}+{y}")
#     popup_window.wm_attributes("-topmost", 1)

#     outer_frame = tk.Frame(popup_window, bg="#f8f8f8")
#     outer_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

#     notebook = ttk.Notebook(outer_frame)
#     notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

#     # Tab 1: To-Do List
#     todo_frame = tk.Frame(notebook)
#     notebook.add(todo_frame, text="Tasks")

#     listbox = tk.Listbox(
#         todo_frame,
#         font=("Arial", 12),
#         selectbackground="lightblue",
#         activestyle="none",
#         height=15,
#     )
#     listbox.pack(fill=tk.BOTH, expand=True, pady=(10, 10), padx=10)

#     def refresh_list():
#         listbox.delete(0, tk.END)
#         for task in tasks:
#             listbox.insert(
#                 tk.END, f"• {task['title']}"
#             )  # Add bullet for better appearance

#     def add_task():
#         title = simpledialog.askstring("New Task", "Enter task title:")
#         if title:
#             tasks.append({"title": title, "details": []})
#             save_tasks()
#             refresh_list()

#     def edit_task():
#         selected = listbox.curselection()
#         if selected:
#             index = selected[0]
#             new_title = simpledialog.askstring(
#                 "Edit Task", "New title:", initialvalue=tasks[index]["title"]
#             )
#             if new_title:
#                 tasks[index]["title"] = new_title
#                 save_tasks()
#                 refresh_list()

#     def delete_task():
#         selected = listbox.curselection()
#         if selected:
#             index = selected[0]
#             title = tasks[index]["title"]
#             if title in open_detail_windows:
#                 open_detail_windows[title].destroy()
#                 del open_detail_windows[title]
#             if messagebox.askyesno("Delete", f"Delete '{title}'?"):
#                 tasks.pop(index)
#                 save_tasks()
#                 refresh_list()

#     def open_task_details(event):
#         selected = listbox.curselection()
#         if selected:
#             index = selected[0]
#             show_task_details(tasks[index], refresh_list)

#     listbox.bind("<Double-1>", open_task_details)

#     btn_frame = tk.Frame(todo_frame)
#     btn_frame.pack(pady=5)

#     tk.Button(
#         btn_frame, text="Add", bg="#c1f0c1", font=("Arial", 11), command=add_task
#     ).grid(row=0, column=0, padx=10)
#     tk.Button(
#         btn_frame, text="Edit", bg="#ffffc1", font=("Arial", 11), command=edit_task
#     ).grid(row=0, column=1, padx=10)
#     tk.Button(
#         btn_frame,
#         text="Delete",
#         bg="#f0c1c1",
#         font=("Arial", 11),
#         command=delete_task,
#     ).grid(row=0, column=2, padx=10)

#     # Tab 2: Completed
#     completed_frame = tk.Frame(notebook)
#     notebook.add(completed_frame, text="Completed")
#     tk.Label(
#         completed_frame, text="Completed tasks will be shown here.", font=("Arial", 14)
#     ).pack(pady=20)

#     # Tab 3: Settings
#     settings_frame = tk.Frame(notebook)
#     notebook.add(settings_frame, text="Settings")
#     tk.Label(settings_frame, text="Settings Page", font=("Arial", 14)).pack(pady=20)

#     def on_close():
#         global is_popup_open
#         is_popup_open = False
#         popup_window.destroy()

#     popup_window.protocol("WM_DELETE_WINDOW", on_close)
#     refresh_list()

# # --- Floating Button ---
# root = tk.Tk()
# root.overrideredirect(True)
# root.geometry("50x50+100+100")
# root.wm_attributes("-topmost", 1)

# canvas = tk.Canvas(root, width=50, height=50, highlightthickness=0, bg="white")
# canvas.pack()
# canvas.create_oval(5, 5, 45, 45, fill="dodgerblue", outline="")         # Outer circle
# canvas.create_oval(8, 8, 42, 42, outline="yellow", width=2)          # Inner circle
# canvas.create_text(25, 25, text="DO", fill="white", font=("Arial", 10, "bold"))


# def on_click(event):
#     show_todo_popup()


# def start_move(event):
#     root.x = event.x
#     root.y = event.y


# def do_move(event):
#     root.geometry(f"+{event.x_root - root.x}+{event.y_root - root.y}")


# canvas.bind("<Button-1>", on_click)
# canvas.bind("<ButtonPress-3>", start_move)
# canvas.bind("<B3-Motion>", do_move)

# root.mainloop()
