from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from app.models import NoticeCreateRequest
from app.database import get_database
from app.routers.auth import require_role, get_current_user
from app.observers.notice_board import NoticeBoardManager
from app.websocket_manager import ConnectionManager

router = APIRouter(tags=["Notice Board"])

notice_board_manager = NoticeBoardManager()  # one registry, shared by the whole app
connection_manager = ConnectionManager()     # one connection map, shared by the whole app


@router.post("/classroom/{classroom_id}/notice")
async def publish_notice(
    classroom_id: str,
    request: NoticeCreateRequest,
    user=Depends(require_role("teacher", "admin")),
):
    """
    --- Observer Pattern in action ---
    This route only asks the NoticeBoard (Subject) for the classroom
    to publish a notice. The NoticeBoard fans that notice out to every
    enrolled student (Observer) attached to it. This handler has zero
    knowledge of *how* a student gets notified -- that logic lives in
    StudentObserver, so it can change (add email, SMS, push, etc.)
    without ever touching this endpoint.
    """
    board = notice_board_manager.get_notice_board(classroom_id)
    notice = await board.publish_notice(
        title=request.title, content=request.content, posted_by=user["user_id"]
    )
    return {"message": "Notice published, all enrolled students notified", "notice": notice}


@router.get("/classroom/{classroom_id}/notice")
def get_classroom_notices(classroom_id: str, user=Depends(get_current_user)):
    db = get_database()
    return list(
        db.notices.find({"classroom_id": classroom_id}, {"_id": 0}).sort("created_at", 1)
    )


@router.get("/student/notifications")
def get_my_notifications(user=Depends(get_current_user)):
    if user["role"] != "student":
        return []
    db = get_database()
    return list(
        db.notifications.find({"student_id": user["user_id"]}, {"_id": 0}).sort(
            "created_at", -1
        )
    )


@router.patch("/student/notifications/{notice_id}/read")
def mark_notification_read(notice_id: str, user=Depends(get_current_user)):
    db = get_database()
    db.notifications.update_many(
        {"student_id": user["user_id"], "notice_id": notice_id}, {"$set": {"is_read": True}}
    )
    return {"message": "Marked as read"}


@router.websocket("/ws/notifications/{student_id}")
async def notifications_websocket(websocket: WebSocket, student_id: str):
    """
    A student's frontend opens this connection once they log in.
    StudentObserver.update() pushes here instantly when a notice is
    published, on top of the persisted copy in MongoDB.
    """
    await connection_manager.connect(student_id, websocket)
    try:
        while True:
            await websocket.receive_text()  # keep-alive; ignore content
    except WebSocketDisconnect:
        connection_manager.disconnect(student_id)
