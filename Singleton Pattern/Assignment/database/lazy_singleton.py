import time

from config.mongo_config import get_mongo_config
from database.base_manager import BaseMongoManager


class LazyMongoManager(BaseMongoManager):
	_instance = None

	def __new__(cls):
		if cls._instance is None:
			config = get_mongo_config()
			slow_init_seconds = config["slow_init_seconds"]
			if slow_init_seconds > 0:
				time.sleep(slow_init_seconds)
			cls._instance = super().__new__(cls)
		return cls._instance

	def __init__(self) -> None:
		if getattr(self, "_initialized", False):
			return
		super().__init__()
		self._initialized = True


def get_instance() -> LazyMongoManager:
	return LazyMongoManager()
