# main.py
import sys
import random
import math

# ---- Project modules ----
from dataset_loader import load_dataset_from_file, sample_window
from linear_search import linear_search
from binary_search import binary_search
from quantum_search import run_grover
from graphs import plot_steps, plot_success_probability


def main():
    print("\n==== REAL DATASET SEARCH BENCHMARK WITH GRAPHS ====\n")

    # ---------------- Dataset Loading ----------------
    dataset_path = input("Enter dataset file path: ").strip()
    if not dataset_path:
        print("Dataset path is required.")
        sys.exit(1)

    max_lines = input("Max lines to load (press Enter for full file): ").strip()
    max_lines = int(max_lines) if max_lines else None

    try:
        dataset = load_dataset_from_file(dataset_path, max_lines)
    except Exception as e:
        print("Failed to load dataset:", e)
        sys.exit(1)

    if len(dataset) < 2:
        print("Dataset too small for search experiments.")
        sys.exit(1)

    print(f"\nLoaded dataset size: {len(dataset)} records")

    # ---------------- Experiment Settings ----------------
    try:
        min_n = int(input("\nEnter minimum qubits (n_min): "))
        max_n = int(input("Enter maximum qubits (n_max): "))
    except ValueError:
        print("Invalid qubit range.")
        sys.exit(1)

    if min_n < 1 or max_n < min_n:
        print("Invalid qubit values.")
        sys.exit(1)

    shots_input = input("Quantum shots (default 1024): ").strip()
    shots = int(shots_input) if shots_input else 1024

    # ---------------- Result Storage ----------------
    dataset_sizes = []
    linear_steps = []
    binary_steps = []
    quantum_iters = []
    success_rates = []

    # ---------------- Benchmark Loop ----------------
    for n in range(min_n, max_n + 1):
        N = 2 ** n

        if N > len(dataset):
            print(f"\nSkipping N={N} (larger than dataset)")
            continue

        print(f"\nRunning benchmark for N = {N}")

        window = sample_window(dataset, N)
        target_value = random.choice(window)
        target_index = window.index(target_value)

        # Linear Search (value-based)
        lin = linear_search(window, target_value)

        # Binary Search (value-based)
        binr = binary_search(window, target_value)

        # Quantum Search (index-based)
        try:
            q = run_grover(target_index, n, shots=shots)
        except Exception as e:
            print("Quantum execution failed:", e)
            continue

        dataset_sizes.append(N)
        linear_steps.append(lin["steps"])
        binary_steps.append(binr["steps"])
        quantum_iters.append(q["iterations"])
        success_rates.append(q["success_rate"])

        print(f"Linear steps : {lin['steps']}")
        print(f"Binary steps : {binr['steps']}")
        print(f"Grover iters : {q['iterations']}")
        print(f"Success prob : {q['success_rate']*100:.2f}%")

    # ---------------- Graph Generation ----------------
    if dataset_sizes:
        print("\nGenerating graphs for PPT & Viva...")
        plot_steps(dataset_sizes, linear_steps, binary_steps, quantum_iters)
        plot_success_probability(dataset_sizes, success_rates)

        print("\nGraphs saved as:")
        print(" - search_steps_comparison.png")
        print(" - grover_success_probability.png")
    else:
        print("No valid data collected. Graphs not generated.")


if __name__ == "__main__":
    main()
