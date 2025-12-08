# main.py
"""
Interactive main program to run/search/benchmark and plot.
Imports the three algorithm modules and allows selecting dataset, params, and runs.

Usage:
    python main.py
"""

import sys
import math
import random
import numpy as np
import matplotlib.pyplot as plt

from quantum_search import run_grover_repeated, run_grover_once
from linear_search import linear_search_repeated, linear_search_once
from binary_search import binary_search_with_optional_sort, binary_search_once

def choose_int(prompt, default=None, minv=None, maxv=None):
    while True:
        try:
            s = input(f"{prompt} " + (f"[default={default}]: " if default is not None else ": "))
            if s.strip() == "" and default is not None:
                return default
            v = int(s)
            if minv is not None and v < minv:
                print("Value too small.")
                continue
            if maxv is not None and v > maxv:
                print("Value too large.")
                continue
            return v
        except ValueError:
            print("Enter an integer.")

def choose_yesno(prompt, default=True):
    d = 'Y/n' if default else 'y/N'
    while True:
        s = input(f"{prompt} [{d}]: ").strip().lower()
        if s == "" :
            return default
        if s in ('y', 'yes'):
            return True
        if s in ('n', 'no'):
            return False
        print("Enter y or n.")

def build_dataset(size, sorted_flag=True, shuffle_before=False):
    # size: integer number of elements (not qubit-based)
    dataset = list(range(size))
    if not sorted_flag and shuffle_before:
        random.shuffle(dataset)
    return dataset

def run_single_algorithm():
    print("\nChoose algorithm:\n1) Quantum (Grover)\n2) Linear (classical)\n3) Binary (with optional sort)\n4) Quit")
    choice = choose_int("Select 1/2/3/4", default=1, minv=1, maxv=4)
    if choice == 4:
        sys.exit(0)

    if choice == 1:
        # Quantum-specific parameters
        n_qubits = choose_int("Number of qubits (n) (dataset size = 2^n)", default=4, minv=1, maxv=12)
        N = 2 ** n_qubits
        target = choose_int(f"Target index (0..{N-1})", default=N//2, minv=0, maxv=N-1)
        shots = choose_int("Shots (measurements)", default=1024, minv=16)
        repeats = choose_int("Repeats (median)", default=3, minv=1)
        print(f"Running Grover: n_qubits={n_qubits}, target={target}, shots={shots}, repeats={repeats}")
        res = run_grover_repeated(target=target, n_qubits=n_qubits, shots=shots, repeats=repeats)
        print("Result (medians):")
        print(res)
        # optional distribution plot
        if choose_yesno("Plot measurement distribution?"):
            counts = res.get('counts', {})
            states = sorted(counts.keys(), key=lambda s: int(s,2))
            values = [counts[s] for s in states]
            plt.figure(figsize=(10,5))
            plt.bar(range(len(states)), values, tick_label=states)
            plt.title(f"Grover counts (target={target})")
            plt.xlabel("States")
            plt.ylabel("Counts")
            plt.show()

    elif choice == 2:
        size = choose_int("Dataset size (N)", default=1024, minv=1)
        sorted_flag = choose_yesno("Is the dataset sorted (if no it will be unsorted)?", default=True)
        if not sorted_flag:
            # unsorted dataset; linear search doesn't care
            dataset = build_dataset(size, sorted_flag=False, shuffle_before=True)
        else:
            dataset = build_dataset(size, sorted_flag=True)
        target = choose_int(f"Target index (0..{size-1})", default=size//2, minv=0, maxv=size-1)
        repeats = choose_int("Repeats (median)", default=3, minv=1)
        res = linear_search_repeated(dataset, target, repeats=repeats)
        print("Linear search result (medians):")
        print(res)

    elif choice == 3:
        size = choose_int("Dataset size (N)", default=1024, minv=1)
        sorted_flag = choose_yesno("Is the dataset already sorted?", default=False)
        dataset = build_dataset(size, sorted_flag=sorted_flag, shuffle_before=not sorted_flag)
        target = choose_int(f"Target index (0..{size-1})", default=size//2, minv=0, maxv=size-1)
        do_sort = not sorted_flag  # if dataset is not sorted, we will sort inside function
        res = binary_search_with_optional_sort(dataset, target, do_sort=do_sort)
        print("Binary search result:")
        print(res)

def run_scalability_compare():
    """
    Runs all three algorithms across sizes and plots steps/times.
    For Quantum we use n_qubits range; for Classical/Binary we use sizes that are 2^n.
    """
    max_qubits = choose_int("Max qubits to test (n)", default=6, minv=1, maxv=12)
    shots = choose_int("Quantum shots", default=512, minv=32)
    repeats = choose_int("Repeats (median) for each point", default=2, minv=1)
    unsorted_for_binary = choose_yesno("When comparing include sort cost for binary (unsorted single-query)?", default=True)

    sizes = [2 ** n for n in range(1, max_qubits + 1)]

    classical_steps = []
    classical_times = []
    binary_total_times = []
    binary_sort_times = []
    binary_search_times = []
    quantum_iters = []
    quantum_times = []
    quantum_success = []

    for n in range(1, max_qubits + 1):
        N = 2 ** n
        target = N // 2

        # classical
        ds_sorted = list(range(N))
        ds_unsorted = ds_sorted.copy()
        random_shuffle = True
        if random_shuffle:
            random.shuffle(ds_unsorted)
        ds_for_classical = ds_unsorted  # test on unsorted
        lin = linear_search_repeated(ds_for_classical, target, repeats=repeats)
        classical_steps.append(lin['steps'])
        classical_times.append(lin['elapsed_py_impl'])

        # binary
        ds_for_binary = ds_unsorted.copy()
        b = binary_search_with_optional_sort(ds_for_binary, target, do_sort=unsorted_for_binary)
        binary_total_times.append(b['elapsed_total'])
        binary_sort_times.append(b['elapsed_sort'])
        binary_search_times.append(b['elapsed_search'])

        # quantum
        q = run_grover_repeated(target=target, n_qubits=n, shots=shots, repeats=repeats)
        quantum_iters.append(q['iterations'])
        quantum_times.append(q['elapsed_exec_time'])
        quantum_success.append(q['success_rate'])

        print(f"n={n} (N={N}) -> linear steps={lin['steps']}, binary_total_ms={b['elapsed_total']*1000:.2f}, quantum_iters={q['iterations']}")

    # plotting
    Ns = np.array(sizes)
    plt.figure(figsize=(10,6))
    plt.plot(Ns, classical_steps, 'o-', label='Classical steps (measured)')
    plt.plot(Ns, quantum_iters, 's-', label='Quantum iterations (measured)')
    # approximate binary steps: log2(N)
    plt.plot(Ns, np.log2(Ns), '^-', label='Binary comparisons (theory log2(N))')
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Dataset size N (log scale)')
    plt.ylabel('Steps / Iterations (log scale)')
    plt.title('Steps: Classical vs Quantum vs Binary (theory)')
    plt.legend()
    plt.grid(alpha=0.3)
    plt.show()

    plt.figure(figsize=(10,6))
    plt.plot(Ns, np.array(classical_times)*1000, 'o-', label='Classical time (ms)')
    plt.plot(Ns, np.array(quantum_times)*1000, 's-', label='Quantum time (ms)')
    plt.plot(Ns, np.array(binary_total_times)*1000, '^-', label='Binary total (ms)')
    if any(binary_sort_times):
        plt.plot(Ns, np.array(binary_sort_times)*1000, ':', label='Binary sort time (ms)')
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Dataset size N (log scale)')
    plt.ylabel('Time (ms, log scale)')
    plt.title('Wall-clock times: Classical vs Quantum vs Binary')
    plt.legend()
    plt.grid(alpha=0.3)
    plt.show()

def main_menu():
    print("\n==== Search Benchmark Suite ====")
    print("1) Run a single algorithm")
    print("2) Run scalability comparison (quantum/linear/binary) across sizes and plot")
    print("3) Quit")
    choice = choose_int("Choose 1/2/3", default=2, minv=1, maxv=3)
    if choice == 1:
        run_single_algorithm()
    elif choice == 2:
        run_scalability_compare()
    else:
        print("Exiting.")
        sys.exit(0)

if __name__ == "__main__":
    print("Welcome — Search Benchmark Main")
    while True:
        main_menu()
        if not choose_yesno("Run again? (y for menu)", default=True):
            print("Goodbye.")
            break
