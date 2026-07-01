# factory.py

import random
from data import Student, Teacher


# 20 sample names
names = [
    "Sojib",
    "Tanvir",
    "Fahim",
    "Mahadi",
    "Sakib",
    "Nafis",
    "Rifat",
    "Muntasir",
    "Rakib",
    "Hasan",
    "Mim",
    "Nabila",
    "Sadia",
    "Toma",
    "Anika",
    "Rasel",
    "Siam",
    "Jubayer",
    "Shakil",
    "Raihan"
]


roles = [
    "Project Leader",
    "Backend Developer",
    "Frontend Developer",
    "Database Administrator",
    "AI Engineer",
    "Software Tester",
    "UI Designer",
    "DevOps Engineer"
]


departments = [
    "Computer Science",
    "Software Engineering",
    "Information Technology",
    "Data Science"
]


class DataFactory:

    @staticmethod
    def create_data(data_type, **kwargs):

        if data_type.lower() == "student":

            return Student(
                kwargs["student_id"],
                kwargs["name"],
                kwargs["email"],
                kwargs["role"],
                kwargs["department"]
            )

        elif data_type.lower() == "teacher":

            return Teacher(
                kwargs["teacher_id"],
                kwargs["name"],
                kwargs["email"],
                kwargs["department"]
            )

        raise ValueError("Invalid data type")


    @staticmethod
    def create_random_student():

        name = random.choice(names)

        return Student(
            student_id=f"CSE{random.randint(22001,22999)}",
            name=name,
            email=f"{name.lower()}@du.ac.bd",
            role=random.choice(roles),
            department=random.choice(departments)
        )


    @staticmethod
    def create_random_teacher():

        name = random.choice(names)

        return Teacher(
            teacher_id=f"T{random.randint(100,999)}",
            name=f"Dr {name}",
            email=f"{name.lower()}@du.ac.bd",
            department=random.choice(departments)
        )


    @staticmethod
    def create_bulk_students(count=10):

        students = []

        for _ in range(count):

            student = DataFactory.create_random_student()

            students.append(
                student.to_dict()
            )

        return students