from pydantic import BaseModel, EmailStr
from datetime import datetime


class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str  # "student" | "teacher" | "admin"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class NoticeCreateRequest(BaseModel):
    title: str
    content: str


class EnrollRequest(BaseModel):
    classroom_id: str
    student_id: str


class NotificationResponse(BaseModel):
    notice_id: str
    classroom_id: str
    title: str
    message: str
    is_read: bool
    created_at: datetime


class StudentScoreItem(BaseModel):
    student_id: str
    marks: float


class GradeEvaluationRequest(BaseModel):
    scores: list[StudentScoreItem]


class AssignmentCreateRequest(BaseModel):
    title: str
    description: str
    max_marks: float = 100.0
    deadline: str = ""


class AssignmentSubmitRequest(BaseModel):
    submission_text: str


class AssignmentTransitionRequest(BaseModel):
    action: str  # "publish" | "close" | "finalize" | "reopen"
