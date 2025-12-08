# main.py
"""
Main controller for Search Benchmark Suite (updated).
- CSV export for scalability runs
- Target placement modes (random, start, middle, end)
- Saves plots as PNG files (sc_steps.png, sc_times.png)
- Optional plotting for single-run tests
"""

import sys
import random
import csv
import numpy as np
import matplotlib.pyplot as plt

# Import the algorithm modules (ensure these files exist in the same directory)
import linear_search
import binary_search
import quantum_search

# -------------------------
# Utility input helpers
# -------------------------
def choose_int(prompt, default=None, minv=None, maxv=None):
    while True:
        full_prompt = prompt + (" " + (f"[default={default}]: " if default is not None else ": "))
        s = input(full_prompt)
        if s.strip() == "" and default is not None:
            return default
        try:
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
        if s == "":
            return default
        if s in ('y', 'yes'):
            return True
        if s in ('n', 'no'):
            return False
        print("Enter y or n.")

# -------------------------
# Dataset builder
# -------------------------
def build_dataset(size, sorted_flag=True, shuffle_before=False):
    ds = list(range(size))
    if not sorted_flag and shuffle_before:
        random.shuffle(ds)
    return ds

# -------------------------
# Single-run UI
# -------------------------
def run_single_algorithm_ui():
    print("\n--- Single Algorithm Test ---")
    print("1) Quantum (Grover)\n2) Linear (classical)\n3) Binary (with optional sort)\n4) Back")
    choice = choose_int("Select 1-4", default=1, minv=1, maxv=4)
    if choice == 4:
        return

    want_plot = choose_yesno("Do you want a plot for this single run?", default=True)

    if choice == 1:
        # Quantum
        n_qubits = choose_int("Number of qubits (n) (dataset size = 2^n)", default=4, minv=1, maxv=12)
        N = 2 ** n_qubits
        target = choose_int(f"Target index (0..{N-1})", default=N//2, minv=0, maxv=N-1)
        shots = choose_int("Shots (measurements)", default=1024, minv=16)
        repeats = choose_int("Repeats (median)", default=3, minv=1)
        print(f"\nRunning Grover: n_qubits={n_qubits}, target={target}, shots={shots}, repeats={repeats}")
        try:
            res = quantum_search.run_grover_repeated(target=target, n_qubits=n_qubits, shots=shots, repeats=repeats)
        except Exception as e:
            print("Quantum run failed (Qiskit may be missing or error occurred):", e)
            return
        print("\n--- Grover Result (median aggregated) ---")
        print(f"Iterations used: {res['iterations']}")
        print(f"Success rate: {res['success_rate']*100:.2f}%")
        print(f"Execution time (median): {res['elapsed_exec_time']:.3f} s")
        print(f"Transpile time (median): {res.get('transpile_time', 0.0):.3f} s")
        if want_plot:
            counts = res.get('counts', {})
            if counts:
                states = sorted(counts.keys(), key=lambda s: int(s,2))
                values = [counts[s] for s in states]
                plt.figure(figsize=(8,4))
                plt.bar(states, values)
                plt.xlabel('State')
                plt.ylabel('Counts')
                plt.title(f'Grover measurement distribution (target={target})')
                plt.xticks(rotation=45)
                plt.tight_layout()
                plt.show()
            else:
                print("No measurement counts to plot.")
        return

    if choice == 2:
        # Linear
        size = choose_int("Dataset size (N)", default=1024, minv=1)
        sorted_flag = choose_yesno("Is the dataset sorted? (if no, dataset will be unsorted)", default=True)
        ds = build_dataset(size, sorted_flag=sorted_flag, shuffle_before=(not sorted_flag))
        target = choose_int(f"Target index (0..{size-1})", default=size//2, minv=0, maxv=size-1)
        repeats = choose_int("Repeats (median)", default=3, minv=1)
        res = linear_search.linear_search_repeated(ds, target, repeats=repeats)
        linear_search.pretty_print_linear_result(res)
        if want_plot:
            linear_search.plot_linear_result(res, size)
        return

    if choice == 3:
        # Binary
        size = choose_int("Dataset size (N)", default=1024, minv=1)
        sorted_flag = choose_yesno("Is the dataset already sorted?", default=False)
        ds = build_dataset(size, sorted_flag=sorted_flag, shuffle_before=(not sorted_flag))
        target = choose_int(f"Target index (0..{size-1})", default=size//2, minv=0, maxv=size-1)
        do_sort = not sorted_flag
        res = binary_search.binary_search_with_optional_sort(ds, target, do_sort=do_sort)
        binary_search.pretty_print_binary_result(res)
        if want_plot:
            binary_search.plot_binary_search_steps(res)
        return

# -------------------------
# Scalability comparison UI (full replacement with CSV, modes and saved PNG)
# -------------------------
def run_scalability_compare_ui():
    print("\n--- Scalability Comparison (quantum/linear/binary) ---")
    max_qubits = choose_int("Max qubits (n) to test (N=2^n)", default=6, minv=1, maxv=12)
    shots = choose_int("Quantum shots", default=512, minv=32)
    repeats = choose_int("Repeats per point (average)", default=10, minv=1)
    include_sort = choose_yesno("Include binary sort cost (unsorted single-query)?", default=True)

    print("\nTarget placement mode (affects classical steps):")
    print("  1) random (shuffle each run)")
    print("  2) start  (place target value at index 0)")
    print("  3) middle (place target value at index N//2)")
    print("  4) end    (place target value at index N-1)")
    tm_choice = choose_int("Choose 1-4", default=1, minv=1, maxv=4)
    if tm_choice == 1:
        target_mode = 'random'
    elif tm_choice == 2:
        target_mode = 'start'
    elif tm_choice == 3:
        target_mode = 'middle'
    else:
        target_mode = 'end'

    Ns = [2 ** n for n in range(1, max_qubits + 1)]
    classical_steps = []
    classical_times = []
    binary_total_times = []
    binary_sort_times = []
    binary_search_times = []
    quantum_iters = []
    quantum_times = []
    quantum_success = []

    rows = []

    print("\nRunning tests (this may take a while for larger qubit counts)...")
    for n in range(1, max_qubits + 1):
        N = 2 ** n

        cs_steps = []
        cs_times = []
        bs_total = []
        bs_sort = []
        bs_search = []

        for _r in range(repeats):
            ds = list(range(N))

            # place the target value according to mode
            if target_mode == 'random':
                random.shuffle(ds)
                target_val = N // 2
            elif target_mode == 'start':
                target_val = 0
                # ensure target_val at index 0
                idx = ds.index(target_val)
                ds[0], ds[idx] = ds[idx], ds[0]
            elif target_mode == 'middle':
                target_val = N // 2
                idx = ds.index(target_val)
                mid_index = N // 2
                ds[mid_index], ds[idx] = ds[idx], ds[mid_index]
            else:  # end
                target_val = N - 1
                idx = ds.index(target_val)
                ds[-1], ds[idx] = ds[idx], ds[-1]

            # classical (use single-run linear_search_once to collect raw times/steps)
            lin = linear_search.linear_search_once(ds, target_val)
            cs_steps.append(lin['steps'])
            cs_times.append(lin['elapsed_py_impl'])

            # binary (with optional sort)
            b = binary_search.binary_search_with_optional_sort(ds.copy(), target_val, do_sort=include_sort)
            bs_total.append(b['elapsed_total'])
            bs_sort.append(b['elapsed_sort'])
            bs_search.append(b['elapsed_search'])

        # aggregated (mean)
        classical_steps.append(float(np.mean(cs_steps)))
        classical_times.append(float(np.mean(cs_times)))
        binary_total_times.append(float(np.mean(bs_total)))
        binary_sort_times.append(float(np.mean(bs_sort)))
        binary_search_times.append(float(np.mean(bs_search)))

        # quantum: run fewer repeats for quantum to save time, but use run_grover_repeated
        try:
            q = quantum_search.run_grover_repeated(target=N//2, n_qubits=n, shots=shots, repeats=max(1, repeats//2))
            quantum_iters.append(float(q['iterations']))
            quantum_times.append(float(q['elapsed_exec_time']))
            quantum_success.append(float(q['success_rate']))
        except Exception as e:
            quantum_iters.append(float('nan'))
            quantum_times.append(float('nan'))
            quantum_success.append(float('nan'))
            print(f"Quantum run failed at n={n}: {e}")

        rows.append({
            'n': n,
            'N': N,
            'classical_steps_mean': classical_steps[-1],
            'classical_time_mean_s': classical_times[-1],
            'binary_total_mean_s': binary_total_times[-1],
            'binary_sort_mean_s': binary_sort_times[-1],
            'binary_search_mean_s': binary_search_times[-1],
            'quantum_iters': quantum_iters[-1],
            'quantum_time_s': quantum_times[-1],
            'quantum_success': quantum_success[-1]
        })

        print(f"n={n} (N={N}) -> classical_steps_mean={classical_steps[-1]:.1f}, binary_total_ms={(binary_total_times[-1]*1000):.3f}, quantum_iters={quantum_iters[-1]}")

    # Save CSV
    csvname = 'results_scalability.csv'
    keys = rows[0].keys()
    with open(csvname, 'w', newline='') as f:
        writer = csv.DictWriter(f, keys)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Saved results to {csvname}")

    # Plot Steps (log-log)
    plt.figure(figsize=(10,6))
    plt.plot(Ns, classical_steps, 'o-', label='Classical steps (mean)')
    if not all(np.isnan(quantum_iters)):
        plt.plot(Ns, quantum_iters, 's-', label='Quantum iterations (measured)')
    plt.plot(Ns, np.log2(Ns), '^-', label='Binary comparisons (theory log2(N))')
    plt.xscale('log'); plt.yscale('log')
    plt.xlabel('Dataset size N (log scale)')
    plt.ylabel('Steps / Iterations (log scale)')
    plt.title('Steps: Classical vs Quantum vs Binary (theory)')
    plt.legend(); plt.grid(alpha=0.3)
    plt.savefig('sc_steps.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("Saved sc_steps.png")

    # Plot Times (log-log)
    plt.figure(figsize=(10,6))
    plt.plot(Ns, np.array(classical_times)*1000, 'o-', label='Classical time (ms)')
    if not all(np.isnan(quantum_times)):
        plt.plot(Ns, np.array(quantum_times)*1000, 's-', label='Quantum time (ms)')
    plt.plot(Ns, np.array(binary_total_times)*1000, '^-', label='Binary total (ms)')
    if any(binary_sort_times):
        plt.plot(Ns, np.array(binary_sort_times)*1000, ':', label='Binary sort time (ms)')
    plt.xscale('log'); plt.yscale('log')
    plt.xlabel('Dataset size N (log scale)')
    plt.ylabel('Time (ms, log scale)')
    plt.title('Wall-clock times: Classical vs Quantum vs Binary')
    plt.legend(); plt.grid(alpha=0.3)
    plt.savefig('sc_times.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("Saved sc_times.png")

# -------------------------
# Main menu
# -------------------------
def main_menu():
    print("\n==== Search Benchmark Suite ====")
    print("1) Run a single algorithm (quick tests, optional plot)")
    print("2) Run scalability comparison (quantum/linear/binary) across sizes and plot")
    print("3) Quit")
    choice = choose_int("Choose 1/2/3", default=2, minv=1, maxv=3)
    if choice == 1:
        run_single_algorithm_ui()
    elif choice == 2:
        run_scalability_compare_ui()
    else:
        print("Exiting.")
        sys.exit(0)

if __name__ == "__main__":
    print("Welcome — Search Benchmark Main (Improved UI)")
    while True:
        main_menu()
        again = choose_yesno("Run again? (y for menu)", default=True)
        if not again:
            print("Goodbye.")
            break
