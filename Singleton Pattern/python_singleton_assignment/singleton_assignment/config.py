from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os


def _load_dotenv_if_present(dotenv_path: Path) -> None:
    if not dotenv_path.exists():
        return

    for raw_line in dotenv_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("'").strip('"')
        os.environ.setdefault(key, value)


@dataclass(frozen=True)
class Settings:
    mongodb_uri: str
    mongodb_db: str
    simulate_slow_init_seconds: float


def load_settings() -> Settings:
    # Local `.env` lives at: <repo>/Singleton Pattern/python_singleton_assignment/.env
    base_dir = Path(__file__).resolve().parents[1]
    _load_dotenv_if_present(base_dir / ".env")

    mongodb_uri = os.environ.get("MONGODB_URI", "").strip()
    mongodb_db = os.environ.get("MONGODB_DB", "").strip()
    if not mongodb_uri or not mongodb_db:
        raise RuntimeError(
            "Missing required config. Set MONGODB_URI and MONGODB_DB in `.env`."
        )

    simulate_slow_init_seconds = float(os.environ.get("SIMULATE_SLOW_INIT_SECONDS", "0"))
    return Settings(
        mongodb_uri=mongodb_uri,
        mongodb_db=mongodb_db,
        simulate_slow_init_seconds=simulate_slow_init_seconds,
    )

