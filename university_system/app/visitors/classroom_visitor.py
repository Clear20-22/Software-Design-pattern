"""
VISITOR DESIGN PATTERN
----------------------
Allows defining new operations on a complex object hierarchy (Classroom,
Assignments, Grades) without modifying the classes of the elements on which it operates.

Double Dispatch Mechanism:
  1. element.accept(visitor)
  2. visitor.visit_<element_type>(self)
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any


# --- VISITOR INTERFACE ---
class ClassroomVisitor(ABC):
    @abstractmethod
    def visit_classroom(self, element: "ClassroomElement") -> None:
        pass

    @abstractmethod
    def visit_assignment(self, element: "AssignmentElement") -> None:
        pass

    @abstractmethod
    def visit_grade(self, element: "GradeElement") -> None:
        pass


# --- ELEMENT INTERFACE ---
class VisitableElement(ABC):
    @abstractmethod
    def accept(self, visitor: ClassroomVisitor) -> None:
        pass


# --- CONCRETE ELEMENTS (Adapters holding domain data) ---
class ClassroomElement(VisitableElement):
    def __init__(self, classroom_id: str, name: str, teacher_name: str, enrolled_count: int):
        self.classroom_id = classroom_id
        self.name = name
        self.teacher_name = teacher_name
        self.enrolled_count = enrolled_count

    def accept(self, visitor: ClassroomVisitor) -> None:
        # Double Dispatch Step 2: Call visitor's specific visit method for Classroom
        visitor.visit_classroom(self)


class AssignmentElement(VisitableElement):
    def __init__(self, assignment_id: str, title: str, state: str, deadline: str, submissions_count: int):
        self.assignment_id = assignment_id
        self.title = title
        self.state = state
        self.deadline = deadline
        self.submissions_count = submissions_count

    def accept(self, visitor: ClassroomVisitor) -> None:
        # Double Dispatch Step 2: Call visitor's specific visit method for Assignment
        visitor.visit_assignment(self)


class GradeElement(VisitableElement):
    def __init__(self, results: List[Dict[str, Any]], strategy_type: str):
        self.results = results  # [{ "student_id": "...", "marks": 85, "grade": "A", "status": "PASSED" }, ...]
        self.strategy_type = strategy_type

    def accept(self, visitor: ClassroomVisitor) -> None:
        # Double Dispatch Step 2: Call visitor's specific visit method for Grade
        visitor.visit_grade(self)


# --- CONCRETE VISITORS ---

class PerformanceAnalyticsVisitor(ClassroomVisitor):
    """
    Visitor 1: Calculates performance metrics (average score, pass rate, highest score, total submissions).
    """
    def __init__(self):
        self.summary = {}
        self.metrics = []

    def visit_classroom(self, element: ClassroomElement) -> None:
        self.summary["classroom_name"] = element.name
        self.summary["teacher_name"] = element.teacher_name
        self.summary["enrolled_students"] = element.enrolled_count
        self.metrics.append(f"🏫 Classroom '{element.name}' has {element.enrolled_count} enrolled students.")

    def visit_assignment(self, element: AssignmentElement) -> None:
        sub_ratio = f"{element.submissions_count} submissions"
        self.metrics.append(f"📝 Assignment '{element.title}' [{element.state.upper()}]: {sub_ratio}.")

    def visit_grade(self, element: GradeElement) -> None:
        results = element.results or []
        if not results:
            self.metrics.append("📊 Grade Analytics: No grade evaluations recorded yet.")
            return

        scores = [r.get("marks", 0) for r in results]
        passed = [r for r in results if r.get("status") == "PASSED"]
        avg_score = round(sum(scores) / len(scores), 2) if scores else 0
        pass_rate = round((len(passed) / len(scores)) * 100, 1) if scores else 0

        self.summary["average_score"] = avg_score
        self.summary["pass_rate"] = pass_rate
        self.summary["highest_score"] = max(scores) if scores else 0
        self.summary["lowest_score"] = min(scores) if scores else 0

        self.metrics.append(f"📊 Class Average: {avg_score}% | Pass Rate: {pass_rate}% ({len(passed)}/{len(scores)} passed).")
        self.metrics.append(f"🏆 Top Score: {max(scores) if scores else 0} | Lowest Score: {min(scores) if scores else 0}.")


class RiskAuditVisitor(ClassroomVisitor):
    """
    Visitor 2: Detects academic risks (failing students, unsubmitted assignments, low engagement).
    """
    def __init__(self):
        self.risk_warnings = []
        self.failing_students = []

    def visit_classroom(self, element: ClassroomElement) -> None:
        if element.enrolled_count == 0:
            self.risk_warnings.append("⚠️ Risk Alert: Classroom has zero enrolled students.")

    def visit_assignment(self, element: AssignmentElement) -> None:
        if element.state == "draft":
            self.risk_warnings.append(f"⚠️ Notice: Assignment '{element.title}' is still in Draft mode.")
        elif element.state == "open" and element.submissions_count == 0:
            self.risk_warnings.append(f"🚨 Risk Alert: Assignment '{element.title}' is Open but has 0 submissions so far.")

    def visit_grade(self, element: GradeElement) -> None:
        results = element.results or []
        for r in results:
            if r.get("status") == "FAILED" or r.get("marks", 0) < 50:
                student_id = r.get("student_id", "Unknown")
                marks = r.get("marks", 0)
                self.failing_students.append({
                    "student_id": student_id,
                    "marks": marks,
                    "grade": r.get("grade", "F")
                })
                self.risk_warnings.append(f"🚨 Academic Risk: Student ({student_id[:8]}...) is FAILING with {marks} marks ({r.get('grade', 'F')}).")


class MarkdownReportVisitor(ClassroomVisitor):
    """
    Visitor 3: Formats a complete markdown summary report of the classroom structure.
    """
    def __init__(self):
        self.lines = ["# 📊 Classroom Visitor Analytical Report", ""]

    def visit_classroom(self, element: ClassroomElement) -> None:
        self.lines.append(f"## 🏫 Course: {element.name}")
        self.lines.append(f"- **Instructor**: {element.teacher_name}")
        self.lines.append(f"- **Enrolled Roster**: {element.enrolled_count} Students")
        self.lines.append("")

    def visit_assignment(self, element: AssignmentElement) -> None:
        self.lines.append(f"### 📝 Assignment: {element.title}")
        self.lines.append(f"- **Current State**: `{element.state}`")
        self.lines.append(f"- **Deadline**: `{element.deadline or 'N/A'}`")
        self.lines.append(f"- **Submissions Received**: {element.submissions_count}")
        self.lines.append("")

    def visit_grade(self, element: GradeElement) -> None:
        results = element.results or []
        self.lines.append(f"### 🎓 Grade Evaluation Summary ({element.strategy_type or 'Standard'})")
        if not results:
            self.lines.append("_No grade evaluations generated yet._")
        else:
            for r in results:
                self.lines.append(f"- Student `{r.get('student_id', '')[:8]}`: Marks **{r.get('marks')}** | Grade **{r.get('grade')}** | Status **{r.get('status')}**")
        self.lines.append("")

    def get_markdown(self) -> str:
        return "\n".join(self.lines)
