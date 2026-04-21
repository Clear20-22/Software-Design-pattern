import threading
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
	sys.path.insert(0, PROJECT_ROOT)

from database.eager_singleton import get_instance as get_eager
from database.lazy_singleton import get_instance as get_lazy
from database.synchronized_singleton import get_instance as get_sync
from database.double_checked_locking import get_instance as get_double_checked
from database.bill_pugh_singleton import get_instance as get_bill_pugh
from database.enum_singleton import get_instance as get_enum
from utils.logger import print_title


SINGLETONS = {
	"Eager": get_eager,
	"Lazy": get_lazy,
	"Synchronized": get_sync,
	"DoubleChecked": get_double_checked,
	"BillPugh": get_bill_pugh,
	"Enum": get_enum,
}


def run_for_one_singleton(name: str, factory, thread_count: int = 20) -> None:
	object_ids = []
	client_ids = []
	list_lock = threading.Lock()

	def worker() -> None:
		manager = factory()
		with list_lock:
			object_ids.append(id(manager))
			client_ids.append(id(manager.get_client()))

	threads = [threading.Thread(target=worker) for _ in range(thread_count)]

	for thread in threads:
		thread.start()
	for thread in threads:
		thread.join()

	print(
		f"{name}: unique_objects={len(set(object_ids))}, "
		f"unique_clients={len(set(client_ids))}"
	)


def run_threading_test() -> None:
	print_title("Threading Test")
	for name, factory in SINGLETONS.items():
		run_for_one_singleton(name, factory)


if __name__ == "__main__":
	run_threading_test()
