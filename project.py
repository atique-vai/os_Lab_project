import psutil
import tkinter as tk
from tkinter import ttk, messagebox

def refresh_process_list():
    # Clear existing rows
    for row in tree.get_children():
        tree.delete(row)

    # Add processes to the tree
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            pid = proc.info['pid']
            name = proc.info['name']
            cpu = proc.info['cpu_percent']
            memory = proc.info['memory_percent']
            tree.insert('', 'end', values=(pid, name, f"{cpu:.2f}%", f"{memory:.2f}%"))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

def kill_process():
    try:
        selected_item = tree.selection()[0]
        pid = int(tree.item(selected_item, 'values')[0])
        psutil.Process(pid).terminate()
        messagebox.showinfo("Success", f"Process with PID {pid} terminated.")
        refresh_process_list()
    except IndexError:
        messagebox.showwarning("Error", "No process selected.")
    except psutil.NoSuchProcess:
        messagebox.showwarning("Error", "Process no longer exists.")
    except psutil.AccessDenied:
        messagebox.showerror("Error", "Permission denied.")

# GUI setup
root = tk.Tk()
root.title("Task Manager")
root.geometry("600x400")

# Treeview for process list
columns = ("PID", "Name", "CPU Usage", "Memory Usage")
tree = ttk.Treeview(root, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)
tree.pack(fill=tk.BOTH, expand=True)

# Buttons
button_frame = tk.Frame(root)
button_frame.pack(fill=tk.X, pady=10)

refresh_button = tk.Button(button_frame, text="Refresh", command=refresh_process_list)
refresh_button.pack(side=tk.LEFT, padx=5)

kill_button = tk.Button(button_frame, text="Kill Process", command=kill_process)
kill_button.pack(side=tk.LEFT, padx=5)

# Load process list on startup
refresh_process_list()

# Run the GUI loop
root.mainloop()
