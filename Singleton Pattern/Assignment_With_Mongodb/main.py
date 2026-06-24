from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from bson import ObjectId

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