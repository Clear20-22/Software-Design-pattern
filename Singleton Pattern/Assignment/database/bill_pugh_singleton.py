import threading

from database.base_manager import BaseMongoManager


class BillPughMongoManager(BaseMongoManager):
	pass


class _Holder:
	instance = None
	lock = threading.Lock()


def get_instance() -> BillPughMongoManager:
	if _Holder.instance is None:
		with _Holder.lock:
			if _Holder.instance is None:
				_Holder.instance = BillPughMongoManager()
	return _Holder.instance
