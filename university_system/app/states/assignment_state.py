"""
STATE PATTERN
-------------
Allows an Assignment object to alter its behavior dynamically when its
internal state changes. The AssignmentContext delegates all state-dependent
actions (publishing, submitting, closing, grading) to its active AssignmentState instance.

States:
  DraftState       -> Editable by teacher, students CANNOT submit.
  OpenState        -> Submissions OPEN for students.
  UnderReviewState -> Submissions CLOSED. Teacher grading in progress.
  GradedState      -> Grades FINALIZED and published. Assignment locked.
"""

from abc import ABC, abstractmethod


class AssignmentState(ABC):
    @abstractmethod
    def publish(self, context) -> None:
        pass

    @abstractmethod
    def close_submissions(self, context) -> None:
        pass

    @abstractmethod
    def finalize_grades(self, context) -> None:
        pass

    @abstractmethod
    def reopen(self, context) -> None:
        pass

    @abstractmethod
    def can_submit(self) -> bool:
        pass

    @abstractmethod
    def can_edit(self) -> bool:
        pass

    @abstractmethod
    def get_state_name(self) -> str:
        pass

    @abstractmethod
    def get_display_label(self) -> str:
        pass


class DraftState(AssignmentState):
    def publish(self, context) -> None:
        context.transition_to(OpenState())

    def close_submissions(self, context) -> None:
        raise ValueError("Cannot close submissions for a Draft assignment.")

    def finalize_grades(self, context) -> None:
        raise ValueError("Cannot finalize grades for a Draft assignment.")

    def reopen(self, context) -> None:
        raise ValueError("Assignment is already in Draft mode.")

    def can_submit(self) -> bool:
        return False

    def can_edit(self) -> bool:
        return True

    def get_state_name(self) -> str:
        return "draft"

    def get_display_label(self) -> str:
        return "📝 Draft"


class OpenState(AssignmentState):
    def publish(self, context) -> None:
        raise ValueError("Assignment is already published and open.")

    def close_submissions(self, context) -> None:
        context.transition_to(UnderReviewState())

    def finalize_grades(self, context) -> None:
        raise ValueError("Cannot finalize grades while submissions are still open. Close submissions first.")

    def reopen(self, context) -> None:
        context.transition_to(DraftState())

    def can_submit(self) -> bool:
        return True

    def can_edit(self) -> bool:
        return False

    def get_state_name(self) -> str:
        return "open"

    def get_display_label(self) -> str:
        return "🔓 Submissions Open"


class UnderReviewState(AssignmentState):
    def publish(self, context) -> None:
        raise ValueError("Assignment is under review.")

    def close_submissions(self, context) -> None:
        raise ValueError("Submissions are already closed.")

    def finalize_grades(self, context) -> None:
        context.transition_to(GradedState())

    def reopen(self, context) -> None:
        context.transition_to(OpenState())

    def can_submit(self) -> bool:
        return False

    def can_edit(self) -> bool:
        return False

    def get_state_name(self) -> str:
        return "under_review"

    def get_display_label(self) -> str:
        return "🔒 Under Review"


class GradedState(AssignmentState):
    def publish(self, context) -> None:
        raise ValueError("Assignment grades are already finalized.")

    def close_submissions(self, context) -> None:
        raise ValueError("Assignment is already graded.")

    def finalize_grades(self, context) -> None:
        raise ValueError("Grades are already finalized.")

    def reopen(self, context) -> None:
        context.transition_to(UnderReviewState())

    def can_submit(self) -> bool:
        return False

    def can_edit(self) -> bool:
        return False

    def get_state_name(self) -> str:
        return "graded"

    def get_display_label(self) -> str:
        return "✅ Graded & Finalized"


class AssignmentStateFactory:
    _states = {
        "draft": DraftState,
        "open": OpenState,
        "under_review": UnderReviewState,
        "graded": GradedState,
    }

    @classmethod
    def from_name(cls, name: str) -> AssignmentState:
        key = (name or "draft").lower().strip()
        state_cls = cls._states.get(key)
        if not state_cls:
            raise ValueError(f"Unknown state: '{name}'. Available: {list(cls._states.keys())}")
        return state_cls()


class AssignmentContext:
    """
    Main Context holding a reference to the current AssignmentState.
    Delegates actions and state transitions to the state object.
    """
    def __init__(self, initial_state: AssignmentState = None):
        self._state = initial_state or DraftState()

    def transition_to(self, state: AssignmentState) -> None:
        self._state = state

    def get_state(self) -> AssignmentState:
        return self._state

    def publish(self) -> None:
        self._state.publish(self)

    def close_submissions(self) -> None:
        self._state.close_submissions(self)

    def finalize_grades(self) -> None:
        self._state.finalize_grades(self)

    def reopen(self) -> None:
        self._state.reopen(self)

    def can_submit(self) -> bool:
        return self._state.can_submit()

    def can_edit(self) -> bool:
        return self._state.can_edit()

    def get_state_name(self) -> str:
        return self._state.get_state_name()

    def get_display_label(self) -> str:
        return self._state.get_display_label()
