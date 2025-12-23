# linear_search.py
import time

def linear_search(dataset, target):
    steps = 0
    t0 = time.perf_counter()
    for i, v in enumerate(dataset):
        steps += 1
        if v == target:
            return {
                "index": i,
                "steps": steps,
                "time": time.perf_counter() - t0
            }
    return {
        "index": -1,
        "steps": steps,
        "time": time.perf_counter() - t0
    }
