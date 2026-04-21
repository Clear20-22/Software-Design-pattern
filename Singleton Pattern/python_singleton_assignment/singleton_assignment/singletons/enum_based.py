from __future__ import annotations

from enum import Enum

from ..mongo_base import MongoConnectionManagerBase
from ._shared import create_manager


class EnumMongoConnectionManager(MongoConnectionManagerBase):
    pass


class MongoManagerEnum(Enum):
    INSTANCE = create_manager(EnumMongoConnectionManager)


def get_manager() -> EnumMongoConnectionManager:
    return MongoManagerEnum.INSTANCE.value

