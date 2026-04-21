from __future__ import annotations

from ..singletons import ALL_SINGLETONS
from ._results import InstanceValidationRow, write_json


def main() -> None:
    rows: list[InstanceValidationRow] = []
    for name, factory in ALL_SINGLETONS.items():
        instances = [factory() for _ in range(5)]
        instance_ids = [id(x) for x in instances]
        client_ids = [id(x.get_client()) for x in instances]
        row = InstanceValidationRow(
            implementation=name,
            instance_ids=instance_ids,
            unique_instance_ids=len(set(instance_ids)),
            client_ids=client_ids,
            unique_client_ids=len(set(client_ids)),
        )
        rows.append(row)

    payload = {"kind": "instance_validation", "rows": [r.to_dict() for r in rows]}
    out_path = write_json("instance_validation", payload)

    for r in rows:
        print(
            f"{r.implementation}: unique instances={r.unique_instance_ids}, "
            f"unique clients={r.unique_client_ids}"
        )
    print(f"Wrote: {out_path}")


if __name__ == "__main__":
    main()

