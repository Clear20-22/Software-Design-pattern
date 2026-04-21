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


def run_instance_validation() -> None:
	print_title("Instance Validation")

	for name, factory in SINGLETONS.items():
		obj1 = factory()
		obj2 = factory()
		print(
			f"{name}: object_id_1={id(obj1)}, object_id_2={id(obj2)}, "
			f"same_instance={obj1 is obj2}, same_client={obj1.get_client() is obj2.get_client()}"
		)


if __name__ == "__main__":
	run_instance_validation()
