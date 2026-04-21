from __future__ import annotations

import threading
from typing import Optional

from ..mongo_base import MongoConnectionManagerBase
from ._shared import create_manager


class DoubleCheckedLockingMongoConnectionManager(MongoConnectionManagerBase):
    _instance: Optional["DoubleCheckedLockingMongoConnectionManager"] = None
    _lock = threading.Lock()

    @classmethod
    def get_instance(cls) -> "DoubleCheckedLockingMongoConnectionManager":
        instance = cls._instance
        if instance is not None:
            return instance
        with cls._lock:
            if cls._instance is None:
                cls._instance = create_manager(cls)
            return cls._instance


def get_manager() -> DoubleCheckedLockingMongoConnectionManager:
    return DoubleCheckedLockingMongoConnectionManager.get_instance()

