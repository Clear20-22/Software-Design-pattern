"""
FACTORY PATTERN
---------------
UserFactory hides the decision of "which concrete class do I build for
this role?" from the rest of the app. Routers just call
UserFactory.create_user(role=..., ...) and get back the right object --
Student, Teacher or Admin -- without knowing those classes exist.
Adding a new role later (e.g. "librarian") only means registering a new
class here; no other file needs to change.
"""

from abc import ABC, abstractmethod


class BaseUser(ABC):
    def __init__(self, user_id: str, name: str, email: str):
        self.user_id = user_id
        self.name = name
        self.email = email

    @abstractmethod
    def get_role(self) -> str:
        ...

    @abstractmethod
    def get_dashboard_data(self) -> dict:
        ...


class Student(BaseUser):
    def get_role(self) -> str:
        return "student"

    def get_dashboard_data(self) -> dict:
        return {"role": "student", "message": "View your enrolled classrooms and notices."}


class Teacher(BaseUser):
    def get_role(self) -> str:
        return "teacher"

    def get_dashboard_data(self) -> dict:
        return {"role": "teacher", "message": "Manage your classrooms and post notices."}


class Admin(BaseUser):
    def get_role(self) -> str:
        return "admin"

    def get_dashboard_data(self) -> dict:
        return {"role": "admin", "message": "Full system access."}


class UserFactory:
    _registry = {
        "student": Student,
        "teacher": Teacher,
        "admin": Admin,
    }

    @staticmethod
    def create_user(role: str, user_id: str, name: str, email: str) -> BaseUser:
        role_key = role.lower().strip()
        user_class = UserFactory._registry.get(role_key)
        if user_class is None:
            raise ValueError(f"Unknown role: '{role}'. Allowed roles: {list(UserFactory._registry.keys())}")
        return user_class(user_id=user_id, name=name, email=email)
