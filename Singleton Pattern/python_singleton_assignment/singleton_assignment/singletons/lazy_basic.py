from __future__ import annotations

import time
from typing import Optional

from ..config import load_settings
from ..mongo_base import MongoConnectionManagerBase
from ._shared import build_manager_config


class LazyBasicMongoConnectionManager(MongoConnectionManagerBase):
    _instance: Optional["LazyBasicMongoConnectionManager"] = None

    def __new__(cls) -> "LazyBasicMongoConnectionManager":
        if cls._instance is None:
            settings = load_settings()
            if settings.simulate_slow_init_seconds > 0:
                time.sleep(settings.simulate_slow_init_seconds)
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if getattr(self, "_initialized", False):
            return
        super().__init__(build_manager_config())
        self._initialized = True


def get_manager() -> LazyBasicMongoConnectionManager:
    return LazyBasicMongoConnectionManager()
