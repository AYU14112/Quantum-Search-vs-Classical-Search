# benchmark.py
"""
Comprehensive benchmark comparing classical and quantum search algorithms.
Measures performance, visualizes complexity, and analyzes speedup.
"""

import time
import numpy as np
import matplotlib.pyplot as plt
from math import pi, sqrt, floor
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import sys

# ----------------------------
# Classical Search
# ----------------------------

def classical_search(dataset, target):
    """Performs linear search on a dataset."""
    steps = 0
    start_time = time.time()

    for index, item in enumerate(dataset):
        steps += 1
        if item == target:
            elapsed_time = time.time() - start_time
            return index, steps, elapsed_time

    elapsed_time = time.time() - start_time
    return -1, steps, elapsed_time

# ----------------------------
# Quantum Search (Grover's Algorithm)
# ----------------------------

def grover_oracle(qc, target, n_qubits):
    """Apply oracle that flips the phase of the target state."""
    target_bin = format(target, f'0{n_qubits}b')

    for i, bit in enumerate(target_bin):
        if bit == '0':
            qc.x(i)

    if n_qubits == 1:
        qc.z(0)
    else:
        qc.h(n_qubits-1)
        qc.mcx(list(range(n_qubits-1)), n_qubits-1)
        qc.h(n_qubits-1)

    for i, bit in enumerate(target_bin):
        if bit == '0':
            qc.x(i)

def grover_diffusion(qc, n_qubits):
    """Apply the Grover diffusion operator."""
    qc.h(range(n_qubits))
    qc.x(range(n_qubits))

    if n_qubits == 1:
        qc.z(0)
    else:
        qc.h(n_qubits-1)
        qc.mcx(list(range(n_qubits-1)), n_qubits-1)
        qc.h(n_qubits-1)

    qc.x(range(n_qubits))
    qc.h(range(n_qubits))

def quantum_search(target, n_qubits, shots=1024):
    """Build and execute Grover's algorithm."""
    start_time = time.time()

    qc = QuantumCircuit(n_qubits, n_qubits)
    qc.h(range(n_qubits))

    N = 2 ** n_qubits
    iterations = floor((pi/4) * sqrt(N))

    for _ in range(iterations):
        grover_oracle(qc, target, n_qubits)
        grover_diffusion(qc, n_qubits)

    qc.measure(range(n_qubits), range(n_qubits))

    simulator = AerSimulator()
    qc_transpiled = transpile(qc, simulator)
    result = simulator.run(qc_transpiled, shots=shots).result()
    counts = result.get_counts()

    elapsed_time = time.time() - start_time

    target_bin = format(target, f'0{n_qubits}b')
    success_count = counts.get(target_bin, 0)
    success_rate = success_count / shots

    return iterations, success_rate, elapsed_time, counts

# ----------------------------
# Benchmark Functions
# ----------------------------

def run_single_comparison(n_qubits, target, shots=1024):
    """Run both algorithms and compare results."""
    N = 2 ** n_qubits
    dataset = list(range(N))

    # Classical search
    idx, classical_steps, classical_time = classical_search(dataset, target)

    # Quantum search
    quantum_iters, success_rate, quantum_time, counts = quantum_search(target, n_qubits, shots)

    return {
        'n_qubits': n_qubits,
        'dataset_size': N,
        'target': target,
        'classical_steps': classical_steps,
        'classical_time': classical_time,
        'quantum_iterations': quantum_iters,
        'quantum_success_rate': success_rate,
        'quantum_time': quantum_time,
        'theoretical_speedup': classical_steps / quantum_iters if quantum_iters > 0 else 0,
        'counts': counts
    }

def run_scalability_test(max_qubits=8, shots=1024):
    """Test both algorithms across different problem sizes."""
    results = []

    print("Running scalability tests...\n")
    print(f"{'Qubits':<8} {'Size':<10} {'Classical':<12} {'Quantum':<12} {'Speedup':<10} {'Success Rate':<15}")
    print("-" * 75)

    for n_qubits in range(1, max_qubits + 1):
        N = 2 ** n_qubits
        target = N // 2  # Search for middle element

        result = run_single_comparison(n_qubits, target, shots)
        results.append(result)

        print(f"{n_qubits:<8} {N:<10} {result['classical_steps']:<12} "
              f"{result['quantum_iterations']:<12} "
              f"{result['theoretical_speedup']:<10.2f} "
              f"{result['quantum_success_rate']*100:<14.1f}%")

    return results

# ----------------------------
# Visualization Functions
# ----------------------------

def plot_complexity_comparison(results):
    """Plot complexity: O(N) vs O(√N)"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    dataset_sizes = [r['dataset_size'] for r in results]
    classical_steps = [r['classical_steps'] for r in results]
    quantum_steps = [r['quantum_iterations'] for r in results]
    speedups = [r['theoretical_speedup'] for r in results]
    success_rates = [r['quantum_success_rate'] * 100 for r in results]

    # Plot 1: Steps Comparison
    axes[0, 0].plot(dataset_sizes, classical_steps, 'o-', label='Classical O(N)', linewidth=2, markersize=8)
    axes[0, 0].plot(dataset_sizes, quantum_steps, 's-', label='Quantum O(√N)', linewidth=2, markersize=8)
    axes[0, 0].set_xlabel('Dataset Size (N)', fontsize=12)
    axes[0, 0].set_ylabel('Steps/Iterations', fontsize=12)
    axes[0, 0].set_title('Search Steps: Classical vs Quantum', fontsize=14, fontweight='bold')
    axes[0, 0].legend(fontsize=11)
    axes[0, 0].grid(True, alpha=0.3)

    # Plot 2: Speedup
    axes[0, 1].plot(dataset_sizes, speedups, 'o-', color='green', linewidth=2, markersize=8)
    axes[0, 1].axhline(y=1, color='r', linestyle='--', label='No speedup', alpha=0.5)
    axes[0, 1].set_xlabel('Dataset Size (N)', fontsize=12)
    axes[0, 1].set_ylabel('Speedup Factor', fontsize=12)
    axes[0, 1].set_title('Quantum Speedup vs Dataset Size', fontsize=14, fontweight='bold')
    axes[0, 1].legend(fontsize=11)
    axes[0, 1].grid(True, alpha=0.3)

    # Plot 3: Log-scale comparison
    axes[1, 0].loglog(dataset_sizes, classical_steps, 'o-', label='Classical O(N)', linewidth=2, markersize=8)
    axes[1, 0].loglog(dataset_sizes, quantum_steps, 's-', label='Quantum O(√N)', linewidth=2, markersize=8)
    # Theoretical lines
    x_theory = np.array(dataset_sizes)
    axes[1, 0].loglog(x_theory, x_theory, ':', alpha=0.5, label='Theoretical O(N)')
    axes[1, 0].loglog(x_theory, np.sqrt(x_theory), ':', alpha=0.5, label='Theoretical O(√N)')
    axes[1, 0].set_xlabel('Dataset Size (N)', fontsize=12)
    axes[1, 0].set_ylabel('Steps/Iterations', fontsize=12)
    axes[1, 0].set_title('Log-Log Complexity Analysis', fontsize=14, fontweight='bold')
    axes[1, 0].legend(fontsize=10)
    axes[1, 0].grid(True, alpha=0.3)

    # Plot 4: Success Rate
    axes[1, 1].plot(dataset_sizes, success_rates, 'o-', color='purple', linewidth=2, markersize=8)
    axes[1, 1].axhline(y=100, color='g', linestyle='--', label='Perfect success', alpha=0.5)
    axes[1, 1].set_xlabel('Dataset Size (N)', fontsize=12)
    axes[1, 1].set_ylabel('Success Rate (%)', fontsize=12)
    axes[1, 1].set_title('Quantum Search Success Rate', fontsize=14, fontweight='bold')
    axes[1, 1].set_ylim([0, 105])
    axes[1, 1].legend(fontsize=11)
    axes[1, 1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('benchmark_results.png', dpi=300, bbox_inches='tight')
    print("\n✓ Saved: benchmark_results.png")
    plt.show()

def plot_measurement_distribution(result):
    """Plot measurement outcome distribution with highlighted target."""
    counts = result['counts']
    target = result['target']
    n_qubits = result['n_qubits']
    target_bin = format(target, f'0{n_qubits}b')

    # Sort by state value
    states = sorted(counts.keys())
    values = [counts[s] for s in states]
    colors = ['red' if s == target_bin else 'blue' for s in states]

    plt.figure(figsize=(12, 6))
    bars = plt.bar(range(len(states)), values, color=colors, alpha=0.7, edgecolor='black')

    # Highlight target
    target_idx = states.index(target_bin) if target_bin in states else -1
    if target_idx >= 0:
        bars[target_idx].set_color('red')
        bars[target_idx].set_linewidth(3)

    plt.xlabel('Quantum States', fontsize=12)
    plt.ylabel('Measurement Counts', fontsize=12)
    plt.title(f'Grover Search Results (Target: {target} = |{target_bin}⟩)',
              fontsize=14, fontweight='bold')
    plt.xticks(range(len(states)), states, rotation=45 if len(states) > 8 else 0)

    # Add legend
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor='red', alpha=0.7, label=f'Target: |{target_bin}⟩'),
                      Patch(facecolor='blue', alpha=0.7, label='Other states')]
    plt.legend(handles=legend_elements, fontsize=11)

    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig('measurement_distribution.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: measurement_distribution.png")
    plt.show()

# ----------------------------
# Main Execution
# ----------------------------

if __name__ == "__main__":
    print("=" * 75)
    print("QUANTUM vs CLASSICAL SEARCH BENCHMARK")
    print("=" * 75)

    # Run scalability test
    max_qubits = 8  # Adjust based on your system (higher = longer runtime)
    results = run_scalability_test(max_qubits=max_qubits, shots=1024)

    # Generate visualizations
    print("\n" + "=" * 75)
    print("GENERATING VISUALIZATIONS")
    print("=" * 75)

    plot_complexity_comparison(results)

    # Show detailed results for a specific case
    print("\n" + "=" * 75)
    print("DETAILED ANALYSIS FOR 6-QUBIT EXAMPLE")
    print("=" * 75)

    detailed_result = run_single_comparison(n_qubits=6, target=42, shots=2048)

    print(f"\nDataset Size: {detailed_result['dataset_size']}")
    print(f"Target: {detailed_result['target']}")
    print(f"Classical Steps: {detailed_result['classical_steps']}")
    print(f"Quantum Iterations: {detailed_result['quantum_iterations']}")
    print(f"Theoretical Speedup: {detailed_result['theoretical_speedup']:.2f}x")
    print(f"Quantum Success Rate: {detailed_result['quantum_success_rate']*100:.2f}%")

    plot_measurement_distribution(detailed_result)

    print("\n" + "=" * 75)
    print("BENCHMARK COMPLETE!")
    print("=" * 75)