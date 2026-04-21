from __future__ import annotations

from dataclasses import dataclass
import time
from typing import Any

from ..singletons import enum_based_manager
from ._results import write_json


@dataclass
class CollectionSummary:
    name: str
    estimated_count: int
    sample: dict[str, Any] | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "estimated_count": self.estimated_count,
            "sample": self.sample,
        }


def _stringify_for_json(value: Any) -> Any:
    # Make BSON-ish values (ObjectId, datetime, etc.) safe for JSON output.
    if isinstance(value, dict):
        return {str(k): _stringify_for_json(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_stringify_for_json(v) for v in value]
    try:
        import bson  # type: ignore

        if isinstance(value, bson.ObjectId):
            return str(value)
    except Exception:
        pass
    if hasattr(value, "isoformat"):
        try:
            return value.isoformat()
        except Exception:
            pass
    return value


def main() -> None:
    manager = enum_based_manager()
    db = manager.get_database()

    start = time.perf_counter()
    collection_names = sorted(db.list_collection_names())

    summaries: list[CollectionSummary] = []
    for name in collection_names:
        coll = db[name]
        estimated = int(coll.estimated_document_count())
        sample = coll.find_one()
        summaries.append(
            CollectionSummary(
                name=name,
                estimated_count=estimated,
                sample=_stringify_for_json(sample) if sample is not None else None,
            )
        )

    elapsed = time.perf_counter() - start

    payload = {
        "kind": "explore_db",
        "database": str(db.name),
        "collection_count": len(collection_names),
        "collections": [s.to_dict() for s in summaries],
        "elapsed_seconds": elapsed,
    }
    out_path = write_json("explore_db", payload)

    print(f"Database: {db.name} (collections={len(collection_names)})")
    for s in summaries:
        print(f"- {s.name}: ~{s.estimated_count} docs")
    print(f"Wrote: {out_path}")


if __name__ == "__main__":
    main()

