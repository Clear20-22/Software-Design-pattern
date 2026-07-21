"""
Concrete Subject. One NoticeBoard exists per classroom. It holds the
list of Observers (enrolled students) and is the ONLY thing that
knows a new notice was published -- it has no idea what happens to
each observer afterwards (that's StudentObserver's job). This is the
loose coupling the task asks for: publish_notice() never touches
notification logic directly, it just calls notify().
"""

import uuid
from typing import List, Dict
from datetime import datetime

from app.observers.observer import Subject, Observer
from app.observers.student_observer import StudentObserver
from app.database import get_database


class NoticeBoard(Subject):
    def __init__(self, classroom_id: str):
        self.classroom_id = classroom_id
        self._observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    async def notify(self, notice: dict) -> None:
        for observer in self._observers:
            await observer.update(notice)

    async def publish_notice(self, title: str, content: str, posted_by: str) -> dict:
        db = get_database()
        notice_doc = {
            "notice_id": str(uuid.uuid4()),
            "classroom_id": self.classroom_id,
            "title": title,
            "content": content,
            "posted_by": posted_by,
            "created_at": datetime.utcnow(),
        }
        db.notices.insert_one(notice_doc)
        notice_doc.pop("_id", None)
        await self.notify(notice_doc)  # <-- fan-out to every enrolled student
        return notice_doc


class NoticeBoardManager:
    """
    Registry that hands out one NoticeBoard per classroom_id, and
    refreshes its observer list from the current enrollment records
    before every use -- so students added/removed since the last
    notice are always accounted for.
    """
    _instance = None
    _boards: Dict[str, NoticeBoard] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_notice_board(self, classroom_id: str) -> NoticeBoard:
        if classroom_id not in self._boards:
            self._boards[classroom_id] = NoticeBoard(classroom_id)
        board = self._boards[classroom_id]
        self._sync_observers(board)
        return board

    def _sync_observers(self, board: NoticeBoard) -> None:
        db = get_database()
        board._observers.clear()
        enrollments = db.enrollments.find({"classroom_id": board.classroom_id})
        for enrollment in enrollments:
            student = db.users.find_one({"user_id": enrollment["student_id"]})
            if student:
                board.attach(StudentObserver(student["user_id"], student["name"]))
