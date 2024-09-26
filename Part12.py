import json
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
        self.enrolled_students = enrolled_students if enrolled_students is not None else []  # List of Student objects

    def add_student(self, student):
        self.enrolled_students.append(student)

