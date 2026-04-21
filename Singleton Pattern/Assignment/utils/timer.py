import time
from typing import Callable, Any


def measure_seconds(function: Callable, *args, **kwargs) -> tuple[Any, float]:
	start_time = time.time()
	result = function(*args, **kwargs)
	end_time = time.time()
	return result, end_time - start_time
