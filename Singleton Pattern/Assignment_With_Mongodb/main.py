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
    get_enum,
)

app = FastAPI(title="Singleton Pattern Demo")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

patterns = {
    "eager": get_eager,
    "lazy": get_lazy,
    "safe": get_safe,
    "double": get_double,
    "bill": get_bill,
    "enum": get_enum,
}


def serialize_docs(docs):
    result = []

    for doc in docs:
        item = {}

        for k, v in doc.items():
            if isinstance(v, ObjectId):
                item[k] = str(v)
            else:
                item[k] = v

        result.append(item)

    return result


@app.get("/")
def home():
    return FileResponse("home.html")


@app.get("/singleton/{pattern}")
def test_pattern(pattern: str):

    if pattern not in patterns:
        return {"error": "Invalid Pattern"}

    maker = patterns[pattern]

    first = maker()
    second = maker()
    third = maker()

    try:
        users = first.get_all_users()
        users = serialize_docs(users)
        user_count = len(users)

    except Exception as exc:
        print(exc)
        users = []
        user_count = 0

    return {
        "pattern": pattern.upper(),
        "first_id": id(first),
        "second_id": id(second),
        "third_id": id(third),
        "same_object": first is second is third,
        "user_count": user_count,
        "users": users,
    }


@app.get("/thread-test/{pattern}")
def thread_test(pattern: str):

    if pattern not in patterns:
        return {"error": "Invalid Pattern"}

    maker = patterns[pattern]

    instance_ids = []
    result_lock = threading.Lock()

    def worker():
        obj = maker()

        with result_lock:
            instance_ids.append(id(obj))

    threads = []

    for _ in range(50):
        t = threading.Thread(target=worker)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    unique_ids = list(set(instance_ids))

    return {
        "pattern": pattern.upper(),
        "total_threads": len(instance_ids),
        "unique_instances": len(unique_ids),
        "instance_ids": unique_ids,
        "thread_safe": len(unique_ids) == 1,
    }


@app.get("/all-thread-tests")
def all_thread_tests():

    results = []

    for pattern_name, maker in patterns.items():

        instance_ids = []
        result_lock = threading.Lock()

        def worker():
            obj = maker()

            with result_lock:
                instance_ids.append(id(obj))

        threads = []

        for _ in range(50):
            t = threading.Thread(target=worker)
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        unique_ids = list(set(instance_ids))

        results.append({
            "pattern": pattern_name.upper(),
            "threads": 50,
            "unique_instances": len(unique_ids),
            "thread_safe": len(unique_ids) == 1,
            "instance_id": unique_ids[0] if unique_ids else None
        })

    return results


@app.get("/health")
def health():
    return {
        "status": "running",
        "message": "FastAPI Singleton Demo is working"
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )