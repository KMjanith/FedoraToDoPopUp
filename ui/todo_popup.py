import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
from data.storage import TaskManager
from ui.custom_text_dialog import ask_formatted_string
from ui.task_detail_window import show_task_details


is_popup_open = False
popup_window = None


def show_todo_popup(root):
    global is_popup_open, popup_window

    if is_popup_open:
        popup_window.destroy()
        is_popup_open = False
        return

    is_popup_open = True
    popup_window = tk.Toplevel()
    popup_window.title("To-Do List")
    x = root.winfo_x()
    y = root.winfo_y()
    popup_window.geometry(f"800x500+{x+60}+{y}")
    popup_window.wm_attributes("-topmost", 1)

    outer_frame = tk.Frame(popup_window, bg="#f8f8f8")
    outer_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    notebook = ttk.Notebook(outer_frame)
    notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    managers = {
        "Tasks": TaskManager("tasks.json"),
        "Diary": TaskManager("Diary.json"),
        "Password/Tokens": TaskManager("passwords.json"),
    }

    for tab_name, manager in managers.items():
        frame = tk.Frame(notebook)
        notebook.add(frame, text=tab_name)

        listbox = tk.Listbox(
            frame,
            font=("Arial", 12),
            selectbackground="lightblue",
            activestyle="none",
            height=15,
        )
        listbox.pack(fill=tk.BOTH, expand=True, pady=(10, 10), padx=10)

        def make_refresh(mgr=manager, lb=listbox):
            def refresh():
                lb.delete(0, tk.END)
                for task in mgr.tasks:
                    lb.insert(tk.END, f"• {task['title']}")

            return refresh

        refresh_list = make_refresh()

        def add_task(mgr=manager, refresh=refresh_list):
            title = ask_formatted_string(popup_window, "New Task")
            if title:
                mgr.add_task(title)
                refresh()

        def edit_task(mgr=manager, refresh=refresh_list, lb=listbox):
            selected = lb.curselection()
            if selected:
                index = selected[0]
                task = mgr.tasks[index]  # Get the selected task

                # Prompt for new title with the current task title as the initial value
                new_title = ask_formatted_string(
                    popup_window,
                    f"Edit Task (Current: {task['title']})",
                    initial=task["title"],  # Pass 'initial' instead of 'initialvalue'
                )

                if new_title:  # If the user provided a new title
                    mgr.edit_task(index, new_title)  # Update the task title
                    refresh()  # Refresh the list


        def delete_task(mgr=manager, refresh=refresh_list, lb=listbox):
            selected = lb.curselection()
            if selected:
                index = selected[0]
                title = mgr.tasks[index]["title"]
                if messagebox.askyesno(
                    "Delete", f"Delete '{title}'?", parent=popup_window
                ):
                    mgr.delete_task(index)
                    refresh()

        def open_details(event, mgr=manager, lb=listbox, refresh=refresh_list):
            selected = lb.curselection()
            if selected:
                index = selected[0]
                show_task_details(popup_window, mgr, index, refresh)

        listbox.bind("<Double-1>", open_details)

        btn_frame = tk.Frame(frame)
        btn_frame.pack(pady=5)

        tk.Button(
            btn_frame, text="Add", bg="#c1f0c1", font=("Arial", 11), command=add_task
        ).grid(row=0, column=0, padx=10)
        tk.Button(
            btn_frame, text="Edit", bg="#ffffc1", font=("Arial", 11), command=edit_task
        ).grid(row=0, column=1, padx=10)
        tk.Button(
            btn_frame,
            text="Delete",
            bg="#f0c1c1",
            font=("Arial", 11),
            command=delete_task,
        ).grid(row=0, column=2, padx=10)

        refresh_list()

    def on_close():
        global is_popup_open
        is_popup_open = False
        popup_window.destroy()

    popup_window.protocol("WM_DELETE_WINDOW", on_close)
