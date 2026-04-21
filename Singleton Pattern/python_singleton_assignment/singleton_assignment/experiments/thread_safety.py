from __future__ import annotations

import threading
from typing import Callable

from ..singletons import ALL_SINGLETONS
from ._results import ThreadSafetyRow, write_json


def _run_concurrently(factory: Callable[[], object], threads: int) -> list[int]:
    barrier = threading.Barrier(threads)
    ids: list[int] = []
    ids_lock = threading.Lock()

    def worker() -> None:
        barrier.wait()
        obj = factory()
        with ids_lock:
            ids.append(id(obj))

    ts = [threading.Thread(target=worker, daemon=True) for _ in range(threads)]
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    return ids


def main() -> None:
    threads = 40
    rows: list[ThreadSafetyRow] = []

    for name, factory in ALL_SINGLETONS.items():
        instance_ids = _run_concurrently(factory, threads=threads)
        row = ThreadSafetyRow(
            implementation=name,
            threads=threads,
            unique_instance_ids=len(set(instance_ids)),
            instance_ids=sorted(instance_ids),
        )
        rows.append(row)

    payload = {"kind": "thread_safety", "rows": [r.to_dict() for r in rows]}
    out_path = write_json("thread_safety", payload)

    for r in rows:
        print(f"{r.implementation}: unique instances across {r.threads} threads = {r.unique_instance_ids}")
    print(f"Wrote: {out_path}")


if __name__ == "__main__":
    main()

