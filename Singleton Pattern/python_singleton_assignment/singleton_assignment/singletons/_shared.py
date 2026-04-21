from __future__ import annotations

from typing import TypeVar

from ..config import load_settings
from ..mongo_base import MongoConfig, MongoConnectionManagerBase


ManagerT = TypeVar("ManagerT", bound=MongoConnectionManagerBase)


def build_manager_config() -> MongoConfig:
    settings = load_settings()
    return MongoConfig(
        uri=settings.mongodb_uri,
        db_name=settings.mongodb_db,
        simulate_slow_init_seconds=settings.simulate_slow_init_seconds,
    )


def create_manager(manager_type: type[ManagerT]) -> ManagerT:
    return manager_type(build_manager_config())