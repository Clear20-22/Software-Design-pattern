from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any


RESULTS_DIR = Path(__file__).resolve().parents[1] / "results"
REPORT_OUT = Path(__file__).resolve().parent / "REPORT.generated.md"


def _latest_json(prefix: str) -> Path:
    candidates = sorted(RESULTS_DIR.glob(f"{prefix}-*.json"))
    if not candidates:
        raise RuntimeError(f"No results found for {prefix}. Run the experiments first.")
    return candidates[-1]


def _load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


@dataclass
class InstanceRow:
    implementation: str
    unique_instance_ids: int
    unique_client_ids: int


@dataclass
class ThreadRow:
    implementation: str
    threads: int
    unique_instance_ids: int


@dataclass
class PerfRow:
    implementation: str
    init_seconds: float
    access_seconds_per_call: float


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    instance_payload = _load(_latest_json("instance_validation"))
    thread_payload = _load(_latest_json("thread_safety"))
    perf_payload = _load(_latest_json("performance"))

    instance_rows = [
        InstanceRow(
            implementation=r["implementation"],
            unique_instance_ids=r["unique_instance_ids"],
            unique_client_ids=r["unique_client_ids"],
        )
        for r in instance_payload["rows"]
    ]
    thread_rows = [
        ThreadRow(
            implementation=r["implementation"],
            threads=r["threads"],
            unique_instance_ids=r["unique_instance_ids"],
        )
        for r in thread_payload["rows"]
    ]
    perf_rows = [
        PerfRow(
            implementation=r["implementation"],
            init_seconds=float(r["init_seconds"]),
            access_seconds_per_call=float(r["access_seconds_per_call"]),
        )
        for r in perf_payload["rows"]
    ]

    def md_table(headers: list[str], rows: list[list[str]]) -> str:
        lines = []
        lines.append("| " + " | ".join(headers) + " |")
        lines.append("|" + "|".join(["---"] * len(headers)) + "|")
        for row in rows:
            lines.append("| " + " | ".join(row) + " |")
        return "\n".join(lines)

    report = []
    report.append("# Singleton Pattern (Python) — Experiment Results Report\n")
    report.append("## 1) Instance Validation Results\n")
    report.append(
        md_table(
            ["Implementation", "Unique instance IDs", "Unique MongoClient IDs", "Notes"],
            [
                [r.implementation, str(r.unique_instance_ids), str(r.unique_client_ids), ""]
                for r in instance_rows
            ],
        )
    )
    report.append("\n## 2) Multithreading Results\n")
    report.append(
        md_table(
            ["Implementation", "Threads", "Unique instance IDs", "Notes"],
            [
                [r.implementation, str(r.threads), str(r.unique_instance_ids), ""]
                for r in thread_rows
            ],
        )
    )
    report.append("\n## 3) Performance Measurements\n")
    report.append(
        md_table(
            ["Implementation", "Init (s)", "Access (µs/call)", "Notes"],
            [
                [
                    r.implementation,
                    f"{r.init_seconds:.6f}",
                    f"{(r.access_seconds_per_call * 1e6):.2f}",
                    "",
                ]
                for r in perf_rows
            ],
        )
    )
    report.append("\n## 4) Comparative Summary (Based on Results Only)\n")
    report.append("- Fastest access:\n- Safest under concurrency:\n- Inconsistencies observed:\n")

    REPORT_OUT.write_text("\n".join(report).strip() + "\n", encoding="utf-8")
    print(f"Wrote: {REPORT_OUT}")


if __name__ == "__main__":
    main()

