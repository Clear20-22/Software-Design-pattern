"""
SINGLETON PATTERN
-----------------
Guarantees exactly one MongoDB client/connection exists for the whole
application, no matter how many times MongoDBSingleton() is called or
from how many modules. Every router/service asks for the DB through
get_database() instead of creating its own client.
"""

import os
from pymongo import MongoClient
from pymongo.database import Database
from dotenv import load_dotenv
load_dotenv()


class MongoDBSingleton:
    _instance = None
    _client: MongoClient = None
    _db: Database = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(MongoDBSingleton, cls).__new__(cls)
        return cls._instance

    def __init__(
        self,
        uri: str = None,
        db_name: str = None,
    ):
        # __init__ runs every time MongoDBSingleton() is called, but we
        # only actually connect once -- the _client is None check makes
        # every subsequent call a no-op, so we always reuse the same
        # connection instead of opening a new one.
        if MongoDBSingleton._client is None:
            uri = uri or os.getenv("MONGO_URI", "mongodb://localhost:27017")
            db_name = db_name or os.getenv("MONGO_DB_NAME", "university_db")
            try:
                import certifi
                MongoDBSingleton._client = MongoClient(uri, tlsCAFile=certifi.where())
            except Exception:
                MongoDBSingleton._client = MongoClient(uri)
            MongoDBSingleton._db = MongoDBSingleton._client[db_name]
            print(f"[Singleton] MongoDB connection established -> db='{db_name}'")

    def get_db(self) -> Database:
        return self._db

    def get_collection(self, name: str):
        return self._db[name]


def get_database() -> Database:
    """Convenience accessor used everywhere else in the app."""
    return MongoDBSingleton().get_db()
