# binary_search.py
"""
Binary search module with optional sorting.
Exports:
 - binary_search_with_optional_sort(dataset, target, do_sort=True, repeats=3)
 - pretty_print_binary_result
 - plot_binary_search_steps (visualization of steps on a sorted list)
"""
import time
import numpy as np
import matplotlib.pyplot as plt

def now():
    return time.perf_counter()

def binary_search_once(sorted_dataset, target):
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
    sort_time = 0.0
    if do_sort:
        t0 = now()
        sorted_dataset = sorted(dataset)
        sort_time = now() - t0
    else:
        sorted_dataset = dataset
    bs = binary_search_once(sorted_dataset, target)
    return {
        'index': int(bs['index']),
        'steps': int(bs['steps']),
        'elapsed_sort': float(sort_time),
        'elapsed_search': float(bs['elapsed_search']),
        'elapsed_total': float(sort_time + bs['elapsed_search']),
        'sorted_dataset': sorted_dataset
    }

def pretty_print_binary_result(res):
    print("\n--- Binary Search Result ---")
    print(f"Index found: {res['index']}")
    print(f"Comparisons (binary steps): {res['steps']}")
    print(f"Sort time: {res['elapsed_sort']:.6e} s")
    print(f"Search time: {res['elapsed_search']:.6e} s")
    print(f"Total time: {res['elapsed_total']:.6e} s")
    print("-----------------------------\n")

def plot_binary_search_steps(res):
    sd = res.get('sorted_dataset', [])
    if not sd:
        print("No sorted dataset available for plotting.")
        return
    N = len(sd)
    # we'll illustrate possible mid-checks by simulating the binary search again collecting mids
    mids = []
    lo, hi = 0, N - 1
    target = sd[res['index']] if 0 <= res['index'] < N else None
    while lo <= hi:
        mid = (lo + hi) // 2
        mids.append(mid)
        if sd[mid] == target:
            break
        elif sd[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    plt.figure(figsize=(10,2))
    plt.scatter(range(N), [1]*N, c='lightgray', s=40)
    plt.scatter(mids, [1]*len(mids), c='red', s=80, label='mid checks')
    plt.yticks([])
    plt.xlabel('Index')
    plt.title(f'Binary search mid checks (N={N})')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    ds = [5,2,9,1,7,3]
    res = binary_search_with_optional_sort(ds, 7, do_sort=True)
    pretty_print_binary_result(res)
    plot_binary_search_steps(res)
