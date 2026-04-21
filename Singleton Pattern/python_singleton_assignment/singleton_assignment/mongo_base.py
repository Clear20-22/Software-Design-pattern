from __future__ import annotations

from dataclasses import dataclass
import threading
import time
from typing import Optional

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection


@dataclass(frozen=True)
class MongoConfig:
    uri: str
    db_name: str
    simulate_slow_init_seconds: float = 0.0


class MongoConnectionManagerBase:
    def __init__(self, config: MongoConfig) -> None:
        if config.simulate_slow_init_seconds > 0:
            time.sleep(config.simulate_slow_init_seconds)
        self._config = config
        self._client: Optional[MongoClient] = None
        self._client_lock = threading.Lock()

    def get_client(self) -> MongoClient:
        if self._client is not None:
            return self._client
        with self._client_lock:
            if self._client is None:
                self._client = MongoClient(self._config.uri)
        return self._client

    def get_database(self) -> Database:
        client = self.get_client()
        return client[self._config.db_name]

    def get_collection(self, name: str) -> Collection:
        return self.get_database()[name]

    def close_connection(self) -> None:
        with self._client_lock:
            if self._client is not None:
                self._client.close()
                self._client = None

