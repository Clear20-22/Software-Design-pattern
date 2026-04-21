import time

from pymongo import MongoClient

from config.mongo_config import get_mongo_config


class BaseMongoManager:
	def __init__(self, uri: str | None = None, database_name: str | None = None) -> None:
		config = get_mongo_config()
		self.uri = uri or config["uri"]
		self.database_name = database_name or config["database_name"]
		slow_init_seconds = config["slow_init_seconds"]
		if slow_init_seconds > 0:
			time.sleep(slow_init_seconds)
		self.client = MongoClient(self.uri)

	def get_client(self) -> MongoClient:
		return self.client

	def get_database(self):
		return self.client[self.database_name]

	def get_collection(self, name: str):
		return self.get_database()[name]

	def close_connection(self) -> None:
		if self.client is not None:
			self.client.close()
