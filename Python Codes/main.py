# main.py
import sys
import math   # ✅ FIX: missing import added

from dataset_adapters import load_and_find_target
from linear_search import linear_search
from binary_search import binary_search
from quantum_search import run_grover
from graphs import plot_steps, plot_success_probability


def main():
    print("\n==== UNIVERSAL DATASET SEARCH (CLASSICAL vs QUANTUM) ====\n")

    # --------------------------------------------------
    # Dataset + target input
    # --------------------------------------------------
    dataset_path = input("Enter dataset file path: ").strip().strip('"').strip("'")
    if not dataset_path:
        sys.exit("Dataset path is required")

    max_rows = input("Max rows to scan (press Enter for full file): ").strip()
    max_rows = int(max_rows) if max_rows else None

    target = input("\nEnter what you want to find (exact text): ").strip()
    if not target:
        sys.exit("Target cannot be empty")

    try:
        dataset, target_value, target_index = load_and_find_target(
            dataset_path, target, max_rows
        )
    except Exception as e:
        sys.exit(f"\n❌ {e}")

    print(f"\n✅ Target FOUND at dataset index: {target_index}")
    print(f"Total dataset size: {len(dataset)} records")

    # --------------------------------------------------
    # Experiment configuration
    # --------------------------------------------------
    try:
        min_n = int(input("\nEnter minimum qubits (n_min): "))
        max_n = int(input("Enter maximum qubits (n_max): "))
    except ValueError:
        sys.exit("Invalid qubit input")

    shots_input = input("Quantum shots (default 1024): ").strip()
    shots = int(shots_input) if shots_input else 1024

    # --------------------------------------------------
    # Result storage
    # --------------------------------------------------
    dataset_sizes = []
    linear_steps = []
    binary_steps = []
    quantum_iters = []
    success_rates = []

    # --------------------------------------------------
    # Benchmark loop (CORRECT QUANTUM WINDOWING)
    # --------------------------------------------------
    for n in range(min_n, max_n + 1):
        N = 2 ** n

        if N > len(dataset):
            print(f"\nSkipping N={N} (dataset too small)")
            continue

        # ----- Build window that CONTAINS the target -----
        start = max(0, target_index - N // 2)
        end = start + N

        if end > len(dataset):
            end = len(dataset)
            start = end - N

        window = dataset[start:end]
        local_target_index = window.index(target_value)

        print(f"\nRunning benchmark for N = {N}")
        print(f"Target local index in window: {local_target_index}")

        # -------- Classical Linear Search --------
        lin = linear_search(window, target_value)

        # -------- Classical Binary Search --------
        binr = binary_search(window, target_value)

        # -------- Quantum Grover Search --------
        try:
            q = run_grover(local_target_index, n, shots=shots)
        except Exception as e:
            print("Quantum execution failed:", e)
            continue

        # Store results
        dataset_sizes.append(N)
        linear_steps.append(lin["steps"])
        binary_steps.append(binr["steps"])
        quantum_iters.append(q["iterations"])
        success_rates.append(q["success_rate"])

        # Output
        print(f"Linear steps      : {lin['steps']}")
        print(f"Binary steps      : {binr['steps']}")
        print(f"Grover iterations : {q['iterations']}")
        print(f"Success prob      : {q['success_rate']*100:.2f}%")

    # --------------------------------------------------
    # Graph generation
    # --------------------------------------------------
    if not dataset_sizes:
        sys.exit("\nNo valid data collected. Graphs not generated.")

    print("\nGenerating graphs...")
    plot_steps(dataset_sizes, linear_steps, binary_steps, quantum_iters)
    plot_success_probability(dataset_sizes, success_rates)

    print("\nGraphs saved:")
    print(" - search_steps_comparison.png")
    print(" - grover_success_probability.png")
    print("\n==== EXPERIMENT COMPLETED SUCCESSFULLY ====\n")


if __name__ == "__main__":
    main()
