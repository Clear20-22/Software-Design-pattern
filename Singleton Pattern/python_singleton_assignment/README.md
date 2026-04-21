# Python Singleton Assignment (MongoDB)

This folder contains the full code + experiment scripts for `Singleton Pattern/Singleton Assignment.pdf`.

## Setup

1. Create a virtual environment and install dependencies:
   - `python -m venv .venv`
   - `source .venv/bin/activate`
   - `pip install -r requirements.txt`

2. Create your `.env` file (do **not** commit it):

   - Copy `env.example` to `.env`
   - Set at least:
     - `MONGODB_URI=...`
     - `MONGODB_DB=...`

## Run experiments

From this directory (`Singleton Pattern/python_singleton_assignment`):

- Instance validation:
  - `python -m singleton_assignment.experiments.instance_validation`
- Thread safety analysis:
  - `python -m singleton_assignment.experiments.thread_safety`
- Performance comparison:
  - `python -m singleton_assignment.experiments.performance`
- Seed sample data (optional):
  - `python -m singleton_assignment.experiments.seed_data`
- Explore DB/collections (optional):
  - `python -m singleton_assignment.experiments.explore_db`

Outputs are written to `singleton_assignment/results/`.

## Report

Use `singleton_assignment/report/REPORT.md` and paste the results produced by the scripts.

Optional: generate a pre-filled Markdown report from the latest JSON outputs:
- `python -m singleton_assignment.report.generate_report`
