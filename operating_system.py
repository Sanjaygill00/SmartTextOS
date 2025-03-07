import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
import os
import shutil
import wikipediaapi  # Add this import statement

# Function to display welcome message
def show_welcome():
    welcome_label.config(text="Welcome to your operating system")
    welcome_label.place(relx=0.5, rely=0.5, anchor="center")
    fade_in(welcome_label)

# Function for fade-in animation
def fade_in(widget, alpha=0):
    if alpha < 1:
        alpha += 0.1
        hex_color = f"#{int(alpha * 255):02x}{int(alpha * 255):02x}{int(alpha * 255):02x}"
        widget.config(fg=hex_color)
        widget.after(100, fade_in, widget, alpha)

# Function to update the clock
def update_clock():
    now = datetime.now().strftime("%I:%M:%S %p")
    clock_label.config(text=now)
    clock_label.after(1000, update_clock)

# Real-Time Notifications
def show_notification(message):
    notification_label.config(text=message, fg="white", bg="green")
    root.after(3000, lambda: notification_label.config(text="", bg="#2C3E50"))  # Clear notification after 3 seconds

# File operations
def new_file():
    tab = ttk.Frame(tab_control)
    tab_control.add(tab, text="Untitled")
    text_widget = tk.Text(tab, wrap="word", font=("Arial", 14), undo=True, bg="#FFFFFF", fg="#000000")
    text_widget.pack(expand=True, fill="both")
    tab_control.select(tab)
    show_notification("New file created")

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        try:
            with open(file_path, "r") as file:
                content = file.read()
            tab = ttk.Frame(tab_control)
            tab_control.add(tab, text=file_path.split("/")[-1])
            text_widget = tk.Text(tab, wrap="word", font=("Arial", 14), undo=True, bg="#FFFFFF", fg="#000000")
            text_widget.insert(tk.END, content)
            text_widget.pack(expand=True, fill="both")
            tab_control.select(tab)
            show_notification(f"File opened: {file_path}")
        except Exception as e:
            show_notification(f"Error opening file: {e}")

def save_file():
    current_tab = tab_control.nametowidget(tab_control.select())
    if current_tab:
        text_widget = current_tab.winfo_children()[0]
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            try:
                with open(file_path, "w") as file:
                    file.write(text_widget.get("1.0", tk.END))
                tab_control.tab(current_tab, text=file_path.split("/")[-1])
                show_notification(f"File saved at: {file_path}")
            except Exception as e:
                show_notification(f"Error saving file: {e}")

# Secret Save functionality
def secret_save():
    current_tab = tab_control.nametowidget(tab_control.select())
    if current_tab:
        text_widget = current_tab.winfo_children()[0]
        content = text_widget.get("1.0", tk.END)
        
        secret_dir = os.path.expanduser("~/.secret_files")  # Hidden folder for secret files
        if not os.path.exists(secret_dir):
            os.makedirs(secret_dir)
        
        secret_file_path = os.path.join(secret_dir, f"secret_file_{len(os.listdir(secret_dir)) + 1}.txt")
        try:
            with open(secret_file_path, "w") as file:
                file.write(content)
            show_notification(f"Secret file saved at {secret_file_path}")
        except Exception as e:
            show_notification(f"Error saving secret file: {e}")

# Secret File Access
def access_secret_files():
    secret_dir = os.path.expanduser("~/.secret_files")
    if not os.path.exists(secret_dir):
        show_notification("No secret files found.")
        return
    
    secret_files = [f for f in os.listdir(secret_dir) if f.endswith(".txt")]
    if not secret_files:
        show_notification("No secret files found.")
        return
    
    # Create a window to show secret files
    access_window = tk.Toplevel(root)
    access_window.title("Secret Files")
    access_window.geometry("300x300")
    
    file_listbox = tk.Listbox(access_window, height=10)
    for file in secret_files:
        file_listbox.insert(tk.END, file)
    
    def open_secret_file(event):
        selected_file = file_listbox.get(file_listbox.curselection())
        file_path = os.path.join(secret_dir, selected_file)
        try:
            with open(file_path, "r") as file:
                content = file.read()
            new_file()
            current_tab = tab_control.nametowidget(tab_control.select())
            text_widget = current_tab.winfo_children()[0]
            text_widget.insert("1.0", content)
            show_notification(f"Secret file '{selected_file}' opened.")
            access_window.destroy()  # Close the access window
        except Exception as e:
            show_notification(f"Error opening secret file: {e}")

    file_listbox.pack(expand=True, fill="both")
    file_listbox.bind("<Double-1>", open_secret_file)

# Secret File Deletion
def delete_secret_file():
    secret_dir = os.path.expanduser("~/.secret_files")
    if not os.path.exists(secret_dir):
        show_notification("No secret files found.")
        return
    
    secret_files = [f for f in os.listdir(secret_dir) if f.endswith(".txt")]
    if not secret_files:
        show_notification("No secret files found.")
        return
    
    # Create a window to show secret files for deletion
    delete_window = tk.Toplevel(root)
    delete_window.title("Delete Secret File")
    delete_window.geometry("300x300")
    
    file_listbox = tk.Listbox(delete_window, height=10)
    for file in secret_files:
        file_listbox.insert(tk.END, file)
    
    def delete_selected_file(event):
        selected_file = file_listbox.get(file_listbox.curselection())
        file_path = os.path.join(secret_dir, selected_file)
        try:
            os.remove(file_path)
            show_notification(f"Secret file '{selected_file}' deleted.")
            delete_window.destroy()  # Close the delete window
        except Exception as e:
            show_notification(f"Error deleting file: {e}")

    file_listbox.pack(expand=True, fill="both")
    file_listbox.bind("<Double-1>", delete_selected_file)

# Undo/Redo operations
def undo_text():
    current_tab = tab_control.nametowidget(tab_control.select())
    if current_tab:
        text_widget = current_tab.winfo_children()[0]
        try:
            text_widget.edit_undo()
        except Exception:
            show_notification("Nothing to undo.")

def redo_text():
    current_tab = tab_control.nametowidget(tab_control.select())
    if current_tab:
        text_widget = current_tab.winfo_children()[0]
        try:
            text_widget.edit_redo()
        except Exception:
            show_notification("Nothing to redo.")

# Search functionality
def search_text():
    search_query = search_entry.get()
    current_tab = tab_control.nametowidget(tab_control.select())
    if current_tab:
        text_widget = current_tab.winfo_children()[0]
        text_widget.tag_remove("highlight", "1.0", tk.END)
        if search_query:
            idx = "1.0"
            while True:
                idx = text_widget.search(search_query, idx, nocase=1, stopindex=tk.END)
                if not idx:
                    break
                end_idx = f"{idx}+{len(search_query)}c"
                text_widget.tag_add("highlight", idx, end_idx)
                idx = end_idx
            text_widget.tag_config("highlight", background="yellow")
            show_notification(f"Search completed for '{search_query}'")

# Wikipedia search functionality
def search_wikipedia():
    query = search_entry.get()
    if query:
        wiki = wikipediaapi.Wikipedia(language="en", user_agent="MyApp/1.0 (https://example.com)")
        page = wiki.page(query)
        if page.exists():
            new_file()
            current_tab = tab_control.nametowidget(tab_control.select())
            text_widget = current_tab.winfo_children()[0]
            text_widget.insert("1.0", page.text)
            show_notification(f"Wikipedia results for '{query}' displayed.")
        else:
            show_notification(f"No Wikipedia page found for '{query}'.")

# Theme switching
def toggle_theme():
    if workspace["bg"] == "#ECF0F1":
        workspace.configure(bg="#1A1A2E")
        for tab in tab_control.winfo_children():
            text_widget = tab.winfo_children()[0]
            text_widget.configure(bg="#1A1A2E", fg="#FFFFFF")
    else:
        workspace.configure(bg="#ECF0F1")
        for tab in tab_control.winfo_children():
            text_widget = tab.winfo_children()[0]
            text_widget.configure(bg="#FFFFFF", fg="#000000")

# Create the main application window
root = tk.Tk()
root.title("My Operating System")
root.geometry("1200x800")
root.configure(bg="#1A1A2E")

# Welcome Screen
welcome_label = tk.Label(root, text="", font=("Helvetica", 24, "bold"), bg="#1A1A2E", fg="#1A1A2E")
root.after(1000, show_welcome)

# Notification Area
notification_label = tk.Label(root, text="", font=("Helvetica", 12), bg="#2C3E50", fg="white")
notification_label.pack(side="top", fill="x")

# Top Bar
top_bar = tk.Frame(root, bg="#2C3E50")
top_bar.pack(side="top", fill="x")

clock_label = tk.Label(top_bar, text="", font=("Helvetica", 14), bg="#2C3E50", fg="#ECF0F1")
clock_label.pack(side="right", padx=10, pady=5)
update_clock()

search_entry = tk.Entry(top_bar, width=20, font=("Helvetica", 12))
search_entry.pack(side="left", padx=10, pady=5)
search_button = tk.Button(top_bar, text="Search", command=search_text, bg="#1ABC9C", fg="#FFFFFF", font=("Arial", 10))
search_button.pack(side="left", padx=5)
wiki_button = tk.Button(top_bar, text="Wikipedia", command=search_wikipedia, bg="#3498DB", fg="#FFFFFF", font=("Arial", 10))
wiki_button.pack(side="left", padx=5)

# Left Dock
left_dock = tk.Frame(root, bg="#34495E", width=80)
left_dock.pack(side="left", fill="y")

# Initialize the dock_buttons list first
dock_buttons = [
    ("New", new_file, "#1ABC9C"),
    ("Open", open_file, "#1ABC9C"),
    ("Save", save_file, "#1ABC9C"),
    ("Undo", undo_text, "#3498DB"),
    ("Redo", redo_text, "#3498DB"),
    ("Theme", toggle_theme, "#9B59B6"),
    ("Secret Save", secret_save, "#9B59B6"),
    ("Secret Access", access_secret_files, "#E74C3C"),
    ("Delete Secret", delete_secret_file, "#E74C3C"),  # Added here
    ("Exit", root.destroy, "#E74C3C")
]

# Now append the buttons to the dock
for text, command, color in dock_buttons:
    button = tk.Button(left_dock, text=text, command=command, bg=color, fg="#FFFFFF", font=("Arial", 12))
    button.pack(fill="x", padx=5, pady=5)

# Main Workspace
workspace = tk.Frame(root, bg="#ECF0F1")
workspace.pack(side="right", expand=True, fill="both")

# Tab Control (file workspace)
tab_control = ttk.Notebook(workspace)
tab_control.pack(expand=True, fill="both")

root.mainloop()
