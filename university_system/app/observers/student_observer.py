"""
Concrete Observer. One StudentObserver instance represents one
enrolled student subscribed to a classroom's NoticeBoard. When the
NoticeBoard calls update(), this class decides HOW the student gets
notified -- currently: persist to the notifications collection AND
push live over WebSocket if they're connected. That decision lives
entirely here, so the NoticeBoard never has to change if we later add
email or SMS notifications.
"""

from datetime import datetime
from app.observers.observer import Observer
from app.database import get_database
from app.websocket_manager import ConnectionManager


class StudentObserver(Observer):
    def __init__(self, student_id: str, student_name: str):
        self.student_id = student_id
        self.student_name = student_name
        self._connection_manager = ConnectionManager()

    def __eq__(self, other):
        return isinstance(other, StudentObserver) and self.student_id == other.student_id

    async def update(self, notice: dict) -> None:
        db = get_database()
        notification_doc = {
            "student_id": self.student_id,
            "notice_id": notice["notice_id"],
            "classroom_id": notice["classroom_id"],
            "title": notice["title"],
            "message": f"New notice posted: {notice['title']}",
            "is_read": False,
            "created_at": datetime.utcnow(),
        }
        # Always persist, so the student sees it even if offline right now
        db.notifications.insert_one(notification_doc)

        # Push live if the student currently has a websocket connection open
        await self._connection_manager.send_notification(
            self.student_id,
            {
                "type": "new_notice",
                "notice_id": notice["notice_id"],
                "classroom_id": notice["classroom_id"],
                "title": notice["title"],
                "content": notice.get("content", ""),
            },
        )

        print(f"[Observer] Notified {self.student_name} ({self.student_id}) -> '{notice['title']}'")
