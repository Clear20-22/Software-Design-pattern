from __future__ import annotations

from ..mongo_base import MongoConnectionManagerBase
from ._shared import create_manager


class EagerMongoConnectionManager(MongoConnectionManagerBase):
    pass


_INSTANCE = create_manager(EagerMongoConnectionManager)


def get_manager() -> EagerMongoConnectionManager:
    return _INSTANCE

