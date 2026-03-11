import json
import csv
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import simpledialog


# ---------- FILE FUNCTIONS ----------

def save_students():
    with open("students.json", "w") as file:
        json.dump(students, file, indent=4)

def load_students():
    try:
        with open("students.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# ---------- LOGIC FUNCTIONS ----------

def add_student():
    name = name_entry.get()
    mark_text = mark_entry.get()

    if not name.strip():
        output_label.config(text="Name cannot be empty")
        return

    if not mark_text.isdigit():
        output_label.config(text="Mark must be a number")
        return

    mark = int(mark_text)

    if mark < 0 or mark > 100:
        output_label.config(text="Mark must be 0-100")
        return

    students.append({
        "name": name,
        "mark": mark
    })

    save_students()
    refresh_table()

    output_label.config(text=f"{name} added")

    name_entry.delete(0, tk.END)
    mark_entry.delete(0, tk.END)
    
    name_entry.focus()



def average_mark():
    if not students:
        output_label.config(text="No students")
        return

    total = 0
    for s in students:
        total += s["mark"]

    avg = round(total / len(students))

    output_label.config(text=f"Average: {avg}")
    
def refresh_table(filter_text=""):
    table.delete(*table.get_children())
    
    # sort students by mark (highest first)
    sorted_students = sorted(students, key=lambda s: s["mark"], reverse=True)
    
    for student in sorted_students:
        name = student["name"]
        
        if filter_text.lower() in name.lower():
            table.insert("", tk.END, values=(student["name"], student["mark"]))
        
def delete_selected():
    selected = table.selection()
    
    if not selected:
        output_label.config(text="No student selected")
        return
    
    item = table.item(selected[0])
    name = item["values"][0]
    
    for student in students:
        if student["name"] == name:
            students.remove(student)
            break
        
    save_students()
    refresh_table()
    
    output_label.config(text=f"{name} deleted")
    
    
def edit_student(event):
    selected = table.selection()
    
    if not selected:
        return
    
    item = table.item(selected[0])
    name, mark = item["values"]
    
    edit_window = tk.Toplevel(window)
    edit_window.title("Edit Mark")
    
    tk.Label(edit_window, text=f"Student: {name}").pack(pady=5)
    
    tk.Label(edit_window, text="New Mark").pack()
    new_mark_entry = tk.Entry(edit_window)
    new_mark_entry.insert(0, mark)
    new_mark_entry.pack()
    
    def save_edit():
        mark_text = new_mark_entry.get()
    
        if not mark_text.isdigit():
            return
    
        new_mark = int(mark_text)
    
        if new_mark < 0 or new_mark > 100:
            return 
    
        for student in students:
            if student["name"] == name:
                student["mark"] = new_mark
                break
        
        save_students()
        refresh_table()
    
        edit_window.destroy()
    
        output_label.config(text=f"{name}'s mark updated")
    
    tk.Button(edit_window, text="Save", command=save_edit).pack(pady=5)
    
    
def sort_column(col, reverse):
    data = [(table.set(item, col), item) for item in table.get_children()]
    
    if col == "mark":
        data = [(int(value), item) for value, item in data]
        
    data.sort(reverse=reverse)

    for index, (value, item) in enumerate(data):
        table.move(item, "", index)
        
    table.heading(col, command=lambda: sort_column(col, not reverse))
    
    
def search_students(event):
    text = search_entry.get()
    refresh_table(text)       
    
    
def export_csv():
    with open("students.csv", "w", newline="") as file:
        writer = csv.writer(file)
        
        writer.writerow(["Name", "Mark"])
        
        for student in students:
            writer.writerow([student["name"], student["mark"]])
            
        output_label.config(text="Exported to students.csv")
        
        
#def edit_mark(event):
    
    selected = table.selection()
    
    if not selected:
        return
    
    item = table.item(selected[0])
    name = item["values"][0]
    current_mark = item["values"][1]   
    
    new_mark = simpledialog.askinteger(
        "Edit Mark",
        f"Enter new mark for {name}",
        initialvalue=current_mark
        )
    
    if new_mark is None:
        return
    
    if new_mark < 0 or new_mark > 100:
        output_label.config(text="Mark must be 0-100")
        return
    
    for student in students:
        if student["name"] == name:
            student["mark"] = new_mark
            break
        
    save_students()
    refresh_table()
    
    output_label.config(text=f"{name}'s mark updated")
# ---------- LOAD DATA ----------

students = load_students()

# ---------- GUI ----------

window = tk.Tk()
window.title("Student Manager")
window.geometry("700x600")


input_frame = tk.Frame(window)
input_frame.pack(pady=10)


# Menu bar
menu_bar = tk.Menu(window)

file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Export to CSV", command=export_csv)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=window.quit)

menu_bar.add_cascade(label="File", menu=file_menu)

window.config(menu=menu_bar)



# Name
tk.Label(input_frame, text="Name").grid(row=0, column=0, padx=5, pady=5)
name_entry = tk.Entry(input_frame)
name_entry.grid(row=0, column=1, padx=5, pady=5)


# Mark
tk.Label(input_frame, text="Mark").grid(row=0, column=2, padx=5, pady=5)
mark_entry = tk.Entry(input_frame, width=10)
mark_entry.grid(row=0, column=3, padx=5, pady=5)

# Buttons
button_frame = tk.Frame(window)
button_frame.pack(pady=5)

tk.Button(button_frame, text="Add Student", command=add_student).grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="Average Mark", command=average_mark).grid(row=0, column=1,padx=5)
tk.Button(button_frame, text="Delete Selected", command=delete_selected).grid(row=0, column=2, padx=5)


# Search

search_frame = tk.Frame(window)
search_frame.pack(pady=5)


tk.Label(search_frame, text="Search").grid(row=0, column=0, padx=5)

columns = ("name", "mark")



search_entry = tk.Entry(search_frame, width=30)
search_entry.grid(row=0, column=1, padx=5)

search_entry.bind("<KeyRelease>", search_students)



# Table
table_frame = tk.Frame(window)
table_frame.pack(fill="both", expand=True)



scrollbar = tk.Scrollbar(table_frame)
scrollbar.pack(side="right", fill="y")

table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    yscrollcommand=scrollbar.set
)

table.pack(fill="both", expand=True)

scrollbar.config(command=table.yview)




table.heading("name", text="Name", command=lambda: sort_column("name", False))
table.heading("mark", text="Mark", command=lambda: sort_column("mark", False))

table.column("name", width=200)
table.column("mark", width=100, anchor="center")


table.bind("<Double-1>", edit_student)
table["displaycolumns"] = ("name", "mark")

table.bind("<Double-1>", edit_student)

refresh_table()


# Status message
output_label = tk.Label(window, text="")
output_label.pack()

window.mainloop()