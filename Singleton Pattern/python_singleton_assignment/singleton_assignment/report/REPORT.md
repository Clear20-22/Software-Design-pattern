# Singleton Pattern (Python) — Experiment Results Report

> Requirement: 2–4 pages, **results only**, data-driven.
>
> How to generate data:
> - `python -m singleton_assignment.experiments.instance_validation`
> - `python -m singleton_assignment.experiments.thread_safety`
> - `python -m singleton_assignment.experiments.performance`
>
> All outputs are saved as JSON in `singleton_assignment/results/`.
> You can also run `python -m singleton_assignment.report.generate_report` to produce a filled report draft.

## 1) Instance Validation Results

Include evidence that each implementation maintains (or fails to maintain) a single instance.

- Evidence used:
  - Object IDs / memory references (instance IDs)
  - MongoClient IDs (connection reuse)

Paste table here (or screenshots/logs):

| Implementation | Unique instance IDs | Unique MongoClient IDs | Notes |
|---|---:|---:|---|
| Eager Initialization |  |  |  |
| Lazy Initialization (basic) |  |  |  |
| Synchronized Method |  |  |  |
| Double-Checked Locking |  |  |  |
| Bill Pugh Implementation |  |  |  |
| Enum-based Singleton |  |  |  |

## 2) Multithreading Results

Concurrent access using Python `threading`:
- Number of threads:
- Barrier/race setup:

Paste results here (logs/tables/screenshots):

| Implementation | Threads | Unique instance IDs | Notes |
|---|---:|---:|---|
| Eager Initialization |  |  |  |
| Lazy Initialization (basic) |  |  |  |
| Synchronized Method |  |  |  |
| Double-Checked Locking |  |  |  |
| Bill Pugh Implementation |  |  |  |
| Enum-based Singleton |  |  |  |

## 3) Performance Measurements

Empirical comparison of:
- Initialization time (first access)
- Access time under repeated calls

Paste results here:

| Implementation | Init (s) | Access (µs/call) | Notes |
|---|---:|---:|---|
| Eager Initialization |  |  |  |
| Lazy Initialization (basic) |  |  |  |
| Synchronized Method |  |  |  |
| Double-Checked Locking |  |  |  |
| Bill Pugh Implementation |  |  |  |
| Enum-based Singleton |  |  |  |

## 4) Comparative Summary (Based on Results Only)

Summarize strictly from observed data:
- Fastest access:
- Safest under concurrency:
- Any inconsistencies observed:

