# Singleton Assignment (Python + MongoDB)

This project shows 6 Singleton pattern implementations with a MongoDB connection manager using `pymongo`.

## Implemented Singletons

1. Eager Initialization
2. Lazy Initialization
3. Synchronized Method (thread-safe)
4. Double-Checked Locking
5. Bill Pugh (holder class style)
6. Enum-style Singleton (manual, no `enum.Enum`)

## Project Structure

- `config/mongo_config.py`: MongoDB config
- `database/base_manager.py`: base Mongo manager
- `database/*.py`: singleton versions
- `experiments/instance_validation.py`: checks object IDs
- `experiments/threading_test.py`: threading test
- `experiments/performance_test.py`: simple timing
- `main.py`: runs all experiments

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in project root:

```env
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB=singleton_assignment_db
```

The project reads these values from `.env` automatically.

Optional environment variables (if you want to override `.env`):

- `MONGODB_URI` (default: `mongodb://localhost:27017`)
- `MONGODB_DB` (default: `singleton_assignment_db`)

## Run

Run all tests:

```bash
python main.py
```

Run individually:

```bash
python experiments/instance_validation.py
python experiments/threading_test.py
python experiments/performance_test.py
```

## Results Report

- Markdown report: `report/results.md`
- Interactive HTML report (with p5.js animation): `report/results.html`

Open the HTML report in browser:

```bash
open report/results.html
```
