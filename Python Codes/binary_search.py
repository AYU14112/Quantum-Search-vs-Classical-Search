# binary_search.py
import time

def binary_search(dataset, target):
    t0 = time.perf_counter()
    dataset_sorted = sorted(dataset)
    sort_time = time.perf_counter() - t0

    lo, hi = 0, len(dataset_sorted) - 1
    steps = 0
    t1 = time.perf_counter()

    while lo <= hi:
        steps += 1
        mid = (lo + hi) // 2
        if dataset_sorted[mid] == target:
            return {
                "index": mid,
                "steps": steps,
                "sort_time": sort_time,
                "search_time": time.perf_counter() - t1
            }
        elif dataset_sorted[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1

    return {
        "index": -1,
        "steps": steps,
        "sort_time": sort_time,
        "search_time": time.perf_counter() - t1
    }

