from __future__ import annotations

import threading

from pymongo import MongoClient


URL = "mongodb://mimrobo1726_db_user:mimrobo1726_db_user@ac-gq1y29g-shard-00-00.wkza9aw.mongodb.net:27017,ac-gq1y29g-shard-00-01.wkza9aw.mongodb.net:27017,ac-gq1y29g-shard-00-02.wkza9aw.mongodb.net:27017/?ssl=true&replicaSet=atlas-8a1g5a-shard-0&authSource=admin&appName=Cluster0"
DB_NAME = "singleton_db"
COL_NAME = "Users"


class BaseDb:
    def __init__(self) -> None:
        if getattr(self, "ready", False):
            return

        self.url = URL
        self.client = MongoClient(self.url)
        self.db = self.client[DB_NAME]
        self.collection = self.db[COL_NAME]
        self.ready = True

    def get_instance_id(self) -> int:
        return id(self)

    def get_all_users(self):
        return list(self.collection.find())

    def close_connection(self) -> None:
        self.client.close()


class EagerDb(BaseDb):
    _one = None

    def __new__(cls, *args, **kwargs):
        if cls._one is None:
            cls._one = super().__new__(cls)
        return cls._one


class LazyDb(BaseDb):
    _one = None

    def __new__(cls, *args, **kwargs):
        if cls._one is None:
            cls._one = super().__new__(cls)
        return cls._one


class SafeDb(BaseDb):
    _one = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._one is None:
                cls._one = super().__new__(cls)
        return cls._one


class DoubleDb(BaseDb):
    _one = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._one is None:
            with cls._lock:
                if cls._one is None:
                    cls._one = super().__new__(cls)
        return cls._one


class BillDb(BaseDb):
    pass


class BillBox:
    one = BillDb()


class Box:
    def __init__(self, value: BaseDb) -> None:
        self.value = value


class EnumDb(BaseDb):
    pass


class EnumBox:
    one = Box(EnumDb())


EAGER_ONE = EagerDb()


def get_eager():
    return EAGER_ONE


def get_lazy():
    return LazyDb()


def get_safe():
    return SafeDb()


def get_double():
    return DoubleDb()


def get_bill():
    return BillBox.one


def get_enum():
    return EnumBox.one.value
    
    