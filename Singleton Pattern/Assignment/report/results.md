# Singleton Pattern Experiment Report (Results Only)

Date: 22 April 2026
Project: Assignment (Python + MongoDB)

## 1) Instance Validation Results

Goal: confirm repeated creation calls return the same object and same MongoDB client.

Method:

- For each implementation, call `get_instance()` two times.
- Print object IDs and compare with `is`.
- Print MongoClient object identity using `get_client()`.

Raw output (captured):

```
Eager: object_id_1=4402143856, object_id_2=4402143856, same_instance=True, same_client=True
Lazy: object_id_1=4406698608, object_id_2=4406698608, same_instance=True, same_client=True
Synchronized: object_id_1=4406698944, object_id_2=4406698944, same_instance=True, same_client=True
DoubleChecked: object_id_1=4406700624, object_id_2=4406700624, same_instance=True, same_client=True
BillPugh: object_id_1=4402149568, object_id_2=4402149568, same_instance=True, same_client=True
Enum: object_id_1=4406697936, object_id_2=4406697936, same_instance=True, same_client=True
```

Table:

| Implementation | Same instance | Same MongoClient | Evidence                   |
| -------------- | ------------- | ---------------- | -------------------------- |
| Eager          | Yes           | Yes              | object_id_1 == object_id_2 |
| Lazy           | Yes           | Yes              | object_id_1 == object_id_2 |
| Synchronized   | Yes           | Yes              | object_id_1 == object_id_2 |
| DoubleChecked  | Yes           | Yes              | object_id_1 == object_id_2 |
| BillPugh       | Yes           | Yes              | object_id_1 == object_id_2 |
| Enum           | Yes           | Yes              | object_id_1 == object_id_2 |

Observation:

- In single-thread repeated access, all six implementations behaved as singletons.

## 2) Multithreading Results

Goal: detect singleton failures under concurrent access.

Method:

- Spawn 20 threads per implementation.
- Each thread gets instance + client and stores object IDs.
- Count unique object IDs and unique client IDs.

Raw output (captured):

```
Eager: unique_objects=1, unique_clients=1
Lazy: unique_objects=20, unique_clients=20
Synchronized: unique_objects=1, unique_clients=1
DoubleChecked: unique_objects=1, unique_clients=1
BillPugh: unique_objects=1, unique_clients=1
Enum: unique_objects=1, unique_clients=1
```

Table:

| Implementation | Threads | Unique object IDs | Unique client IDs | Thread-safe result |
| -------------- | ------: | ----------------: | ----------------: | ------------------ |
| Eager          |      20 |                 1 |                 1 | Pass               |
| Lazy           |      20 |                20 |                20 | Fail               |
| Synchronized   |      20 |                 1 |                 1 | Pass               |
| DoubleChecked  |      20 |                 1 |                 1 | Pass               |
| BillPugh       |      20 |                 1 |                 1 | Pass               |
| Enum           |      20 |                 1 |                 1 | Pass               |

Observation:

- Lazy singleton (basic version) is not thread-safe; it produced multiple instances and multiple clients under concurrency.
- All synchronized/thread-safe implementations remained consistent.

## 3) Performance Measurements

Goal: compare first initialization cost and repeated access cost.

Method:

- First access: one call to `get_instance()` and measure elapsed seconds.
- Repeated access: 100,000 calls and compute average microseconds per call.

Raw output (captured):

```
Eager: first_access=0.00000000s, avg_access=0.0198us
Lazy: first_access=0.06866884s, avg_access=0.1395us
Synchronized: first_access=0.04609585s, avg_access=0.1591us
DoubleChecked: first_access=0.04338217s, avg_access=0.0759us
BillPugh: first_access=0.04553294s, avg_access=0.0430us
Enum: first_access=0.00000286s, avg_access=0.0834us
```

Table:

| Implementation | First access (s) | Average access (us) |
| -------------- | ---------------: | ------------------: |
| Eager          |       0.00000000 |              0.0198 |
| Lazy           |       0.06866884 |              0.1395 |
| Synchronized   |       0.04609585 |              0.1591 |
| DoubleChecked  |       0.04338217 |              0.0759 |
| BillPugh       |       0.04553294 |              0.0430 |
| Enum           |       0.00000286 |              0.0834 |

Observation:

- Eager had the lowest repeated access time in this run.
- Synchronized had the highest repeated access time in this run.

## 4) Comparative Summary (Observed Data Only)

- Fastest average access in this run: Eager (0.0198 us).
- Most expensive average access in this run: Synchronized (0.1591 us).
- Consistent under thread test: Eager, Synchronized, DoubleChecked, BillPugh, Enum.
- Inconsistent under thread test: Lazy (20 unique instances with 20 threads, so not thread-safe).
- Single-thread repeated instantiation: all six returned same instance and same client.
