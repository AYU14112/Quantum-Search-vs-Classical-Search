# graphs.py
import matplotlib.pyplot as plt

def plot_steps(dataset_sizes, linear_steps, binary_steps, quantum_iters):
    plt.figure(figsize=(10,6))

    plt.plot(dataset_sizes, linear_steps, 'o-', label="Linear Search (comparisons)")
    plt.plot(dataset_sizes, binary_steps, 's-', label="Binary Search (comparisons)")
    plt.plot(dataset_sizes, quantum_iters, '^-', label="Grover (iterations)")

    plt.xscale("log", base=2)
    plt.yscale("log")

    plt.xlabel("Dataset Size (N = 2^n)")
    plt.ylabel("Steps / Iterations (log scale)")
    plt.title("Search Complexity Comparison")
    plt.legend()
    plt.grid(True, which="both", linestyle="--", alpha=0.6)

    plt.savefig("search_steps_comparison.png", dpi=300, bbox_inches="tight")
    plt.show()


def plot_success_probability(dataset_sizes, success_rates):
    plt.figure(figsize=(10,6))

    plt.plot(dataset_sizes, success_rates, 'o-', color="green")

    plt.xscale("log", base=2)
    plt.xlabel("Dataset Size (N = 2^n)")
    plt.ylabel("Success Probability")
    plt.title("Grover Search Success Probability")
    plt.grid(True, linestyle="--", alpha=0.6)

    plt.savefig("grover_success_probability.png", dpi=300, bbox_inches="tight")
    plt.show()
