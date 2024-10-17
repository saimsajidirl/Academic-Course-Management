import tkinter as tk
from tkinter import ttk, messagebox
import re
import requests
from ttkthemes import ThemedTk

class ModernSOSManager:
    def __init__(self):
        # Create themed root window
        self.root = ThemedTk(theme="arc")
        self.root.title("Study Management System")
        self.root.geometry("1200x700")
        self.root.configure(bg="#f0f0f0")

        # Initialize semesters dictionary
        self.semesters = {}

        # Custom style configuration
        self.setup_styles()
        
        # Create main frames
        self.left_frame = ttk.Frame(self.root, padding="20")
        self.right_frame = ttk.Frame(self.root, padding="20")
        
        # Grid configuration
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.setup_left_panel()
        self.setup_right_panel()
        self.setup_menu()

    def setup_styles(self):
        style = ttk.Style()
        style.configure("Treeview", rowheight=30, font=('Helvetica', 10))
        style.configure("TButton", padding=10, font=('Helvetica', 10))
        style.configure("TLabel", font=('Helvetica', 11))
        style.configure("TEntry", font=('Helvetica', 10))
        style.configure("Title.TLabel", font=('Helvetica', 16, 'bold'))
        style.configure("Header.TLabel", font=('Helvetica', 11, 'bold'))

    def setup_left_panel(self):
        # Title Label
        title_label = ttk.Label(self.left_frame, text="Course Information", style="Title.TLabel")
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Input fields with labels
        self.create_input_fields()

        # Buttons Frame
        self.create_buttons()

        # Semester Selection
        self.create_semester_selector()

    def create_input_fields(self):
        labels = ["Course Name:", "Instructor:", "Credits:", "Schedule:"]
        self.entries = []
        
        for i, label in enumerate(labels):
            ttk.Label(self.left_frame, text=label).grid(row=i+1, column=0, sticky="w", pady=5)
            entry = ttk.Entry(self.left_frame, width=30)
            entry.grid(row=i+1, column=1, pady=5, padx=10)
            self.entries.append(entry)

    def create_buttons(self):
        button_frame = ttk.Frame(self.left_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=20)

        buttons = [
            ("Add Course", self.add_item),
            ("Remove Course", self.remove_item),
            ("Edit Course", self.edit_item),
            ("Save Changes", self.save_sos),
            ("Sort Courses", self.sort_items),
            ("Load Courses", self.load_subjects)
        ]

        for i, (text, command) in enumerate(buttons):
            btn = ttk.Button(button_frame, text=text, command=command, width=20)
            btn.grid(row=i//2, column=i%2, padx=5, pady=5)

    def create_semester_selector(self):
        semester_frame = ttk.Frame(self.left_frame)
        semester_frame.grid(row=7, column=0, columnspan=2, pady=20)
        
        ttk.Label(semester_frame, text="Select Semester:", style="Header.TLabel").pack(side=tk.LEFT, padx=5)
        
        options = [f"Semester {i}" for i in range(1, 9)]
        self.variable = tk.StringVar(value=options[0])
        semester_menu = ttk.OptionMenu(semester_frame, self.variable, *options)
        semester_menu.pack(side=tk.LEFT, padx=5)

    def setup_right_panel(self):
        # Create and configure Treeview
        columns = ("Course", "Instructor", "Credits", "Schedule")
        self.tree = ttk.Treeview(self.right_frame, columns=columns, show="headings")
        
        # Configure columns and headings
        for col in columns:
            self.tree.heading(col, text=col, anchor=tk.CENTER)
            self.tree.column(col, anchor=tk.CENTER, width=150)

        # Add scrollbars
        y_scroll = ttk.Scrollbar(self.right_frame, orient=tk.VERTICAL, command=self.tree.yview)
        x_scroll = ttk.Scrollbar(self.right_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

        # Grid layout for tree and scrollbars
        self.tree.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")
        
        self.right_frame.grid_rowconfigure(0, weight=1)
        self.right_frame.grid_columnconfigure(0, weight=1)

    def setup_menu(self):
        menubar = tk.Menu(self.root)
        teacher_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Teachers", menu=teacher_menu)
        
        teachers = [
            ("Sir Nauman", 1),
            ("Sir Rafaqat Kazmi", 2),
            ("Ma'am Sunnia", 3)
        ]
        
        for teacher, num in teachers:
            teacher_menu.add_command(label=teacher, command=lambda x=num: self.select_teacher(x))
        
        self.root.config(menu=menubar)

    def add_item(self):
        try:
            subject_name = self.entries[0].get()
            description = self.entries[1].get()
            course_code = self.entries[2].get()
            teacher_name = self.entries[3].get()

            if all([subject_name, description, course_code, teacher_name]):
                selected_semester = self.variable.get()
                if selected_semester:
                    course_info = (subject_name, teacher_name, course_code, description)
                    self.tree.insert('', 'end', values=course_info)

                    data = {
                        'subject_name': subject_name,
                        'description': description,
                        'course_code': course_code,
                        'teacher_name': teacher_name,
                        'selected_semester': selected_semester
                    }
                    
                    try:
                        response = requests.post('http://127.0.0.1:5000/sos', json=data)
                        if response.status_code == 201:
                            self.show_notification("Course added successfully!")
                        else:
                            self.show_notification(f"Error adding course: {response.json().get('error')}", "error")
                    except requests.RequestException as e:
                        self.show_notification(f"Network error: {str(e)}", "error")

                self.clear_entry_fields()
            else:
                self.show_notification("Please fill all fields!", "error")
        except Exception as e:
            self.show_notification(f"Error: {str(e)}", "error")

    def remove_item(self):
        selected_item = self.tree.selection()
        if selected_item:
            try:
                self.tree.delete(selected_item)
                self.show_notification("Course removed successfully!")
            except Exception as e:
                self.show_notification(f"Error removing course: {str(e)}", "error")
        else:
            self.show_notification("Please select a course to remove!", "error")

    def edit_item(self):
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item)['values']
            for entry, value in zip(self.entries, values):
                entry.delete(0, tk.END)
                entry.insert(0, value)
            self.tree.delete(selected_item)
        else:
            self.show_notification("Please select a course to edit!", "error")

    def save_sos(self):
        try:
            with open("sos.txt", "w") as f:
                for item in self.tree.get_children():
                    values = self.tree.item(item)['values']
                    f.write(f"{','.join(map(str, values))}\n")
            self.show_notification("Courses saved successfully!")
        except Exception as e:
            self.show_notification(f"Error saving courses: {str(e)}", "error")

    def sort_items(self):
        try:
            items = [(self.tree.item(item)["values"], item) for item in self.tree.get_children('')]
            items.sort(key=lambda x: x[0][0])  # Sort by course name
            
            for idx, (values, item) in enumerate(items):
                self.tree.move(item, '', idx)
            
            self.show_notification("Courses sorted successfully!")
        except Exception as e:
            self.show_notification(f"Error sorting courses: {str(e)}", "error")

    def load_subjects(self):
        try:
            selected_semester = self.variable.get()
            if selected_semester:
                response = requests.get('http://127.0.0.1:5000/sos', 
                                     params={'selected_semester': selected_semester})
                
                if response.status_code == 200:
                    self.tree.delete(*self.tree.get_children())
                    courses = response.json().get('courses', [])
                    for course in courses:
                        self.tree.insert('', 'end', values=course)
                    self.show_notification("Courses loaded successfully!")
                else:
                    self.show_notification(f"Error loading courses: {response.json().get('error')}", "error")
        except Exception as e:
            self.show_notification(f"Error: {str(e)}", "error")

    def clear_entry_fields(self):
        for entry in self.entries:
            entry.delete(0, tk.END)

    def select_teacher(self, teacher_number):
        teacher_data = {
            1: ("Sir Nauman", ["Programming", "Data Structures"]),
            2: ("Sir Rafaqat Kazmi", ["Database", "Software Engineering"]),
            3: ("Ma'am Sunnia", ["Web Development", "AI"])
        }

        if teacher_number in teacher_data:
            teacher_name, courses = teacher_data[teacher_number]
            self.tree.delete(*self.tree.get_children())
            for course in courses:
                self.tree.insert('', 'end', values=(course, teacher_name, "3", "Mon/Wed"))
            self.show_notification(f"Loaded courses for {teacher_name}")

    def show_notification(self, message, type_="info"):
        if type_ == "info":
            messagebox.showinfo("Notification", message)
        else:
            messagebox.showerror("Error", message)

if __name__ == "__main__":
    sos_manager = ModernSOSManager()
    sos_manager.root.mainloop()