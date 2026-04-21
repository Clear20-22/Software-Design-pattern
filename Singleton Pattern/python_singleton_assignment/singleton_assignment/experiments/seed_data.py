from __future__ import annotations

import os
import random
import time
from datetime import datetime, timezone

from ..singletons import enum_based_manager
from ._results import write_json


def main() -> None:
    # Config via env (keeps it simple to run as `python -m ...`)
    collections_raw = os.environ.get("SEED_COLLECTIONS", "").strip()
    if collections_raw:
        collection_names = [c.strip() for c in collections_raw.split(",") if c.strip()]
    else:
        # Default: create multiple collections so `explore_db` shows something meaningful.
        collection_names = [
            os.environ.get("SEED_COLLECTION", "singleton_assignment_items").strip(),
            "singleton_assignment_events",
        ]
    doc_count = int(os.environ.get("SEED_COUNT", "200"))
    clear_first = os.environ.get("SEED_CLEAR", "true").lower() in {"1", "true", "yes", "y"}
    rng_seed = int(os.environ.get("SEED_RANDOM_SEED", "42"))

    random.seed(rng_seed)

    manager = enum_based_manager()
    now = datetime.now(timezone.utc)
    categories = ["alpha", "beta", "gamma", "delta"]

    per_collection: list[dict[str, object]] = []
    total_inserted = 0
    total_elapsed = 0.0

    for collection_name in collection_names:
        collection_name = collection_name.strip()
        if not collection_name:
            continue

        collection = manager.get_collection(collection_name)
        if clear_first:
            collection.drop()
            collection = manager.get_collection(collection_name)
            collection.create_index("created_at")
            collection.create_index("category")

        docs = []
        for i in range(doc_count):
            docs.append(
                {
                    "seq": i + 1,
                    "category": random.choice(categories),
                    "value": random.randint(1, 10_000),
                    "active": random.choice([True, False]),
                    "created_at": now,
                }
            )

        start = time.perf_counter()
        result = collection.insert_many(docs, ordered=False)
        elapsed = time.perf_counter() - start

        inserted = len(result.inserted_ids)
        total_inserted += inserted
        total_elapsed += elapsed
        per_collection.append(
            {
                "collection": collection_name,
                "inserted_count": inserted,
                "elapsed_seconds": elapsed,
            }
        )

    payload = {
        "kind": "seed_data",
        "collections": per_collection,
        "total_inserted_count": total_inserted,
        "total_elapsed_seconds": total_elapsed,
        "clear_first": clear_first,
        "doc_count_requested_per_collection": doc_count,
    }
    out_path = write_json("seed_data", payload)

    for row in per_collection:
        print(
            f"Seeded `{row['collection']}`: inserted={row['inserted_count']} "
            f"in {float(row['elapsed_seconds']):.3f}s (clear_first={clear_first})"
        )
    print(f"Wrote: {out_path}")


if __name__ == "__main__":
    main()
