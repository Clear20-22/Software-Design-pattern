from database.base_manager import BaseMongoManager


class EagerMongoManager(BaseMongoManager):
	pass


_instance = EagerMongoManager()


def get_instance() -> EagerMongoManager:
	return _instance
