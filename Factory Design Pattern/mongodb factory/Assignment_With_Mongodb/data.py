# data.py


class Student:

    def __init__(
        self,
        student_id,
        name,
        email,
        role,
        department
    ):

        self.student_id = student_id
        self.name = name
        self.email = email
        self.role = role
        self.department = department
        self.type = "Student"


    def to_dict(self):

        return {

            "type": self.type,

            "student_id": self.student_id,

            "name": self.name,

            "email": self.email,

            "role": self.role,

            "department": self.department
        }


class Teacher:

    def __init__(
        self,
        teacher_id,
        name,
        email,
        department
    ):

        self.teacher_id = teacher_id
        self.name = name
        self.email = email
        self.department = department
        self.type = "Teacher"


    def to_dict(self):

        return {

            "type": self.type,

            "teacher_id": self.teacher_id,

            "name": self.name,

            "email": self.email,

            "department": self.department
        }