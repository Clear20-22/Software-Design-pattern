import threading

from database.base_manager import BaseMongoManager


class SynchronizedMongoManager(BaseMongoManager):
	_instance = None
	_lock = threading.Lock()

	@classmethod
	def get_instance(cls):
		with cls._lock:
			if cls._instance is None:
				cls._instance = cls()
		return cls._instance


def get_instance() -> SynchronizedMongoManager:
	return SynchronizedMongoManager.get_instance()
