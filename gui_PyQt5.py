import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox, QComboBox, QFileDialog, QInputDialog
)
import csv
import json  # For saving and loading data in JSON format

# Global lists to store students, instructors, and courses
students = []
instructors = []
courses = []

class SchoolManagementSystem(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("School Management System")
        self.setGeometry(100, 100, 1000, 800)

        # Central widget
        widget = QWidget()
        self.setCentralWidget(widget)

        # Main layout
        main_layout = QVBoxLayout()

        # Form layouts for students, instructors, and courses
        form_layout = QVBoxLayout()

        # Student form
        student_form = QHBoxLayout()
        global student_id_input, student_name_input, student_email_input
        student_id_input = QLineEdit()
        student_name_input = QLineEdit()
        student_email_input = QLineEdit()
        student_form.addWidget(QLabel("Student ID"))
        student_form.addWidget(student_id_input)
        student_form.addWidget(QLabel("Student Name"))
        student_form.addWidget(student_name_input)
        student_form.addWidget(QLabel("Student Email"))
        student_form.addWidget(student_email_input)
        add_student_button = QPushButton("Add Student")
        add_student_button.clicked.connect(self.add_student)
        student_form.addWidget(add_student_button)

        # Instructor form
        instructor_form = QHBoxLayout()
        global instructor_id_input, instructor_name_input, instructor_email_input
        instructor_id_input = QLineEdit()
        instructor_name_input = QLineEdit()
        instructor_email_input = QLineEdit()
        instructor_form.addWidget(QLabel("Instructor ID"))
        instructor_form.addWidget(instructor_id_input)
        instructor_form.addWidget(QLabel("Instructor Name"))
        instructor_form.addWidget(instructor_name_input)
        instructor_form.addWidget(QLabel("Instructor Email"))
        instructor_form.addWidget(instructor_email_input)
        add_instructor_button = QPushButton("Add Instructor")
        add_instructor_button.clicked.connect(self.add_instructor)
        instructor_form.addWidget(add_instructor_button)

        # Course form
        course_form = QHBoxLayout()
        global course_id_input, course_name_input
        course_id_input = QLineEdit()
        course_name_input = QLineEdit()
        course_form.addWidget(QLabel("Course ID"))
        course_form.addWidget(course_id_input)
        course_form.addWidget(QLabel("Course Name"))
        course_form.addWidget(course_name_input)
        add_course_button = QPushButton("Add Course")
        add_course_button.clicked.connect(self.add_course)
        course_form.addWidget(add_course_button)

        form_layout.addLayout(student_form)
        form_layout.addLayout(instructor_form)
        form_layout.addLayout(course_form)

        # Dropdown for selecting students, instructors, and courses
        dropdown_layout = QHBoxLayout()
        global student_dropdown, instructor_dropdown, course_dropdown
        student_dropdown = QComboBox()
        instructor_dropdown = QComboBox()
        course_dropdown = QComboBox()

        dropdown_layout.addWidget(QLabel("Select Student"))
        dropdown_layout.addWidget(student_dropdown)
        dropdown_layout.addWidget(QLabel("Select Instructor"))
        dropdown_layout.addWidget(instructor_dropdown)
        dropdown_layout.addWidget(QLabel("Select Course"))
        dropdown_layout.addWidget(course_dropdown)

        # Buttons for registration and assignment
        register_button = QPushButton("Register Student for Course")
        register_button.clicked.connect(self.register_student_for_course)
        assign_button = QPushButton("Assign Instructor to Course")
        assign_button.clicked.connect(self.assign_instructor_to_course)
        dropdown_layout.addWidget(register_button)
        dropdown_layout.addWidget(assign_button)

        # Search layout
        search_layout = QHBoxLayout()
        global search_input
        search_input = QLineEdit()
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_records)
        search_layout.addWidget(QLabel("Search"))
        search_layout.addWidget(search_input)
        search_layout.addWidget(search_button)

        # Tables to display students, instructors, and courses
        global students_table, instructors_table, courses_table
        students_table = QTableWidget(0, 4)
        students_table.setHorizontalHeaderLabels(["Student ID", "Student Name", "Email", "Courses"])

        instructors_table = QTableWidget(0, 4)
        instructors_table.setHorizontalHeaderLabels(["Instructor ID", "Instructor Name", "Email", "Courses"])

        courses_table = QTableWidget(0, 2)
        courses_table.setHorizontalHeaderLabels(["Course ID", "Course Name"])

        # Save, Load, Export buttons
        save_button = QPushButton("Save Data")
        save_button.clicked.connect(self.save_data)
        load_button = QPushButton("Load Data")
        load_button.clicked.connect(self.load_data)
        export_button = QPushButton("Export to CSV")
        export_button.clicked.connect(self.export_to_csv)

        # Edit and Delete buttons
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit_record)
        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete_record)

        # Adding widgets to the main layout
        main_layout.addLayout(form_layout)
        main_layout.addLayout(dropdown_layout)
        main_layout.addLayout(search_layout)
        main_layout.addWidget(students_table)
        main_layout.addWidget(instructors_table)
        main_layout.addWidget(courses_table)
        main_layout.addWidget(save_button)
        main_layout.addWidget(load_button)
        main_layout.addWidget(export_button)
        main_layout.addWidget(edit_button)
        main_layout.addWidget(delete_button)

        widget.setLayout(main_layout)

        # Initial update of dropdowns
        self.update_dropdowns()

    def update_dropdowns(self):
        student_dropdown.clear()
        instructor_dropdown.clear()
        course_dropdown.clear()

        for student in students:
            student_dropdown.addItem(student['ID'])
        for instructor in instructors:
            instructor_dropdown.addItem(instructor['ID'])
        for course in courses:
            course_dropdown.addItem(course['ID'])

    def add_student(self):
        global students
        student_id = student_id_input.text().strip()
        student_name = student_name_input.text().strip()
        student_email = student_email_input.text().strip()

        if student_id == "" or student_name == "" or student_email == "":
            QMessageBox.warning(self, "Input Error", "All student fields are required.")
            return

        students.append({"ID": student_id, "Name": student_name, "Email": student_email, "Courses": []})
        student_id_input.clear()
        student_name_input.clear()
        student_email_input.clear()
        self.update_display()
        self.update_dropdowns()
        QMessageBox.information(self, "Success", "Student added successfully!")

    def add_instructor(self):
        global instructors
        instructor_id = instructor_id_input.text().strip()
        instructor_name = instructor_name_input.text().strip()
        instructor_email = instructor_email_input.text().strip()

        if instructor_id == "" or instructor_name == "" or instructor_email == "":
            QMessageBox.warning(self, "Input Error", "All instructor fields are required.")
            return

        instructors.append({"ID": instructor_id, "Name": instructor_name, "Email": instructor_email, "Courses": []})
        instructor_id_input.clear()
        instructor_name_input.clear()
        instructor_email_input.clear()
        self.update_display()
        self.update_dropdowns()
        QMessageBox.information(self, "Success", "Instructor added successfully!")

    def add_course(self):
        global courses
        course_id = course_id_input.text().strip()
        course_name = course_name_input.text().strip()

        if course_id == "" or course_name == "":
            QMessageBox.warning(self, "Input Error", "All course fields are required.")
            return

        courses.append({"ID": course_id, "Name": course_name})
        course_id_input.clear()
        course_name_input.clear()
        self.update_display()
        self.update_dropdowns()
        QMessageBox.information(self, "Success", "Course added successfully!")

    def register_student_for_course(self):
        global students
        student_id = student_dropdown.currentText()
        course_id = course_dropdown.currentText()

        for student in students:
            if student['ID'] == student_id:
                student['Courses'].append(course_id)
                self.update_display()
                QMessageBox.information(self, "Success", f"Student {student_id} registered for course {course_id}!")
                return

        QMessageBox.warning(self, "Error", "Student not found.")

    def assign_instructor_to_course(self):
        global instructors
        instructor_id = instructor_dropdown.currentText()
        course_id = course_dropdown.currentText()

        for instructor in instructors:
            if instructor['ID'] == instructor_id:
                instructor['Courses'].append(course_id)
                self.update_display()
                QMessageBox.information(self, "Success", f"Instructor {instructor_id} assigned to course {course_id}!")
                return

        QMessageBox.warning(self, "Error", "Instructor not found.")

    def save_data(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Data", "", "JSON Files (*.json)")
        if file_path:
            data = {
                "students": students,
                "instructors": instructors,
                "courses": courses
            }
            with open(file_path, 'w') as json_file:
                json.dump(data, json_file)
            QMessageBox.information(self, "Success", "Data saved successfully!")

    def load_data(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Load Data", "", "JSON Files (*.json)")
        if file_path:
            with open(file_path, 'r') as json_file:
                data = json.load(json_file)
                global students, instructors, courses
                students = data.get("students", [])
                instructors = data.get("instructors", [])
                courses = data.get("courses", [])
            self.update_display()
            self.update_dropdowns()
            QMessageBox.information(self, "Success", "Data loaded successfully!")

    def export_to_csv(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Export to CSV", "", "CSV Files (*.csv)")
        if file_path:
            with open(file_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Students"])
                writer.writerow(["ID", "Name", "Email", "Courses"])
                for student in students:
                    writer.writerow([student['ID'], student['Name'], student['Email'], ', '.join(student['Courses'])])
                writer.writerow([])
                writer.writerow(["Instructors"])
                writer.writerow(["ID", "Name", "Email", "Courses"])
                for instructor in instructors:
                    writer.writerow([instructor['ID'], instructor['Name'], instructor['Email'], ', '.join(instructor['Courses'])])
                writer.writerow([])
                writer.writerow(["Courses"])
                writer.writerow(["ID", "Name"])
                for course in courses:
                    writer.writerow([course['ID'], course['Name']])
            QMessageBox.information(self, "Success", "Data exported successfully!")

    def search_records(self):
        search_text = search_input.text().strip()
        results = []
        for student in students:
            if search_text.lower() in student['ID'].lower() or search_text.lower() in student['Name'].lower():
                results.append(f"Student ID: {student['ID']}, Name: {student['Name']}, Email: {student['Email']}, Courses: {', '.join(student['Courses'])}")
        for instructor in instructors:
            if search_text.lower() in instructor['ID'].lower() or search_text.lower() in instructor['Name'].lower():
                results.append(f"Instructor ID: {instructor['ID']}, Name: {instructor['Name']}, Email: {instructor['Email']}, Courses: {', '.join(instructor['Courses'])}")
        for course in courses:
            if search_text.lower() in course['ID'].lower() or search_text.lower() in course['Name'].lower():
                results.append(f"Course ID: {course['ID']}, Name: {course['Name']}")

        if results:
            QMessageBox.information(self, "Search Results", "\n".join(results))
        else:
            QMessageBox.information(self, "Search Results", "No matching records found.")

    def edit_record(self):
        selected_student_id = student_dropdown.currentText()
        selected_instructor_id = instructor_dropdown.currentText()
        selected_course_id = course_dropdown.currentText()

        # Edit Student
        for student in students:
            if student['ID'] == selected_student_id:
                new_name, ok = QInputDialog.getText(self, "Edit Student", "Enter new student name:")
                if ok:
                    student['Name'] = new_name
                new_email, ok = QInputDialog.getText(self, "Edit Student", "Enter new student email:")
                if ok:
                    student['Email'] = new_email
                self.update_display()
                QMessageBox.information(self, "Success", "Student record updated successfully!")
                return

        # Edit Instructor
        for instructor in instructors:
            if instructor['ID'] == selected_instructor_id:
                new_name, ok = QInputDialog.getText(self, "Edit Instructor", "Enter new instructor name:")
                if ok:
                    instructor['Name'] = new_name
                new_email, ok = QInputDialog.getText(self, "Edit Instructor", "Enter new instructor email:")
                if ok:
                    instructor['Email'] = new_email
                self.update_display()
                QMessageBox.information(self, "Success", "Instructor record updated successfully!")
                return

        # Edit Course
        for course in courses:
            if course['ID'] == selected_course_id:
                new_name, ok = QInputDialog.getText(self, "Edit Course", "Enter new course name:")
                if ok:
                    course['Name'] = new_name
                self.update_display()
                QMessageBox.information(self, "Success", "Course record updated successfully!")
                return

    def delete_record(self):
        selected_student_id = student_dropdown.currentText()
        selected_instructor_id = instructor_dropdown.currentText()
        selected_course_id = course_dropdown.currentText()

        global students, instructors, courses

        # Delete Student
        for student in students:
            if student['ID'] == selected_student_id:
                students.remove(student)
                self.update_display()
                self.update_dropdowns()
                QMessageBox.information(self, "Success", "Student record deleted successfully!")
                return

        # Delete Instructor
        for instructor in instructors:
            if instructor['ID'] == selected_instructor_id:
                instructors.remove(instructor)
                self.update_display()
                self.update_dropdowns()
                QMessageBox.information(self, "Success", "Instructor record deleted successfully!")
                return

        # Delete Course
        for course in courses:
            if course['ID'] == selected_course_id:
                courses.remove(course)
                self.update_display()
                self.update_dropdowns()
                QMessageBox.information(self, "Success", "Course record deleted successfully!")
                return

    def update_display(self):
        students_table.setRowCount(len(students))
        instructors_table.setRowCount(len(instructors))
        courses_table.setRowCount(len(courses))

        for row, student in enumerate(students):
            students_table.setItem(row, 0, QTableWidgetItem(student['ID']))
            students_table.setItem(row, 1, QTableWidgetItem(student['Name']))
            students_table.setItem(row, 2, QTableWidgetItem(student['Email']))
            students_table.setItem(row, 3, QTableWidgetItem(', '.join(student['Courses'])))

        for row, instructor in enumerate(instructors):
            instructors_table.setItem(row, 0, QTableWidgetItem(instructor['ID']))
            instructors_table.setItem(row, 1, QTableWidgetItem(instructor['Name']))
            instructors_table.setItem(row, 2, QTableWidgetItem(instructor['Email']))
            instructors_table.setItem(row, 3, QTableWidgetItem(', '.join(instructor['Courses'])))

        for row, course in enumerate(courses):
            courses_table.setItem(row, 0, QTableWidgetItem(course['ID']))
            courses_table.setItem(row, 1, QTableWidgetItem(course['Name']))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SchoolManagementSystem()
    window.show()
    sys.exit(app.exec_())
