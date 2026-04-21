import threading

from database.base_manager import BaseMongoManager


class DoubleCheckedMongoManager(BaseMongoManager):
	_instance = None
	_lock = threading.Lock()

	@classmethod
	def get_instance(cls):
		if cls._instance is None:
			with cls._lock:
				if cls._instance is None:
					cls._instance = cls()
		return cls._instance


def get_instance() -> DoubleCheckedMongoManager:
	return DoubleCheckedMongoManager.get_instance()
