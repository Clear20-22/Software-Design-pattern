from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any


def results_dir() -> Path:
    return Path(__file__).resolve().parents[1] / "results"


def utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def write_json(name: str, payload: Any) -> Path:
    out_dir = results_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{name}-{utc_stamp()}.json"
    out_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return out_path


@dataclass
class InstanceValidationRow:
    implementation: str
    instance_ids: list[int]
    unique_instance_ids: int
    client_ids: list[int]
    unique_client_ids: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ThreadSafetyRow:
    implementation: str
    threads: int
    unique_instance_ids: int
    instance_ids: list[int]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class PerformanceRow:
    implementation: str
    init_seconds: float
    access_seconds_total: float
    access_iterations: int

    @property
    def access_seconds_per_call(self) -> float:
        return self.access_seconds_total / max(1, self.access_iterations)

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["access_seconds_per_call"] = self.access_seconds_per_call
        return d

