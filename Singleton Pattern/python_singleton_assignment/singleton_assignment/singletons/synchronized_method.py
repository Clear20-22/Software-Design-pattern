from __future__ import annotations

import threading
from typing import Optional

from ..mongo_base import MongoConnectionManagerBase
from ._shared import create_manager


class SynchronizedMethodMongoConnectionManager(MongoConnectionManagerBase):
    _instance: Optional["SynchronizedMethodMongoConnectionManager"] = None
    _instance_lock = threading.Lock()

    @classmethod
    def get_instance(cls) -> "SynchronizedMethodMongoConnectionManager":
        with cls._instance_lock:
            if cls._instance is None:
                cls._instance = create_manager(cls)
        return cls._instance


def get_manager() -> SynchronizedMethodMongoConnectionManager:
    return SynchronizedMethodMongoConnectionManager.get_instance()

