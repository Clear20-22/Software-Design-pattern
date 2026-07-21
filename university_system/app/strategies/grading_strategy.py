"""
STRATEGY PATTERN
----------------
Defines a family of algorithms for grading student marks, encapsulates each
one, and makes them interchangeable at runtime. The GradingContext delegates
the calculation to whichever GradingStrategy is currently injected into it.

Adding a new grading scheme (e.g. 4.0 GPA Scale, Honors Scale) only requires
creating a new strategy class here without modifying routers, models, or DB code.
"""

from abc import ABC, abstractmethod
import math
from typing import List, Dict, Any


class GradingStrategy(ABC):
    @abstractmethod
    def evaluate(self, scores: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Takes a list of student score dicts:
        [{ "student_id": "...", "marks": 85.0 }, ...]
        Returns a list of dicts with calculated grade information:
        [{ "student_id": "...", "marks": 85.0, "grade": "A", "status": "PASSED" }, ...]
        """
        pass


class StandardGradingStrategy(GradingStrategy):
    """Absolute percentage scale grading."""
    def evaluate(self, scores: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        results = []
        for item in scores:
            m = float(item.get("marks", 0))
            if m >= 80:
                grade, status = "A", "PASSED"
            elif m >= 70:
                grade, status = "B", "PASSED"
            elif m >= 60:
                grade, status = "C", "PASSED"
            elif m >= 50:
                grade, status = "D", "PASSED"
            else:
                grade, status = "F", "FAILED"
            results.append({
                "student_id": item["student_id"],
                "marks": m,
                "grade": grade,
                "status": status,
                "strategy_used": "Standard Absolute"
            })
        return results


class RelativeGradingStrategy(GradingStrategy):
    """Relative grading based on class mean and standard deviation (Bell Curve)."""
    def evaluate(self, scores: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if not scores:
            return []

        marks_list = [float(s.get("marks", 0)) for s in scores]
        mean = sum(marks_list) / len(marks_list)
        variance = sum((m - mean) ** 2 for m in marks_list) / len(marks_list)
        std_dev = math.sqrt(variance) or 1.0  # avoid division by zero

        results = []
        for item in scores:
            m = float(item.get("marks", 0))
            z_score = (m - mean) / std_dev

            if z_score >= 1.0:
                grade, status = "A (Top)", "PASSED"
            elif z_score >= 0.0:
                grade, status = "B (Above Avg)", "PASSED"
            elif z_score >= -1.0:
                grade, status = "C (Below Avg)", "PASSED"
            else:
                grade, status = "F (Low)", "FAILED"

            results.append({
                "student_id": item["student_id"],
                "marks": m,
                "grade": grade,
                "status": status,
                "strategy_used": "Relative Curve"
            })
        return results


class PassFailGradingStrategy(GradingStrategy):
    """Binary threshold grading (Pass / Fail)."""
    def evaluate(self, scores: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        results = []
        for item in scores:
            m = float(item.get("marks", 0))
            status = "PASSED" if m >= 50 else "FAILED"
            grade = "P" if m >= 50 else "F"
            results.append({
                "student_id": item["student_id"],
                "marks": m,
                "grade": grade,
                "status": status,
                "strategy_used": "Pass / Fail"
            })
        return results


class GradingContext:
    """
    Context that maintains a reference to a GradingStrategy and delegates
    the evaluation to it.
    """
    def __init__(self, strategy: GradingStrategy = None):
        self._strategy = strategy

    def set_strategy(self, strategy: GradingStrategy) -> None:
        self._strategy = strategy

    def execute_evaluation(self, scores: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if not self._strategy:
            raise ValueError("No grading strategy set in GradingContext")
        return self._strategy.evaluate(scores)


class GradingStrategyFactory:
    """Factory to return strategy instances by strategy key."""
    _strategies = {
        "standard": StandardGradingStrategy,
        "relative": RelativeGradingStrategy,
        "pass_fail": PassFailGradingStrategy,
    }

    @classmethod
    def get_strategy(cls, strategy_type: str) -> GradingStrategy:
        key = strategy_type.lower().strip()
        strategy_cls = cls._strategies.get(key)
        if not strategy_cls:
            raise ValueError(f"Unknown grading strategy: '{strategy_type}'. Available: {list(cls._strategies.keys())}")
        return strategy_cls()
