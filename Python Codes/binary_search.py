# binary_search.py
"""
Binary search module with optional sorting.
Provides:
 - binary_search_once(sorted_dataset, target)
 - binary_search_with_optional_sort(dataset, target, do_sort=True)

Usage:
    from binary_search import binary_search_with_optional_sort
    res = binary_search_with_optional_sort(dataset, target, do_sort=True)
"""

import time
import numpy as np

def now():
    return time.perf_counter()

def binary_search_once(sorted_dataset, target):
    """
    Perform iterative binary search on an already-sorted list.
    Returns:
    {
      'index': int,
      'steps': int,
      'elapsed_search': float
    }
    """
    lo, hi = 0, len(sorted_dataset) - 1
    steps = 0
    t0 = now()
    while lo <= hi:
        mid = (lo + hi) // 2
        steps += 1
        if sorted_dataset[mid] == target:
            return {'index': mid, 'steps': steps, 'elapsed_search': now() - t0}
        elif sorted_dataset[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return {'index': -1, 'steps': steps, 'elapsed_search': now() - t0}

def binary_search_with_optional_sort(dataset, target, do_sort=True):
    """
    If do_sort=True, measures sort time then runs binary search.
    If do_sort=False, assumes `dataset` is already sorted.
    Returns:
    {
      'index': int,
      'steps': int,
      'elapsed_sort': float,
      'elapsed_search': float,
      'elapsed_total': float
    }
    """
    sort_time = 0.0
    if do_sort:
        t0 = now()
        sorted_dataset = sorted(dataset)
        sort_time = now() - t0
    else:
        sorted_dataset = dataset

    bs = binary_search_once(sorted_dataset, target)
    elapsed_total = sort_time + bs['elapsed_search']
    return {
        'index': bs['index'],
        'steps': bs['steps'],
        'elapsed_sort': sort_time,
        'elapsed_search': bs['elapsed_search'],
        'elapsed_total': elapsed_total
    }

if __name__ == "__main__":
    ds = [5, 2, 9, 1, 7, 3]
    print("Binary search (with sort) demo searching 7")
    print(binary_search_with_optional_sort(ds, 7, do_sort=True))
