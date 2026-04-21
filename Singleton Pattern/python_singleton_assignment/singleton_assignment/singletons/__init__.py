from __future__ import annotations

from .eager import get_manager as eager_manager
from .lazy_basic import get_manager as lazy_basic_manager
from .synchronized_method import get_manager as synchronized_method_manager
from .double_checked_locking import get_manager as double_checked_locking_manager
from .bill_pugh import get_manager as bill_pugh_manager
from .enum_based import get_manager as enum_based_manager


ALL_SINGLETONS = {
    "Eager Initialization": eager_manager,
    "Lazy Initialization (basic)": lazy_basic_manager,
    "Synchronized Method": synchronized_method_manager,
    "Double-Checked Locking": double_checked_locking_manager,
    "Bill Pugh Implementation": bill_pugh_manager,
    "Enum-based Singleton": enum_based_manager,
}

