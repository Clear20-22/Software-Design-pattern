from __future__ import annotations

import threading

from ..mongo_base import MongoConnectionManagerBase
from ._shared import create_manager


class BillPughMongoConnectionManager(MongoConnectionManagerBase):
    pass


class _Holder:
    instance: BillPughMongoConnectionManager | None = None
    lock = threading.Lock()


def _get_manager() -> BillPughMongoConnectionManager:
    if _Holder.instance is None:
        with _Holder.lock:
            if _Holder.instance is None:
                _Holder.instance = create_manager(BillPughMongoConnectionManager)
    return _Holder.instance


def get_manager() -> BillPughMongoConnectionManager:
    return _get_manager()
