from enum import Enum

from database.base_manager import BaseMongoManager


class EnumMongoManager(BaseMongoManager):
	pass


class MongoManagerEnum(Enum):
	INSTANCE = EnumMongoManager()


def get_instance() -> EnumMongoManager:
	return MongoManagerEnum.INSTANCE.value
