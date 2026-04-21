from __future__ import annotations

import time

from ..singletons import ALL_SINGLETONS
from ._results import PerformanceRow, write_json


def main() -> None:
    access_iterations = 200_000
    rows: list[PerformanceRow] = []

    for name, factory in ALL_SINGLETONS.items():
        start = time.perf_counter()
        _ = factory()
        init_seconds = time.perf_counter() - start

        start = time.perf_counter()
        for _ in range(access_iterations):
            factory()
        access_seconds_total = time.perf_counter() - start

        rows.append(
            PerformanceRow(
                implementation=name,
                init_seconds=init_seconds,
                access_seconds_total=access_seconds_total,
                access_iterations=access_iterations,
            )
        )

    payload = {"kind": "performance", "rows": [r.to_dict() for r in rows]}
    out_path = write_json("performance", payload)

    for r in rows:
        print(
            f"{r.implementation}: init={r.init_seconds:.6f}s, "
            f"access/call={r.access_seconds_per_call * 1e6:.2f}us"
        )
    print(f"Wrote: {out_path}")


if __name__ == "__main__":
    main()

