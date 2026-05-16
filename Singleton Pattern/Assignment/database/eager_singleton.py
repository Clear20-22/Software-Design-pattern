from database.base_manager import BaseMongoManager


class EagerMongoManager(BaseMongoManager):
	pass


class _EagerHolder:
	instance = EagerMongoManager()


def get_instance() -> EagerMongoManager:
	return _EagerHolder.instance
