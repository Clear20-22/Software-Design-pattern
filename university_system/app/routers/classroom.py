import uuid
from fastapi import APIRouter, Depends, HTTPException

from app.database import get_database
from app.models import EnrollRequest
from app.routers.auth import require_role, get_current_user

router = APIRouter(prefix="/classroom", tags=["Classroom"])


@router.post("/create")
def create_classroom(name: str, user=Depends(require_role("teacher", "admin"))):
    db = get_database()
    classroom_id = str(uuid.uuid4())
    db.classrooms.insert_one(
        {"classroom_id": classroom_id, "name": name, "teacher_id": user["user_id"]}
    )
    return {"classroom_id": classroom_id, "name": name}


@router.get("")
@router.get("/")
def list_classrooms(user=Depends(get_current_user)):
    db = get_database()
    if user["role"] in ["teacher", "admin"]:
        return list(db.classrooms.find({"teacher_id": user["user_id"]}, {"_id": 0}))
    else:
        enrollments = db.enrollments.find({"student_id": user["user_id"]})
        c_ids = [e["classroom_id"] for e in enrollments]
        return list(db.classrooms.find({"classroom_id": {"$in": c_ids}}, {"_id": 0}))


@router.post("/enroll")
def enroll_student(request: EnrollRequest, user=Depends(get_current_user)):
    db = get_database()
    if not db.classrooms.find_one({"classroom_id": request.classroom_id}):
        raise HTTPException(status_code=404, detail="Classroom not found")
    if not db.users.find_one({"user_id": request.student_id, "role": "student"}):
        raise HTTPException(status_code=404, detail="Student not found")
    if db.enrollments.find_one(
        {"classroom_id": request.classroom_id, "student_id": request.student_id}
    ):
        raise HTTPException(status_code=400, detail="Already enrolled")

    db.enrollments.insert_one(
        {"classroom_id": request.classroom_id, "student_id": request.student_id}
    )
    return {"message": "Student enrolled successfully"}


@router.get("/{classroom_id}/students")
def list_students(classroom_id: str, user=Depends(get_current_user)):
    db = get_database()
    student_ids = [
        e["student_id"] for e in db.enrollments.find({"classroom_id": classroom_id})
    ]
    return list(db.users.find({"user_id": {"$in": student_ids}}, {"_id": 0, "password": 0}))
