import uuid
from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime

from app.database import get_database
from app.models import GradeEvaluationRequest
from app.routers.auth import require_role, get_current_user
from app.strategies.grading_strategy import GradingContext, GradingStrategyFactory
from app.observers.notice_board import NoticeBoardManager

router = APIRouter(prefix="/classroom", tags=["Grading & Strategy Pattern"])
notice_board_manager = NoticeBoardManager()


@router.post("/{classroom_id}/evaluate")
async def evaluate_classroom_grades(
    classroom_id: str,
    request: GradeEvaluationRequest,
    strategy_type: str = Query("standard", description="Grading strategy: 'standard', 'relative', or 'pass_fail'"),
    user=Depends(require_role("teacher", "admin")),
):
    """
    --- Strategy Pattern + Observer Pattern ---
    1. Strategy Pattern: Dynamically applies the requested grading strategy ('standard',
       'relative', or 'pass_fail') to compute grades for classroom students.
    2. Observer Pattern: Automatically fans out a grade publication notification to all
       enrolled StudentObservers via NoticeBoard.notify().
    """
    db = get_database()
    classroom = db.classrooms.find_one({"classroom_id": classroom_id})
    if not classroom:
        raise HTTPException(status_code=404, detail="Classroom not found")

    try:
        strategy = GradingStrategyFactory.get_strategy(strategy_type)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    scores_data = [item.dict() for item in request.scores]
    context = GradingContext(strategy)
    results = context.execute_evaluation(scores_data)

    evaluation_record = {
        "classroom_id": classroom_id,
        "evaluated_by": user["user_id"],
        "strategy_type": strategy_type,
        "evaluated_at": datetime.utcnow(),
        "results": results,
    }

    # Upsert grade evaluation for this classroom
    db.grades.update_one(
        {"classroom_id": classroom_id},
        {"$set": evaluation_record},
        upsert=True,
    )
    evaluation_record.pop("_id", None)

    # --- Observer Pattern Fan-out Notification ---
    board = notice_board_manager.get_notice_board(classroom_id)
    notice_payload = {
        "notice_id": str(uuid.uuid4()),
        "classroom_id": classroom_id,
        "title": f"Course Grades Published ({strategy_type.title()})",
        "content": f"Grades for classroom '{classroom.get('name', classroom_id)}' have been evaluated using '{strategy_type}' strategy.",
        "posted_by": user["user_id"],
        "created_at": datetime.utcnow(),
    }
    await board.notify(notice_payload)

    return {"message": "Grades evaluated successfully and students notified", "data": evaluation_record}


@router.get("/{classroom_id}/grades")
def get_classroom_grades(classroom_id: str, user=Depends(get_current_user)):
    """
    Retrieves calculated grade evaluation.
    - Teachers/Admins: see all students' grades in the classroom.
    - Students: see ONLY their own personal evaluated grade for privacy.
    """
    db = get_database()
    record = db.grades.find_one({"classroom_id": classroom_id}, {"_id": 0})
    if not record:
        return {"classroom_id": classroom_id, "results": []}

    if user["role"] == "student":
        # Filter results to include ONLY the current student's grade
        my_results = [r for r in record.get("results", []) if r.get("student_id") == user["user_id"]]
        record["results"] = my_results

    return record
