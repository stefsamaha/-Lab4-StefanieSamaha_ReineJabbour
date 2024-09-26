"""
school_management_system.py
===========================

This module creates a GUI for a School Management System using Tkinter. It allows users
to manage student, instructor, and course data, including adding, updating, deleting
students, as well as registering students for courses.

Global Variables:
-----------------
my_data_list : list
    Stores student data, including name, age, email, ID, and registered courses.
instructor_data_list : list
    Stores instructor data, including name, age, email, and ID.
course_data_list : list
    Stores course data, including course name, ID, instructor name, and enrolled students.

Functions:
----------
-load delete into the database
- load_json_from_file
- save_json_to_file
- remove_all_data_from_trv
- load_trv_with_json
- clear_all_fields
- find_row_in_my_data_list
- change_bg_color
- change_enabled_state
- load_edit_field_with_row_data
- search_student
- cancel
- print_all_entries
- add_entry
- update_entry
- delete_entry
- process_request
- MouseButtonUpCallBack
- register_student_for_course
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import sqlite3
import re

# Helper function for email validation


def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)


class Person:
    def __init__(self, name, age, _email):
        self.name = name
        self.age = age
        if int(age) < 0:
            raise ValueError("Age cannot be negative")
        if not is_valid_email(_email):
            raise ValueError("Invalid email format")
        self._email = _email

    def introduce(self):
        return f"Name: {self.name}, Age: {self.age}"

    def to_dict(self):
        return {
            "n_entry": self.name,
            "Age": self.age,
            "email": self._email,
            "id": self.student_id
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["n_entry"],
            age=data["Age"],
            _email=data["email"],
            student_id=data["id"]
        )


class Student(Person):
    def __init__(self, name, age, _email, student_id, registered_courses=None):
        super().__init__(name, age, _email)
        self.student_id = student_id
        self.registered_courses = registered_courses if registered_courses is not None else []

    def register_course(self, course):
        self.registered_courses.append(course)

    def to_dict(self):
        # Convert the object to a dictionary for JSON storage
        return {
            "n_entry": self.name,
            "Age": self.age,
            "email": self._email,
            "id": self.student_id,
            "registered_courses": self.registered_courses
        }

    @classmethod
    def from_dict(cls, data):
        # Create a Student object from a dictionary
        return cls(
            name=data["n_entry"],
            age=data["Age"],
            _email=data["email"],
            student_id=data["id"],
            registered_courses=data.get("registered_courses", [])
        )


class Instructor(Person):
    def __init__(self, name, age, _email, instructor_id, assigned_courses=None):
        super().__init__(name, age, _email)
        self.instructor_id = instructor_id
        self.assigned_courses = assigned_courses if assigned_courses is not None else []

    def assign_course(self, course):
        self.assigned_courses.append(course)


class Course:
    def __init__(self, course_id, course_name, instructor=None, enrolled_students=None):
        self.course_id = course_id
        self.course_name = course_name
        self.instructor = instructor  # Instructor object
        # List of Student objects
        self.enrolled_students = enrolled_students if enrolled_students is not None else []

    def add_student(self, student):
        self.enrolled_students.append(student)


# Database functions
def initialize_db():
    conn = sqlite3.connect('school_management.db')
    c = conn.cursor()

    # Drop the existing table if it exists
    c.execute('DROP TABLE IF EXISTS students')
    c.execute('DROP TABLE IF EXISTS instructors')
    c.execute('DROP TABLE IF EXISTS courses')
    c.execute('DROP TABLE IF EXISTS registrations')
    c.execute('DROP TABLE IF EXISTS assignments')

    # Create tables
    c.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id TEXT PRIMARY KEY,
            name TEXT,
            age INTEGER,
            email TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS instructors (
            id TEXT PRIMARY KEY,
            name TEXT,
            age INTEGER,
            email TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            id TEXT PRIMARY KEY,
            name TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS registrations (
            student_id TEXT,
            course_id TEXT,
            FOREIGN KEY (student_id) REFERENCES students (id),
            FOREIGN KEY (course_id) REFERENCES courses (id)
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS assignments (
            instructor_id TEXT,
            course_id TEXT,
            FOREIGN KEY (instructor_id) REFERENCES instructors (id),
            FOREIGN KEY (course_id) REFERENCES courses (id)
        )
    ''')

    conn.commit()
    conn.close()


def insert_student(student_id, name, age, email):
    conn = sqlite3.connect('school_management.db')
    c = conn.cursor()
    c.execute('INSERT INTO students (id, name, age, email) VALUES (?, ?, ?, ?)',
              (student_id, name, age, email))
    conn.commit()
    conn.close()


def insert_instructor(instructor_id, name, age, email):
    conn = sqlite3.connect('school_management.db')
    c = conn.cursor()
    c.execute('INSERT INTO instructors (id, name, age, email) VALUES (?, ?, ?, ?)',
              (instructor_id, name, age, email))
    conn.commit()
    conn.close()


def insert_course(course_id, name):
    conn = sqlite3.connect('school_management.db')
    c = conn.cursor()
    c.execute('INSERT INTO courses (id, name) VALUES (?, ?)', (course_id, name))
    conn.commit()
    conn.close()


def insert_registration(student_id, course_id):
    conn = sqlite3.connect('school_management.db')
    c = conn.cursor()
    c.execute('INSERT INTO registrations (student_id, course_id) VALUES (?, ?)',
              (student_id, course_id))
    conn.commit()
    conn.close()


def insert_assignment(instructor_id, course_id):
    conn = sqlite3.connect('school_management.db')
    c = conn.cursor()
    c.execute('INSERT INTO assignments (instructor_id, course_id) VALUES (?, ?)',
              (instructor_id, course_id))
    conn.commit()
    conn.close()


def fetch_all_students():
    conn = sqlite3.connect('school_management.db')
    c = conn.cursor()
    c.execute('SELECT * FROM students')
    students = c.fetchall()
    conn.close()
    return students


def fetch_all_instructors():
    conn = sqlite3.connect('school_management.db')
    c = conn.cursor()
    c.execute('SELECT * FROM instructors')
    instructors = c.fetchall()
    conn.close()
    return instructors


def fetch_all_courses():
    conn = sqlite3.connect('school_management.db')
    c = conn.cursor()
    c.execute('SELECT * FROM courses')
    courses = c.fetchall()
    conn.close()
    return courses


def fetch_all_registrations():
    conn = sqlite3.connect('school_management.db')
    c = conn.cursor()
    c.execute('''
        SELECT students.id, courses.name, 'Registered'
        FROM registrations
        JOIN students ON registrations.student_id = students.id
        JOIN courses ON registrations.course_id = courses.id
    ''')
    registrations = c.fetchall()
    conn.close()
    return registrations


def fetch_all_assignments():
    conn = sqlite3.connect('school_management.db')
    c = conn.cursor()
    c.execute('''
        SELECT instructors.id, courses.name, 'Assigned'
        FROM assignments
        JOIN instructors ON assignments.instructor_id = instructors.id
        JOIN courses ON assignments.course_id = courses.id
    ''')
    assignments = c.fetchall()
    conn.close()
    return assignments


def delete_record(record_id, record_type):
    conn = sqlite3.connect('school_management.db')
    c = conn.cursor()

    if record_type == "Student":
        c.execute('DELETE FROM students WHERE id = ?', (record_id,))
        c.execute('DELETE FROM registrations WHERE student_id = ?', (record_id,))
    elif record_type == "Instructor":
        c.execute('DELETE FROM instructors WHERE id = ?', (record_id,))
        c.execute('DELETE FROM assignments WHERE instructor_id = ?', (record_id,))
    elif record_type == "Course":
        c.execute('DELETE FROM courses WHERE id = ?', (record_id,))
        c.execute('DELETE FROM registrations WHERE course_id = ?', (record_id,))
        c.execute('DELETE FROM assignments WHERE course_id = ?', (record_id,))

    conn.commit()
    conn.close()


# Initialize database
initialize_db()

global my_data_list
global currentRowIndex
my_data_list = [
    {
        "name": "John Doe",
        "id": "12345",
        "Age": 25,
        "email": "johndoe@example.com",
        "registered_courses": ["Mathematics 101", "Physics 102"]
    }
]

instructor_data_list = [
    {
        "n_entry": "Jane Smith",
        "id": "98765",
        "Age": 40,
        "email": "janesmith@example.com"
    }
]

course_data_list = [
    {
        "course_name": "Mathematics 101",
        "id": "MATH101",
        "instructor_name": "John Doe",
        "enrolled_students": ["John Doe"]
    },
    {
        "course_name": "Physics 102",
        "id": "PHYS102",
        "instructor_name": "Jane Smith",
        "enrolled_students": ["John Doe"]
    }
]


# creating the first window
window = tk.Tk()
window.title("School Management System")
window.configure(bg='LightBlue')

notebook = ttk.Notebook(window)
notebook.pack(pady=10, expand=True)

# creating the forst frame inside the window
student_frame = tk.Frame(window)
student_frame.pack()

instructor_frame = tk.Frame(window)
instructor_frame.pack()

course_frame = tk.Frame(window)
course_frame.pack()
# creating the student label frame inside the frame
student = tk.LabelFrame(student_frame, text="New student")
student.grid(row=0, column=0, sticky="news", padx=20, pady=10)

student_frame.pack(fill="both", expand=True)
instructor_frame.pack(fill="both", expand=True)
course_frame.pack(fill="both", expand=True)

# Adding tabs
notebook.add(student_frame, text="Students")
notebook.add(instructor_frame, text="Instructors")
notebook.add(course_frame, text="Courses")
# creating all the widget inside the student frame
name = tk.Label(student, text="Name:")
name.grid(row=0, column=0)

age = tk.Label(student, text="Age:")
age.grid(row=0, column=2)

email = tk.Label(student, text="Email:")
email.grid(row=0, column=3)

id = tk.Label(student, text="ID:")
id.grid(row=0, column=4)

n_entry = tk.Entry(student)
n_entry.grid(row=1, column=0)
age_spinbox = tk.Spinbox(student, from_=17, to=100)
age_spinbox.grid(row=1, column=2)
email_entry = tk.Entry(student)
email_entry.grid(row=1, column=3)
id1_entry = tk.Entry(student)
id1_entry.grid(row=1, column=4)
# Create a dropdown for course registration in the student section
course_label = tk.Label(student, text="Register for Course:")
course_label.grid(row=2, column=0, padx=10, pady=5)

course_dropdown = ttk.Combobox(student)
course_dropdown['values'] = [course['course_name']
                             for course in course_data_list]
course_dropdown.grid(row=2, column=1, padx=10, pady=5)


for widget in student.winfo_children():
    widget.grid_configure(padx=10, pady=5)

trv = ttk.Treeview(student, columns=(1, 2, 3, 4), show="headings", height="16")
trv.grid(row=6, column=0, sticky="news", rowspan=16, columnspan=4)

trv.heading(1, text="Name", anchor="center")
trv.heading(2, text="Age", anchor="center")
trv.heading(3, text="Email", anchor="center")
trv.heading(4, text="ID", anchor="center")

# w: west
trv.column("#1", anchor="w", width=140, stretch=True)
trv.column("#2", anchor="w", width=140, stretch=True)
trv.column("#3", anchor="w", width=140, stretch=True)
trv.column("#4", anchor="w", width=140, stretch=True)


def load_json_from_file():
    """
    Loads student data from a JSON file and updates the global `my_data_list`.
    Converts each loaded entry into a `Student` object.
    """
    global my_data_list
    with open("school_data.json", "r") as file_handler:
        data = json.load(file_handler)
        # Convert dict to Student objects
        my_data_list = [Student.from_dict(entry) for entry in data]
    file_handler.close()
    print('file has been read and closed')


def save_json_to_file():
    """
    Saves the current student data into a JSON file.

    Writes the content of the global `my_data_list` into 'school_data.json'.
    """
    global my_data_list
    with open("school_data.json", "w") as file_handler:
        json.dump([student.to_dict()
                  for student in my_data_list], file_handler, indent=4)
    file_handler.close()
    print('file has been written to and close')


def remove_all_data_from_trv():
    """
    Clears all existing rows from the Tkinter Treeview widget (`trv`).

    Deletes all the rows in the Treeview widget so that it can be repopulated.
    """
    for item in trv.get_children():
        trv.delete(item)

# diff


def load_trv_with_json():
    """
    Loads data from `my_data_list` into the Treeview widget.
    Iterates over the `my_data_list` and adds each student as a row in the Treeview widget.
    """
    global my_data_list

    remove_all_data_from_trv()

    rowIndex = 1
    for student in my_data_list:
        # Now using the Student object attributes instead of dict keys
        trv.insert('', index='end', iid=rowIndex, text="",
                   values=(student.name, student.age, student._email, student.student_id))
        rowIndex += 1


def clear_all_fields():
    """
    Clears all input fields in the student form.

    Resets the text fields (`n_entry`, `age_spinbox`, `email_entry`, and `id1_entry`)
    so they are empty.
    """
    n_entry.delete(0, tk.END)
    age_spinbox.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    id1_entry.delete(0, tk.END)


def find_row_in_my_data_list(value):
    """
    Finds the row index of a student based on their name.

    Parameters:
    -----------
    value : str
        The name of the student to search for in `my_data_list`.

    Returns:
    --------
    int
        The index of the student in `my_data_list` or -1 if not found.
    """
    global my_data_list
    row = 0
    found = False

    for rec in my_data_list:
        if rec["n_entry"] == value:
            found = True
            break
        row += 1

    if (found == True):
        return (row)
    return (-1)


# def change_enabled_state(state):
#     """
#     Enables or disables specific buttons based on the state of the form.

#     Parameters:
#     -----------
#     state : str
#         The current state of the form, which determines which buttons are enabled or disabled.
#         Possible values: 'Edit', 'Cancel', 'New'.
#     """
#     if state == 'Edit':
#         btnUpdate["state"] = "normal"
#         btnDelete["state"] = "normal"
#         btnAdd["state"] = "disabled"
#     elif state == "Cancel":
#         btnUpdate["state"] = "disabled"
#         btnDelete["state"] = "disabled"
#         btnAdd["state"] = "disabled"
#     else:
#         btnUpdate["state"] = "disabled"
#         btnDelete["state"] = "disabled"
#         btnAdd["state"] = "normal"


def load_edit_field_with_row_data(_tuple):
    """
    Populates the input fields with the data of the selected row.

    Parameters:
    -----------
    _tuple : tuple
        A tuple containing the student's data (name, age, email, ID) to be loaded into the form.
    """
    if len(_tuple) == 0:
        return

    n_entry.delete(0, tk.END)
    n_entry.insert(0, _tuple[0])
    age_spinbox.delete(0, tk.END)
    age_spinbox.insert(0, _tuple[1])
    email_entry.delete(0, tk.END)
    email_entry.insert(0, _tuple[2])
    id1_entry.delete(0, tk.END)
    id1_entry.insert(0, _tuple[3])


def search_student(search_value):
    """
    Searches for students by name or ID and displays the results in the Treeview widget.

    Parameters:
    -----------
    search_value : str
        The value to search for in the student's name or ID.

    Displays a message if no matching student is found.
    """
    # Clear current Treeview
    remove_all_data_from_trv()

    # Search for students matching by name or ID
    rowIndex = 1
    for student in my_data_list:
        if search_value.lower() in student.name.lower() or search_value == student.student_id:
            trv.insert('', index='end', iid=rowIndex, text="", values=(
                student.name, student.age, student._email, student.student_id))
            rowIndex += 1

    # If no match found
    if rowIndex == 1:
        messagebox.showinfo(
            "Search Result", "No student found with that Name or ID")


def cancel():
    """
    Clears all input fields and sets the form state to 'New'.

    Calls `clear_all_fields()` and changes the enabled state of the buttons to the 'New' state.
    """
    clear_all_fields()
    # change_enabled_state('New')


def print_all_entries():
    """
    Prints all student entries from `my_data_list` to the console.

    Iterates through `my_data_list` and prints each student's data.
    """
    global my_data_list

    for rec in my_data_list:
        print(rec)


def add_entry():
    """
    Adds a new student entry to `my_data_list` based on the input form values.

    Retrieves the values entered in the form (name, age, email, ID) and processes the request
    to add the new student.
    """
    Name = n_entry.get()
    Age = int(age_spinbox.get())
    Email = email_entry.get()
    id1 = id1_entry.get()

    process_request('_INSERT_', Name, Age, Email, id1)
    # new_student = Student(Name, Age, Email, id1)
    # my_data_list.append(new_student)
    save_json_to_file()
    load_trv_with_json()
    clear_all_fields()


def update_entry():
    """
    Updates an existing student entry in `my_data_list`.

    Retrieves the values entered in the form and processes the request to update the student
    information.
    """
    Name = n_entry.get()
    Age = int(age_spinbox.get())
    Email = email_entry.get()
    ID = id1_entry.get()

    process_request('_UPDATE_', Name, Age, Email, ID)


def delete_entry():
    """
    Deletes a student entry from `my_data_list`.

    Retrieves the name entered in the form and processes the request to delete the student.
    """
    Name = n_entry.get()
    # student = search_student(Name)
    process_request('_DELETE_', Name, None, None, None)

    # if student:
    #     my_data_list.remove(student)
    #     save_json_to_file()
    #     load_trv_with_json()
    #     clear_all_fields()


def process_request(command_type, name_value, age_value, email_value, id_value):
    """
    Processes a request to insert, update, or delete a student entry.

    Depending on the command (`_INSERT_`, `_UPDATE_`, `_DELETE_`), the function modifies
    `my_data_list` accordingly.

    Parameters:
    -----------
    command_type : str
        The type of request ('_INSERT_', '_UPDATE_', '_DELETE_').
    name_value : str
        The name of the student.
    age_value : str
        The age of the student.
    email_value : str
        The email address of the student.
    id_value : str
        The ID of the student.
    """
    global my_data_list

    if command_type == "_UPDATE_":
        row = find_row_in_my_data_list(name_value)
        if row >= 0:
            data = {"n_entry": name_value,
                    "Age": age_value, "email": email_value, "id": id_value}
            my_data_list[row] = data
        student = search_student(name_value)
        if student:
            student.age = int(age_value)
            student._email = email_value
            student.student_id = id_value
        row = find_row_in_my_data_list(name_value)
        if row >= 0:
            data = {"n_entry": name_value,
                    "Age": age_value, "email": email_value, "id": id_value}
            my_data_list[row] = data

    elif command_type == "_INSERT_":
        data = {"n_entry": name_value,
                "Age": age_value, "email": email_value, "id": id_value}
        my_data_list.append(data)
        # new_student = Student(name=name_value, age=int(
        #     age_value), _email=email_value, student_id=id_value)
        # my_data_list.append(new_student)

    elif command_type == "_DELETE_":
        student = search_student(name_value)
        row = find_row_in_my_data_list(name_value)
        if row >= 0:
            del my_data_list[row]
        if student:
            my_data_list.remove(student)

    save_json_to_file()
    load_trv_with_json()
    clear_all_fields()


def MouseButtonUpCallBack(event):
    """
    Callback function that is triggered when a row in the Treeview widget is clicked.

    Loads the clicked row's data into the input fields and changes the form state to 'Edit'.

    Parameters:
    -----------
    event : Event
        The Tkinter event that triggered this callback.
    """
    currentRowIndex = trv.selection()[0]
    lastTuple = trv.item(currentRowIndex, "values")
    n_entry.delete(0, tk.END)
    n_entry.insert(0, lastTuple[0])
    age_spinbox.delete(0, tk.END)
    age_spinbox.insert(0, lastTuple[1])
    email_entry.delete(0, tk.END)
    email_entry.insert(0, lastTuple[2])
    id1_entry.delete(0, tk.END)
    id1_entry.insert(0, lastTuple[3])


# Add this above the Treeview in the student frame
search_label = tk.Label(student, text="Search by Name or ID:")
search_label.grid(row=3, column=0, padx=10, pady=5)

search_entry = tk.Entry(student)
search_entry.grid(row=3, column=1, padx=10, pady=5)

search_button = tk.Button(student, text="Search",
                          command=lambda: search_student(search_entry.get()))
search_button.grid(row=3, column=2, padx=10, pady=5)

clear_button = tk.Button(student, text="Clear Search",
                         command=load_trv_with_json)  # To reload all data
clear_button.grid(row=3, column=3, padx=10, pady=5)


def register_student_for_course():
    """
    Registers a student for a course based on the selected values.

    The function retrieves the selected student and course, updates the student's registered
    courses, and updates the course's enrolled students.

    Displays an info message upon successful registration or a warning if an error occurs.
    """
    selected_course = course_dropdown.get()
    student_name = n_entry.get()

    student = search_student(student_name)
    if student and selected_course:
        student.register_course(selected_course)

        course = next(
            (c for c in course_data_list if c['course_name'] == selected_course), None)
        if course:
            if student_name not in course['enrolled_students']:
                course['enrolled_students'].append(student_name)

        save_json_to_file()

        messagebox.showinfo(
            "Success", f"{student_name} has been registered for {selected_course}")
    else:
        messagebox.showwarning("Error", "Student or Course not found!")


# Add a button to trigger the registration
register_button = tk.Button(
    student, text="Register for Course", command=register_student_for_course)
register_button.grid(row=2, column=2, padx=10, pady=5)

trv.bind("<ButtonRelease>", MouseButtonUpCallBack)


ButtonFrame = tk.LabelFrame(
    student, text='', bg="lightgray", font=('Consolas', 14))
ButtonFrame.grid(row=5, column=0, columnspan=6)

btnShow = tk.Button(ButtonFrame, text="Print", padx=20,
                    pady=10, command=print_all_entries)
btnShow.pack(side=tk.LEFT)

btnAdd = tk.Button(ButtonFrame, text="Add", padx=20,
                   pady=10, command=add_entry)
btnAdd.pack(side=tk.LEFT)

btnUpdate = tk.Button(ButtonFrame, text="Update", padx=20,
                      pady=10, command=update_entry)
btnUpdate.pack(side=tk.LEFT)

btnDelete = tk.Button(ButtonFrame, text="Delete", padx=20,
                      pady=10, command=delete_entry)
btnDelete.pack(side=tk.LEFT)

btnClear = tk.Button(ButtonFrame, text="Clear",
                     padx=20, pady=10, command=cancel)
btnClear.pack(side=tk.LEFT)

btnExit = tk.Button(ButtonFrame, text="Exit", padx=20,
                    pady=10, command=window.quit)
btnExit.pack(side=tk.LEFT)

load_json_from_file()
load_trv_with_json()


# --- INSTRUCTOR SECTION ---

def load_trv_with_instructor_data():
    """
    Loads instructor data into the TreeView widget from the global instructor data list.
    """
    global instructor_data_list

    remove_all_data_from_trv_instructor()

    rowIndex = 1

    for key in instructor_data_list:
        iName = key["n_entry"]
        iAge = key["Age"]
        iEmail = key["email"]
        iID = key["id"]
        trv_instructor.insert('', index='end', iid=rowIndex,
                              text="", values=(iName, iAge, iEmail, iID))
        rowIndex += 1


# creating the instructor label frame inside the frame
instructor = tk.LabelFrame(instructor_frame, text="New Instructor")
instructor.grid(row=1, column=0, sticky="news", padx=20, pady=10)

# Creating all the widget inside the instructor frame
nameInstructor = tk.Label(instructor, text="Name:")
nameInstructor.grid(row=0, column=0)

ageInstructor = tk.Label(instructor, text="Age:")
ageInstructor.grid(row=0, column=2)

emailInstructor = tk.Label(instructor, text="Email:")
emailInstructor.grid(row=0, column=3)

idInstructor = tk.Label(instructor, text="ID:")
idInstructor.grid(row=0, column=4)

name_entry_Instructor = tk.Entry(instructor)
name_entry_Instructor.grid(row=1, column=0)
age_spinbox_Instructor = tk.Spinbox(instructor, from_=25, to=100)
age_spinbox_Instructor.grid(row=1, column=2)
email_entry_Instructor = tk.Entry(instructor)
email_entry_Instructor.grid(row=1, column=3)
id_entry_Instructor = tk.Entry(instructor)
id_entry_Instructor.grid(row=1, column=4)


search_label_instructor = tk.Label(instructor, text="Search by Name or ID:")
search_label_instructor.grid(row=2, column=0, padx=10, pady=5)

search_entry_instructor = tk.Entry(instructor)
search_entry_instructor.grid(row=2, column=1, padx=10, pady=5)

search_button_instructor = tk.Button(
    instructor, text="Search", command=lambda: search_instructor(search_entry_instructor.get()))
search_button_instructor.grid(row=2, column=2, padx=10, pady=5)

clear_button_instructor = tk.Button(instructor, text="Clear Search",
                                    command=load_trv_with_instructor_data)  # To reload all instructor data
clear_button_instructor.grid(row=2, column=3, padx=10, pady=5)

# Add a Treeview to display instructor data
trv_instructor = ttk.Treeview(instructor, columns=(
    1, 2, 3, 4), show="headings", height="16")
trv_instructor.grid(row=6, column=0, sticky="news", rowspan=16, columnspan=4)

trv_instructor.heading(1, text="Name", anchor="center")
trv_instructor.heading(2, text="Age", anchor="center")
trv_instructor.heading(3, text="Email", anchor="center")
trv_instructor.heading(4, text="ID", anchor="center")

trv_instructor.column("#1", anchor="w", width=140, stretch=True)
trv_instructor.column("#2", anchor="w", width=140, stretch=True)
trv_instructor.column("#3", anchor="w", width=140, stretch=True)
trv_instructor.column("#4", anchor="w", width=140, stretch=True)

# --- FUNCTIONS FOR INSTRUCTORS ---


def search_instructor(search_value):
    """
    Searches and displays instructors by name or ID in the TreeView based on the search value.
    """
    # Clear current Treeview for instructors
    remove_all_data_from_trv_instructor()

    # Search for instructors matching by name or ID
    rowIndex = 1
    for key in instructor_data_list:
        if search_value.lower() in key["n_entry"].lower() or search_value == key["id"]:
            trv_instructor.insert('', index='end', iid=rowIndex, text="", values=(
                key["n_entry"], key["Age"], key["email"], key["id"]))
            rowIndex += 1

    # If no match found
    if rowIndex == 1:
        messagebox.showinfo(
            "Search Result", "No instructor found with that Name or ID")


def remove_all_data_from_trv_instructor():
    """
    Removes all current data from the instructor TreeView.
    """
    for item in trv_instructor.get_children():
        trv_instructor.delete(item)


def clear_instructor_fields():
    """
    Clears all input fields for instructor details.
    """
    name_entry_Instructor.delete(0, tk.END)
    age_spinbox_Instructor.delete(0, tk.END)
    email_entry_Instructor.delete(0, tk.END)
    id_entry_Instructor.delete(0, tk.END)


def find_instructor_row(value):
    """
    Finds and returns the index of an instructor by name. Returns -1 if not found.
    """
    global instructor_data_list
    row = 0
    found = False

    for rec in instructor_data_list:
        if rec["n_entry"] == value:
            found = True
            break
        row += 1

    if found:
        return row
    return -1


def add_entry_instructor():
    """
    Adds a new instructor entry to the global list and updates the TreeView.
    """
    Name = name_entry_Instructor.get()
    Age = age_spinbox_Instructor.get()
    Email = email_entry_Instructor.get()
    ID = id_entry_Instructor.get()

    process_instructor_request('_INSERT_', Name, Age, Email, ID)


def update_entry_instructor():
    """
    Updates the selected instructor's details and refreshes the TreeView.
    """
    Name = name_entry_Instructor.get()
    Age = age_spinbox_Instructor.get()
    Email = email_entry_Instructor.get()
    ID = id_entry_Instructor.get()

    process_instructor_request('_UPDATE_', Name, Age, Email, ID)


def delete_entry_instructor():
    """
    Deletes the selected instructor from the list and updates the TreeView.
    """
    Name = name_entry_Instructor.get()
    process_instructor_request('_DELETE_', Name, None, None, None)


def process_instructor_request(command_type, name_value, age_value, email_value, id_value):
    """
    Processes insert, update, or delete requests for instructor data and refreshes the TreeView.
    """
    global instructor_data_list

    if command_type == "_UPDATE_":
        row = find_instructor_row(name_value)
        if row >= 0:
            data = {"n_entry": name_value, "Age": age_value,
                    "email": email_value, "id": id_value}
            instructor_data_list[row] = data

    if command_type == "_INSERT_":
        data = {"n_entry": name_value, "Age": age_value,
                "email": email_value, "id": id_value}
        instructor_data_list.append(data)

    if command_type == "_DELETE_":
        row = find_instructor_row(name_value)
        if row >= 0:
            del instructor_data_list[row]

    load_trv_with_instructor_data()
    clear_instructor_fields()

# Bind instructor TreeView selection


def MouseButtonUpCallBackInstructor(event):
    """
    Loads the selected instructor's details into the input fields when clicked in the TreeView.
    """
    currentRowIndex = trv_instructor.selection()[0]
    lastTuple = (trv_instructor.item(currentRowIndex, "values"))
    load_instructor_field_with_row_data(lastTuple)


def load_instructor_field_with_row_data(_tuple):
    """
    Fills the input fields with instructor data from the selected row in the TreeView.
    """
    if len(_tuple) == 0:
        return

    name_entry_Instructor.delete(0, tk.END)
    name_entry_Instructor.insert(0, _tuple[0])
    age_spinbox_Instructor.delete(0, tk.END)
    age_spinbox_Instructor.insert(0, _tuple[1])
    email_entry_Instructor.delete(0, tk.END)
    email_entry_Instructor.insert(0, _tuple[2])
    id_entry_Instructor.delete(0, tk.END)
    id_entry_Instructor.insert(0, _tuple[3])


trv_instructor.bind("<ButtonRelease>", MouseButtonUpCallBackInstructor)

# --- INSTRUCTOR BUTTONS ---

ButtonFrameInstructor = tk.LabelFrame(
    instructor, text='', bg="lightgray", font=('Consolas', 14))
ButtonFrameInstructor.grid(row=5, column=0, columnspan=6)

btnAddInstructor = tk.Button(
    ButtonFrameInstructor, text="Add", padx=20, pady=10, command=add_entry_instructor)
btnAddInstructor.pack(side=tk.LEFT)

btnUpdateInstructor = tk.Button(
    ButtonFrameInstructor, text="Update", padx=20, pady=10, command=update_entry_instructor)
btnUpdateInstructor.pack(side=tk.LEFT)

btnDeleteInstructor = tk.Button(
    ButtonFrameInstructor, text="Delete", padx=20, pady=10, command=delete_entry_instructor)
btnDeleteInstructor.pack(side=tk.LEFT)

btnClearInstructor = tk.Button(
    ButtonFrameInstructor, text="Clear", padx=20, pady=10, command=clear_instructor_fields)
btnClearInstructor.pack(side=tk.LEFT)

load_trv_with_instructor_data()
# creating course label frame
course = tk.LabelFrame(course_frame, text="New course")
course.grid(row=2, column=0, sticky="news", padx=20, pady=10)

# creating widget inside the course label frame
name = tk.Label(course, text="Course Name:")
name.grid(row=0, column=0)

id = tk.Label(course, text="ID:")
id.grid(row=0, column=1)

name_entry = tk.Entry(course)
name_entry.grid(row=1, column=0)
id_entry = tk.Entry(course)
id_entry.grid(row=1, column=1)

Instructor = tk.Label(course, text="Assign Instructor")
Instructor.grid(row=0, column=2)

Instructor = ttk.Combobox(course)
# I have to fix this and add the available instructors
Instructor.grid(row=1, column=2)

submit_button = tk.Button(course, text="Submit")
submit_button.grid(row=2, column=0)

# Add search functionality for course frame


def load_trv_with_course_data():
    """
    Loads course data into the TreeView widget from the global course data list.
    Clears existing entries before adding new ones.
    """
    global course_data_list
    # Clear the current content in the course TreeView
    remove_all_data_from_trv_course()

    # Populate TreeView with course data
    rowIndex = 1
    for course in course_data_list:
        trv_course.insert('', index='end', iid=rowIndex, text="", values=(
            course["course_name"], course["id"], course["instructor_name"]))
        rowIndex += 1


search_label_course = tk.Label(course, text="Search by Course Name or ID:")
search_label_course.grid(row=2, column=0, padx=10, pady=5)

search_entry_course = tk.Entry(course)
search_entry_course.grid(row=2, column=1, padx=10, pady=5)

search_button_course = tk.Button(
    course, text="Search", command=lambda: search_course(search_entry_course.get()))
search_button_course.grid(row=2, column=2, padx=10, pady=5)

clear_button_course = tk.Button(
    course, text="Clear Search", command=load_trv_with_course_data)
clear_button_course.grid(row=2, column=3, padx=10, pady=5)
# Add TreeView to display course data
trv_course = ttk.Treeview(course, columns=(
    1, 2, 3), show="headings", height="16")
trv_course.grid(row=6, column=0, sticky="news", rowspan=16, columnspan=4)

trv_course.heading(1, text="Course Name", anchor="center")
trv_course.heading(2, text="Course ID", anchor="center")
trv_course.heading(3, text="Instructor", anchor="center")

trv_course.column("#1", anchor="w", width=140, stretch=True)
trv_course.column("#2", anchor="w", width=140, stretch=True)
trv_course.column("#3", anchor="w", width=140, stretch=True)

for widget in course.winfo_children():
    widget.grid_configure(padx=10, pady=5)


# -------courses functions--------
def search_course(search_value):
    """
    Searches and displays courses by name or ID in the TreeView based on the search value.
    """
    # Clear current Treeview for courses
    remove_all_data_from_trv_course()

    # Search for courses matching by name or ID
    rowIndex = 1
    for key in course_data_list:
        if search_value.lower() in key["course_name"].lower() or search_value == key["id"]:
            trv_course.insert('', index='end', iid=rowIndex, text="", values=(
                key["course_name"], key["id"], key["instructor_name"]))
            rowIndex += 1

    # If no match found
    if rowIndex == 1:
        messagebox.showinfo(
            "Search Result", "No course found with that Name or ID")


def remove_all_data_from_trv_course():
    """
    Removes all current data from the course TreeView.
    """
    for item in trv_course.get_children():
        trv_course.delete(item)


def clear_course_fields():
    """
    Clears all input fields for course details.
    """
    name_entry.delete(0, tk.END)
    id_entry.delete(0, tk.END)
    Instructor.set('')  # Clear the instructor dropdown


def find_course_row(value):
    """
    Finds and returns the index of a course by name. Returns -1 if not found.
    """
    global course_data_list
    row = 0
    found = False

    for rec in course_data_list:
        if rec["course_name"] == value:
            found = True
            break
        row += 1

    if found:
        return row
    return -1


def add_entry_course():
    """
    Adds a new course entry to the global list and updates the TreeView.
    """
    course_name = name_entry.get()
    course_id = id_entry.get()
    instructor_name = Instructor.get()

    process_course_request('_INSERT_', course_name, course_id, instructor_name)


def update_entry_course():
    """
    Updates the selected course's details and refreshes the TreeView.
    """
    course_name = name_entry.get()
    course_id = id_entry.get()
    instructor_name = Instructor.get()

    process_course_request('_UPDATE_', course_name, course_id, instructor_name)


def delete_entry_course():
    """
    Deletes the selected course from the list and updates the TreeView.
    """
    course_name = name_entry.get()
    process_course_request('_DELETE_', course_name, None, None)


def process_course_request(command_type, course_name_value, course_id_value, instructor_name_value):
    """
    Processes insert, update, or delete requests for course data and refreshes the TreeView.
    """
    global course_data_list

    if command_type == "_UPDATE_":
        row = find_course_row(course_name_value)
        if row >= 0:
            data = {"course_name": course_name_value,
                    "id": course_id_value, "instructor_name": instructor_name_value}
            course_data_list[row] = data

    if command_type == "_INSERT_":
        data = {"course_name": course_name_value,
                "id": course_id_value, "instructor_name": instructor_name_value}
        course_data_list.append(data)

    if command_type == "_DELETE_":
        row = find_course_row(course_name_value)
        if row >= 0:
            del course_data_list[row]

    load_trv_with_course_data()
    clear_course_fields()


# Dropdown for available instructors in course frame
Instructor = ttk.Combobox(course)
Instructor.grid(row=1, column=2)
Instructor['values'] = [instructor['n_entry']
                        # Populate with instructor names
                        for instructor in instructor_data_list]
Instructor.set('')  # Clear the default value


def MouseButtonUpCallBackCourse(event):
    """
    Loads the selected course's details into the input fields when clicked in the TreeView.
    """
    currentRowIndex = trv_course.selection()[0]
    lastTuple = (trv_course.item(currentRowIndex, "values"))
    load_course_field_with_row_data(lastTuple)


def load_course_field_with_row_data(_tuple):
    """
    Fills the input fields with course data from the selected row in the TreeView.
    """
    if len(_tuple) == 0:
        return

    name_entry.delete(0, tk.END)
    name_entry.insert(0, _tuple[0])
    id_entry.delete(0, tk.END)
    id_entry.insert(0, _tuple[1])
    Instructor.set(_tuple[2])  # Set the instructor in the dropdown


# --- COURSE BUTTONS ---
ButtonFrameCourse = tk.LabelFrame(
    course, text='', bg="lightgray", font=('Consolas', 14))
ButtonFrameCourse.grid(row=5, column=0, columnspan=6)

btnAddCourse = tk.Button(ButtonFrameCourse, text="Add",
                         padx=20, pady=10, command=add_entry_course)
btnAddCourse.pack(side=tk.LEFT)

btnUpdateCourse = tk.Button(
    ButtonFrameCourse, text="Update", padx=20, pady=10, command=update_entry_course)
btnUpdateCourse.pack(side=tk.LEFT)

btnDeleteCourse = tk.Button(
    ButtonFrameCourse, text="Delete", padx=20, pady=10, command=delete_entry_course)
btnDeleteCourse.pack(side=tk.LEFT)

btnClearCourse = tk.Button(
    ButtonFrameCourse, text="Clear", padx=20, pady=10, command=clear_course_fields)
btnClearCourse.pack(side=tk.LEFT)

trv_course.bind("<ButtonRelease>", MouseButtonUpCallBackCourse)


window.mainloop()
