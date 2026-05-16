from database.base_manager import BaseMongoManager


class EnumMongoManager(BaseMongoManager):
	pass


class _EnumMember:
	def __init__(self, value: EnumMongoManager) -> None:
		self.value = value


class MongoManagerEnum:
	# Manual "enum-like" container (no use of Python's built-in enum.Enum).
	INSTANCE = _EnumMember(EnumMongoManager())


def get_instance() -> EnumMongoManager:
	return MongoManagerEnum.INSTANCE.value
