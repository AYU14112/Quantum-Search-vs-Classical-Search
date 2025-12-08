# linear_search.py
"""
Linear (classical) search module.
Provides `linear_search_once()` and `linear_search_repeated()`.

Usage:
    from linear_search import linear_search_once
    res = linear_search_once(dataset, target)
"""

import time
import numpy as np

def now():
    return time.perf_counter()

def linear_search_once(dataset, target):
    """
    Perform linear search and return:
    {
      'index': int,
      'steps': int,            # number of comparisons
      'elapsed_c_impl': float, # time using dataset.index (C-optimized)
      'elapsed_py_impl': float # time using explicit Python loop
    }
    """
    t0 = now()
    try:
        idx_c = dataset.index(target)
        elapsed_c = now() - t0
    except ValueError:
        idx_c = -1
        elapsed_c = now() - t0

    steps = 0
    idx_py = -1
    t0 = now()
    for i, v in enumerate(dataset):
        steps += 1
        if v == target:
            idx_py = i
            break
    elapsed_py = now() - t0

    idx = idx_c if idx_c != -1 else idx_py
    return {
        'index': idx,
        'steps': steps,
        'elapsed_c_impl': elapsed_c,
        'elapsed_py_impl': elapsed_py
    }

def linear_search_repeated(dataset, target, repeats=3):
    records = []
    for _ in range(repeats):
        records.append(linear_search_once(dataset, target))
    steps = int(np.median([r['steps'] for r in records]))
    elapsed_c = float(np.median([r['elapsed_c_impl'] for r in records]))
    elapsed_py = float(np.median([r['elapsed_py_impl'] for r in records]))
    index = records[0]['index']
    return {
        'index': index,
        'steps': steps,
        'elapsed_c_impl': elapsed_c,
        'elapsed_py_impl': elapsed_py
    }

if __name__ == "__main__":
    # demo
    data = list(range(32))
    print("Linear search demo; searching target 15 in range(32)")
    print(linear_search_once(data, 15))
