from fastapi import APIRouter, Depends, HTTPException, Query

from app.database import get_database
from app.routers.auth import get_current_user
from app.visitors.classroom_visitor import (
    ClassroomElement,
    AssignmentElement,
    GradeElement,
    PerformanceAnalyticsVisitor,
    RiskAuditVisitor,
    MarkdownReportVisitor,
)

router = APIRouter(prefix="/classroom", tags=["Analytics & Visitor Pattern"])


@router.get("/{classroom_id}/analytics/visitor")
def run_classroom_visitor(
    classroom_id: str,
    visitor_type: str = Query("performance", description="Visitor type: 'performance', 'risk', or 'report'"),
    user=Depends(get_current_user),
):
    """
    --- Visitor Design Pattern (Double Dispatch Engine) ---
    Constructs the VisitableElement object tree (ClassroomElement, AssignmentElement, GradeElement)
    and accepts the requested ClassroomVisitor (PerformanceAnalyticsVisitor, RiskAuditVisitor, MarkdownReportVisitor).
    The operation is executed entirely through Double Dispatch (element.accept(visitor)).
    """
    db = get_database()

    # 1. Fetch Classroom Data
    classroom = db.classrooms.find_one({"classroom_id": classroom_id})
    if not classroom:
        raise HTTPException(status_code=404, detail="Classroom not found")

    teacher = db.users.find_one({"user_id": classroom.get("teacher_id")})
    teacher_name = teacher.get("name", "Teacher") if teacher else "Teacher"

    enrolled_count = db.enrollments.count_documents({"classroom_id": classroom_id})

    # Create Classroom Element
    classroom_element = ClassroomElement(
        classroom_id=classroom_id,
        name=classroom.get("name", "Classroom"),
        teacher_name=teacher_name,
        enrolled_count=enrolled_count,
    )

    # 2. Fetch Assignment Elements
    assignment_docs = list(db.assignments.find({"classroom_id": classroom_id}))
    assignment_elements = []
    for doc in assignment_docs:
        sub_count = db.assignment_submissions.count_documents({"assignment_id": doc["assignment_id"]})
        assignment_elements.append(
            AssignmentElement(
                assignment_id=doc["assignment_id"],
                title=doc.get("title", "Assignment"),
                state=doc.get("state", "draft"),
                deadline=doc.get("deadline", ""),
                submissions_count=sub_count,
            )
        )

    # 3. Fetch Grade Element
    grade_doc = db.grades.find_one({"classroom_id": classroom_id})
    grade_element = GradeElement(
        results=grade_doc.get("results", []) if grade_doc else [],
        strategy_type=grade_doc.get("strategy_type", "standard") if grade_doc else "standard",
    )

    # 4. Instantiate Requested Concrete Visitor
    v_type = (visitor_type or "performance").lower().strip()
    if v_type == "performance":
        visitor = PerformanceAnalyticsVisitor()
    elif v_type == "risk":
        visitor = RiskAuditVisitor()
    elif v_type == "report":
        visitor = MarkdownReportVisitor()
    else:
        raise HTTPException(status_code=400, detail=f"Unknown visitor_type: '{visitor_type}'. Allowed: performance, risk, report")

    # 5. Execute DOUBLE DISPATCH on the Object Tree!
    classroom_element.accept(visitor)

    for assign_elem in assignment_elements:
        assign_elem.accept(visitor)

    grade_element.accept(visitor)

    # 6. Return Visitor Results
    if v_type == "performance":
        return {
            "visitor_type": "PerformanceAnalyticsVisitor",
            "pattern": "Visitor (Double Dispatch)",
            "summary": visitor.summary,
            "metrics": visitor.metrics,
        }
    elif v_type == "risk":
        return {
            "visitor_type": "RiskAuditVisitor",
            "pattern": "Visitor (Double Dispatch)",
            "risk_warnings": visitor.risk_warnings,
            "failing_students": visitor.failing_students,
        }
    elif v_type == "report":
        return {
            "visitor_type": "MarkdownReportVisitor",
            "pattern": "Visitor (Double Dispatch)",
            "markdown_report": visitor.get_markdown(),
        }
