# University Management System — FastAPI + MongoDB

Lab project combining three design patterns:

| Pattern   | Where                                   | Problem it solves |
|-----------|------------------------------------------|--------------------|
| Singleton | `app/database.py`                        | One shared MongoDB connection for the whole app |
| Factory   | `app/factories/user_factory.py`          | Role-based user creation (student/teacher/admin) without the rest of the app knowing the concrete classes |
| Observer  | `app/observers/`                         | Classroom notice board notifies all enrolled students without being coupled to *how* they're notified |

## Run it

```bash
pip install -r requirements.txt
export MONGO_URI="mongodb://localhost:27017"
export JWT_SECRET_KEY="some-long-random-string"
uvicorn app.main:app --reload
```

Docs at `http://localhost:8000/docs`.

## How the Observer pattern is wired up (this week's task)

- **Subject** = `NoticeBoard` (one per classroom, `app/observers/notice_board.py`).
  Holds a list of Observers and exposes `publish_notice()`, which
  saves the notice then calls `notify()` — nothing else.
- **Observer** = `StudentObserver` (`app/observers/student_observer.py`).
  One instance per enrolled student. `update()` decides what
  "getting notified" actually means: write to the `notifications`
  collection, and push live over the student's WebSocket if they're
  connected.
- **Registry** = `NoticeBoardManager`. Hands out the right
  `NoticeBoard` per classroom and re-syncs its observer list from the
  `enrollments` collection every time, so newly enrolled/unenrolled
  students are always up to date.

Because `NoticeBoard` only ever calls `observer.update(notice)`, you
can add a new notification channel (email, SMS, push service) by
writing a new `Observer` subclass and attaching it — the notice board
route in `app/routers/notice.py` never changes.

## Typical flow to test

1. `POST /auth/register` — role=`teacher`, and register a couple of
   `student` accounts.
2. `POST /auth/login` as the teacher → get a token.
3. `POST /classroom/create?name=CSE401` (teacher token).
4. `POST /classroom/enroll` with `classroom_id` + each `student_id`.
5. Open `ws://localhost:8000/ws/notifications/{student_id}` for a
   student (e.g. via a WebSocket test client).
6. `POST /classroom/{classroom_id}/notice` as the teacher with a
   title/content → every enrolled student's socket receives it
   instantly, and `GET /student/notifications` (as that student)
   shows it persisted too.
