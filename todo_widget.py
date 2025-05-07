import tkinter as tk
from tkinter import simpledialog, messagebox

# --- Todo list data ---
tasks = []

# Flag to track if the popup is already open
is_popup_open = False
popup_window = None  # To store the reference of the popup window

# --- Function to show To-Do list popup ---
def show_todo_popup():
    global is_popup_open, popup_window  # Use the global flag and reference

    if is_popup_open:  # If the popup is already open, close it
        popup_window.destroy()
        is_popup_open = False
        return

    is_popup_open = True  # Set the flag to True indicating popup is open

    popup_window = tk.Toplevel()  # Create the popup window
    popup_window.title("To-Do List")
    popup_window.geometry("600x400")

    listbox = tk.Listbox(popup_window)
    listbox.pack(fill=tk.BOTH, expand=True)

    # Add tasks to listbox (display task title as a button)
    for task in tasks:
        listbox.insert(tk.END, task['title'])

    def add_task():
        task_title = simpledialog.askstring("Add Task", "Enter a new task:")
        if task_title:
            new_task = {"title": task_title, "details": []}
            tasks.append(new_task)
            listbox.insert(tk.END, task_title)

    def delete_task():
        selected = listbox.curselection()
        if selected:
            task_title = listbox.get(selected[0])
            task_to_delete = next((task for task in tasks if task["title"] == task_title), None)
            if task_to_delete:
                tasks.remove(task_to_delete)
                listbox.delete(selected[0])

    def edit_task():
        selected = listbox.curselection()
        if selected:
            current_title = listbox.get(selected[0])
            new_title = simpledialog.askstring("Edit Task", "Edit your task:", initialvalue=current_title)
            if new_title:
                task_to_edit = next((task for task in tasks if task["title"] == current_title), None)
                if task_to_edit:
                    task_to_edit["title"] = new_title
                    listbox.delete(selected[0])
                    listbox.insert(selected[0], new_title)

    def open_task_details(event):
        selected = listbox.curselection()
        if selected:
            task_title = listbox.get(selected[0])
            task_to_open = next((task for task in tasks if task["title"] == task_title), None)
            if task_to_open:
                show_task_details(task_to_open)

    # Add task edit/delete buttons with sticker icons (representing icons as text for simplicity)
    tk.Button(popup_window, text="Add", command=add_task).pack(fill=tk.X)
    tk.Button(popup_window, text="Edit", command=edit_task).pack(fill=tk.X)
    tk.Button(popup_window, text="Delete", command=delete_task).pack(fill=tk.X)

    listbox.bind("<Button-1>", open_task_details)

    # When popup is closed, reset the flag
    def on_close():
        global is_popup_open
        is_popup_open = False
        popup_window.destroy()

    popup_window.protocol("WM_DELETE_WINDOW", on_close)  # Ensure flag is reset when popup is closed


# --- Function to show task details ---
def show_task_details(task):
    detail_window = tk.Toplevel()
    detail_window.title(task['title'])
    detail_window.geometry("400x400")

    # Title of the task
    tk.Label(detail_window, text=task['title'], font=("Arial", 18, "bold")).pack(pady=10)

    # Listbox to show details (point-wise tasks)
    details_listbox = tk.Listbox(detail_window, height=10)
    details_listbox.pack(fill=tk.BOTH, expand=True)

    # Add current details if any
    for detail in task['details']:
        details_listbox.insert(tk.END, detail)

    # Function to add details
    def add_detail():
        detail = simpledialog.askstring("Add Detail", "Enter the detail:")
        if detail:
            task['details'].append(detail)
            details_listbox.insert(tk.END, detail)

    # Adding "Add Detail" button with sticker-like icon (text used for simplicity)
    add_detail_button = tk.Label(detail_window, text="➕ Add Detail", font=("Arial", 14), bg="green", width=15, height=2)
    add_detail_button.pack(pady=10)

    def on_delete_task():
        task_index = tasks.index(task)
        if task_index != -1:
            tasks.pop(task_index)
            detail_window.destroy()

    def on_edit_task():
        new_title = simpledialog.askstring("Edit Task", "Enter new task title:", initialvalue=task['title'])
        if new_title:
            task['title'] = new_title
            detail_window.title(new_title)

    # Adding edit and delete buttons with sticker-like icons (represented as text for simplicity)
    delete_button = tk.Label(detail_window, text="❌ Delete", font=("Arial", 14), bg="red", width=10, height=2)
    delete_button.pack(side=tk.LEFT, padx=20, pady=10)

    edit_button = tk.Label(detail_window, text="✏️ Edit", font=("Arial", 14), bg="yellow", width=10, height=2)
    edit_button.pack(side=tk.RIGHT, padx=20, pady=10)

    delete_button.bind("<Button-1>", lambda event: on_delete_task())
    edit_button.bind("<Button-1>", lambda event: on_edit_task())
    add_detail_button.bind("<Button-1>", lambda event: add_detail())

# --- Floating Icon Window ---
root = tk.Tk()
root.overrideredirect(True)
root.geometry("50x50+100+100")
root.wm_attributes("-topmost", 1)

# --- Use Canvas to draw a circle ---
canvas = tk.Canvas(root, width=50, height=50, highlightthickness=0, bg='white')
canvas.pack()

# Draw circle (oval) in the center
circle = canvas.create_oval(5, 5, 45, 45, fill="dodgerblue", outline="")

# Optional: add a white text in the center
canvas.create_text(25, 25, text="todo", fill="white", font=("Arial", 10, "bold"))

def on_click(event):
    show_todo_popup()  # Show or close the popup when the icon is clicked

def start_move(event): 
    root.x = event.x
    root.y = event.y

def do_move(event):
    x = root.winfo_pointerx() - root.x
    y = root.winfo_pointery() - root.y
    root.geometry(f"+{x}+{y}")

button = tk.Label(root, text="📝", font=("Arial", 24), bg="white", width=3, height=1)
button.pack()

button.bind("<Button-1>", on_click)
button.bind("<ButtonPress-3>", start_move)
button.bind("<B3-Motion>", do_move)

canvas.bind("<Button-1>", on_click)
canvas.bind("<ButtonPress-3>", start_move)
canvas.bind("<B3-Motion>", do_move)

root.mainloop()
