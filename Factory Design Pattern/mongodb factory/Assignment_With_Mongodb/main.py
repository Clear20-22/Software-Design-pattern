from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from bson import ObjectId
import threading

from singleton import (
    get_eager,
    get_lazy,
    get_safe,
    get_double,
    get_bill,
    get_enum
)

from factory import DataFactory


app = FastAPI(
    title="Singleton + Factory Demo"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


patterns = {
    "eager": get_eager,
    "lazy": get_lazy,
    "safe": get_safe,
    "double": get_double,
    "bill": get_bill,
    "enum": get_enum
}


# Default selected singleton
current_pattern = "lazy"


def serialize_docs(docs):

    result = []

    for doc in docs:

        item = {}

        for key, value in doc.items():

            if isinstance(value, ObjectId):
                item[key] = str(value)

            else:
                item[key] = value

        result.append(item)

    return result


@app.get("/")
def home():

    return FileResponse(
        "home.html"
    )


@app.get("/set-pattern/{pattern}")
def set_pattern(pattern: str):

    global current_pattern

    if pattern not in patterns:

        return {
            "error": "Invalid pattern"
        }

    current_pattern = pattern

    return {
        "message": "Pattern selected",
        "current_pattern": current_pattern.upper()
    }


@app.get("/current-pattern")
def get_pattern():

    return {
        "current_pattern": current_pattern.upper()
    }


@app.get("/singleton/{pattern}")
def singleton_test(pattern: str):

    if pattern not in patterns:

        return {
            "error": "Invalid pattern"
        }

    maker = patterns[pattern]

    first = maker()
    second = maker()
    third = maker()

    try:

        users = serialize_docs(
            first.get_all_users()
        )

    except Exception as e:

        print(e)

        users = []

    return {

        "pattern": pattern.upper(),

        "first_id": id(first),

        "second_id": id(second),

        "third_id": id(third),

        "same_object":
        first is second is third,

        "user_count":
        len(users),

        "users":
        users
    }


@app.post("/add-random-student")
def add_random_student():

    db = patterns[
        current_pattern
    ]()

    student = (
        DataFactory
        .create_random_student()
    )

    db.insert_data(
        student.to_dict()
    )

    return {

        "message":
        "Random student added",

        "singleton":
        current_pattern.upper(),

        "data":
        student.to_dict()
    }


@app.post("/add-random-teacher")
def add_random_teacher():

    db = patterns[
        current_pattern
    ]()

    teacher = (
        DataFactory
        .create_random_teacher()
    )

    db.insert_data(
        teacher.to_dict()
    )

    return {

        "message":
        "Random teacher added",

        "singleton":
        current_pattern.upper(),

        "data":
        teacher.to_dict()
    }


@app.post("/seed-data")
def seed_data():

    db = patterns[
        current_pattern
    ]()

    students = (
        DataFactory
        .create_bulk_students(
            15
        )
    )

    for student in students:

        db.insert_data(
            student
        )

    return {

        "message":
        "15 records inserted",

        "singleton":
        current_pattern.upper()
    }


@app.get("/all-users")
def get_users():

    db = patterns[
        current_pattern
    ]()

    users = (
        db.get_all_users()
    )

    return {

        "count":
        len(users),

        "singleton":
        current_pattern.upper(),

        "data":
        serialize_docs(users)
    }


@app.post("/clear")
def clear_data():

    db = patterns[
        current_pattern
    ]()

    db.clear_data()

    return {

        "message":
        "Database cleared"
    }


@app.get("/thread-test/{pattern}")
def thread_test(
    pattern: str
):

    if pattern not in patterns:

        return {
            "error":
            "Invalid pattern"
        }

    maker = patterns[
        pattern
    ]

    instance_ids = []

    result_lock = (
        threading.Lock()
    )

    def worker():

        obj = maker()

        with result_lock:

            instance_ids.append(
                id(obj)
            )

    threads = []

    for _ in range(50):

        t = threading.Thread(
            target=worker
        )

        threads.append(t)

        t.start()

    for t in threads:
        t.join()

    unique_ids = list(
        set(instance_ids)
    )

    return {

        "pattern":
        pattern.upper(),

        "threads":
        len(instance_ids),

        "unique_instances":
        len(unique_ids),

        "instance_ids":
        unique_ids,

        "thread_safe":
        len(unique_ids) == 1
    }


@app.get("/all-thread-tests")
def all_thread_tests():

    results = []

    for pattern_name, maker in patterns.items():

        instance_ids = []

        lock = (
            threading.Lock()
        )

        def worker():

            obj = maker()

            with lock:

                instance_ids.append(
                    id(obj)
                )

        threads = []

        for _ in range(50):

            t = threading.Thread(
                target=worker
            )

            threads.append(t)

            t.start()

        for t in threads:
            t.join()

        unique_ids = list(
            set(instance_ids)
        )

        results.append({

            "pattern":
            pattern_name.upper(),

            "threads":
            50,

            "unique_instances":
            len(unique_ids),

            "instance_id":
            unique_ids[0]
            if unique_ids
            else None,

            "thread_safe":
            len(unique_ids) == 1
        })

    return results


@app.get("/health")
def health():

    return {

        "status":
        "running",

        "singleton":
        current_pattern.upper(),

        "message":
        "Singleton + Factory Running"
    }


if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )