# linear_search.py
"""
Linear search module with pretty printing and optional simple plotting support.
Exports:
 - linear_search_once(dataset, target)
 - linear_search_repeated(dataset, target, repeats=3)
 - pretty_print_linear_result(result)
"""
import time
import numpy as np
import matplotlib.pyplot as plt

def now():
    return time.perf_counter()

def linear_search_once(dataset, target):
    """Return dict: index, steps, elapsed_c_impl, elapsed_py_impl"""
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
        'index': int(idx),
        'steps': int(steps),
        'elapsed_c_impl': float(elapsed_c),
        'elapsed_py_impl': float(elapsed_py)
    }

def linear_search_repeated(dataset, target, repeats=3):
    recs = [linear_search_once(dataset, target) for _ in range(repeats)]
    return {
        'index': recs[0]['index'],
        'steps': int(np.median([r['steps'] for r in recs])),
        'elapsed_c_impl': float(np.median([r['elapsed_c_impl'] for r in recs])),
        'elapsed_py_impl': float(np.median([r['elapsed_py_impl'] for r in recs]))
    }

def pretty_print_linear_result(res):
    print("\n--- Linear Search Result ---")
    print(f"Index found: {res['index']}")
    print(f"Steps (comparisons): {res['steps']}")
    print(f"Time (C-optimized .index): {res['elapsed_c_impl']:.6e} s")
    print(f"Time (Python loop): {res['elapsed_py_impl']:.6e} s")
    print("----------------------------\n")

def plot_linear_result(res, dataset_size):
    # simple bar: python vs c implementation times
    labels = ['C impl (.index)', 'Python loop']
    times = [res['elapsed_c_impl'] * 1000, res['elapsed_py_impl'] * 1000]  # ms
    plt.figure(figsize=(6,4))
    plt.bar(labels, times)
    plt.ylabel('Time (ms)')
    plt.title(f'Linear search timing (N={dataset_size})')
    plt.show()

if __name__ == "__main__":
    data = list(range(32))
    out = linear_search_repeated(data, 15, repeats=3)
    pretty_print_linear_result(out)
    plot_linear_result(out, len(data))
