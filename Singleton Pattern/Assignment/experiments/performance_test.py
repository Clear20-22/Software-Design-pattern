import time
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


def run_performance_test(iterations: int = 100000) -> None:
	print_title("Performance Test")

	for name, factory in SINGLETONS.items():
		start = time.time()
		factory()
		first_access_time = time.time() - start

		start = time.time()
		for _ in range(iterations):
			factory()
		repeated_access_time = time.time() - start

		avg_microseconds = (repeated_access_time / iterations) * 1_000_000

		print(
			f"{name}: first_access={first_access_time:.8f}s, "
			f"avg_access={avg_microseconds:.4f}us"
		)


if __name__ == "__main__":
	run_performance_test()
