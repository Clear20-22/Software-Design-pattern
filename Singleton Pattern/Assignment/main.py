from experiments.instance_validation import run_instance_validation
from experiments.threading_test import run_threading_test
from experiments.performance_test import run_performance_test
from utils.logger import print_title


def close_all_connections() -> None:
	# We get each singleton once and close its underlying MongoClient.
	from database.eager_singleton import get_instance as eager
	from database.lazy_singleton import get_instance as lazy
	from database.synchronized_singleton import get_instance as sync
	from database.double_checked_locking import get_instance as dcl
	from database.bill_pugh_singleton import get_instance as bill_pugh
	from database.enum_singleton import get_instance as enum_singleton

	singleton_getters = [eager, lazy, sync, dcl, bill_pugh, enum_singleton]
	for get_singleton in singleton_getters:
		get_singleton().close_connection()


def main() -> None:
	print_title("Singleton Pattern Assignment - MongoDB")
	run_instance_validation()
	run_threading_test()
	run_performance_test()
	close_all_connections()
	print("\nDone.")


if __name__ == "__main__":
	main()
