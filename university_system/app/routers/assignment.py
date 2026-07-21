import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException

from app.database import get_database
from app.models import (
    AssignmentCreateRequest,
    AssignmentSubmitRequest,
    AssignmentTransitionRequest,
)
from app.routers.auth import require_role, get_current_user
from app.states.assignment_state import AssignmentContext, AssignmentStateFactory
from app.observers.notice_board import NoticeBoardManager

router = APIRouter(tags=["Assignment Lifecycle & State Pattern"])
notice_board_manager = NoticeBoardManager()


@router.post("/classroom/{classroom_id}/assignment/create")
def create_assignment(
    classroom_id: str,
    request: AssignmentCreateRequest,
    user=Depends(require_role("teacher", "admin")),
):
    """
    Creates a new assignment starting in 'Draft' state (DraftState).
    """
    db = get_database()
    classroom = db.classrooms.find_one({"classroom_id": classroom_id})
    if not classroom:
        raise HTTPException(status_code=404, detail="Classroom not found")

    assignment_id = str(uuid.uuid4())
    context = AssignmentContext()  # starts in DraftState

    doc = {
        "assignment_id": assignment_id,
        "classroom_id": classroom_id,
        "title": request.title,
        "description": request.description,
        "max_marks": request.max_marks,
        "deadline": request.deadline,
        "state": context.get_state_name(),
        "created_by": user["user_id"],
        "created_at": datetime.utcnow(),
    }
    db.assignments.insert_one(doc)
    doc.pop("_id", None)
    return {"message": "Assignment created in Draft state", "assignment": doc}
    

@router.post("/assignment/{assignment_id}/transition")
async def transition_assignment_state(
    assignment_id: str,
    request: AssignmentTransitionRequest,
    user=Depends(require_role("teacher", "admin")),
):
    """
    --- State Pattern in Action ---
    Executes state transitions (publish, close, finalize, reopen) on the assignment.
    The AssignmentContext delegates the state change and rules to the current AssignmentState.
    """
    db = get_database()
    assignment = db.assignments.find_one({"assignment_id": assignment_id})
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    current_state_obj = AssignmentStateFactory.from_name(assignment.get("state", "draft"))
    context = AssignmentContext(current_state_obj)

    action = (request.action or "").lower().strip()
    try:
        if action == "publish":
            context.publish()
        elif action == "close":
            context.close_submissions()
        elif action == "finalize":
            context.finalize_grades()
        elif action == "reopen":
            context.reopen()
        else:
            raise HTTPException(status_code=400, detail=f"Invalid action: '{action}'. Allowed: publish, close, finalize, reopen")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    new_state_name = context.get_state_name()
    new_state_label = context.get_display_label()

    db.assignments.update_one(
        {"assignment_id": assignment_id},
        {"$set": {"state": new_state_name, "updated_at": datetime.utcnow()}},
    )

    # --- Observer Pattern Fan-out Notification on State Change ---
    if action in ["publish", "finalize"]:
        board = notice_board_manager.get_notice_board(assignment["classroom_id"])
        notice_payload = {
            "notice_id": str(uuid.uuid4()),
            "classroom_id": assignment["classroom_id"],
            "title": f"Assignment Notice: {assignment['title']}",
            "content": f"Assignment '{assignment['title']}' status updated to '{new_state_label}'.",
            "posted_by": user["user_id"],
            "created_at": datetime.utcnow(),
        }
        await board.notify(notice_payload)

    return {
        "message": f"Assignment state transitioned to '{new_state_name}' ({new_state_label})",
        "assignment_id": assignment_id,
        "state": new_state_name,
        "display_label": new_state_label,
    }


@router.post("/assignment/{assignment_id}/submit")
def submit_assignment(
    assignment_id: str,
    request: AssignmentSubmitRequest,
    user=Depends(get_current_user),
):
    """
    --- State Pattern Control ---
    Students can submit work ONLY when the assignment's current State allows submissions (OpenState).
    """
    db = get_database()
    assignment = db.assignments.find_one({"assignment_id": assignment_id})
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    current_state_obj = AssignmentStateFactory.from_name(assignment.get("state", "draft"))
    context = AssignmentContext(current_state_obj)

    # State Pattern Rule Check
    if not context.can_submit():
        raise HTTPException(
            status_code=400,
            detail=f"Submissions are blocked. Current state is '{context.get_display_label()}'."
        )

    submission_doc = {
        "assignment_id": assignment_id,
        "student_id": user["user_id"],
        "student_name": user.get("name", "Student"),
        "submission_text": request.submission_text,
        "submitted_at": datetime.utcnow(),
    }

    db.assignment_submissions.update_one(
        {"assignment_id": assignment_id, "student_id": user["user_id"]},
        {"$set": submission_doc},
        upsert=True,
    )
    submission_doc.pop("_id", None)
    return {"message": "Assignment submission recorded successfully", "submission": submission_doc}


@router.get("/classroom/{classroom_id}/assignments")
def list_classroom_assignments(classroom_id: str, user=Depends(get_current_user)):
    """
    Returns all assignments for a classroom with state indicators, submission stats,
    deadlines, and submission details for teachers/admins.
    """
    db = get_database()
    assignments = list(db.assignments.find({"classroom_id": classroom_id}, {"_id": 0}))

    for item in assignments:
        state_obj = AssignmentStateFactory.from_name(item.get("state", "draft"))
        context = AssignmentContext(state_obj)
        item["display_label"] = context.get_display_label()
        item["can_submit"] = context.can_submit()
        item["can_edit"] = context.can_edit()

        # Fetch submissions
        subs = list(db.assignment_submissions.find({"assignment_id": item["assignment_id"]}, {"_id": 0}))
        item["submissions_count"] = len(subs)

        # Teachers/Admins get full submission list (who submitted & what they submitted)
        if user["role"] in ["teacher", "admin"]:
            item["submissions_list"] = subs

        # Fetch current user's submission if student
        if user["role"] == "student":
            sub = next((s for s in subs if s.get("student_id") == user["user_id"]), None)
            item["my_submission"] = sub

    return assignments
