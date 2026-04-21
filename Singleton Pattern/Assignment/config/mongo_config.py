import os
from pathlib import Path


def load_dotenv_file() -> None:
	project_root = Path(__file__).resolve().parents[1]
	env_file = project_root / ".env"

	if not env_file.exists():
		return

	for raw_line in env_file.read_text(encoding="utf-8").splitlines():
		line = raw_line.strip()
		if not line or line.startswith("#") or "=" not in line:
			continue
		key, value = line.split("=", 1)
		os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def get_mongo_config() -> dict:
	load_dotenv_file()
	return {
		"uri": os.getenv("MONGODB_URI", "mongodb://localhost:27017"),
		"database_name": os.getenv("MONGODB_DB", "singleton_assignment_db"),
		"slow_init_seconds": float(os.getenv("SIMULATE_SLOW_INIT_SECONDS", "0")),
	}
