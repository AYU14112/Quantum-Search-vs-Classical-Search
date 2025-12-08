# quantum_search.py
"""
Quantum search (Grover) module.
Provides `run_grover_once()` and `run_grover_repeated()` functions.
Requires qiskit and qiskit-aer.

Usage:
    from quantum_search import run_grover_once
    res = run_grover_once(target=5, n_qubits=4, shots=1024)
"""

import time
from math import pi, asin
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

def now():
    return time.perf_counter()

def grover_oracle(qc, target, n_qubits):
    target_bin = format(target, f'0{n_qubits}b')
    for i, bit in enumerate(target_bin):
        if bit == '0':
            qc.x(i)
    if n_qubits == 1:
        qc.z(0)
    else:
        qc.h(n_qubits - 1)
        qc.mcx(list(range(n_qubits - 1)), n_qubits - 1)
        qc.h(n_qubits - 1)
    for i, bit in enumerate(target_bin):
        if bit == '0':
            qc.x(i)

def grover_diffusion(qc, n_qubits):
    qc.h(range(n_qubits))
    qc.x(range(n_qubits))
    if n_qubits == 1:
        qc.z(0)
    else:
        qc.h(n_qubits - 1)
        qc.mcx(list(range(n_qubits - 1)), n_qubits - 1)
        qc.h(n_qubits - 1)
    qc.x(range(n_qubits))
    qc.h(range(n_qubits))

def compute_optimal_iterations(n_qubits):
    N = 2 ** n_qubits
    if N <= 1:
        return 1
    theta = asin(1.0 / np.sqrt(N))
    if theta <= 0 or np.isnan(theta):
        return 1
    return max(1, int(round((pi / 4) / theta)))

def build_grover_circuit(target, n_qubits, iterations):
    qc = QuantumCircuit(n_qubits, n_qubits)
    qc.h(range(n_qubits))
    for _ in range(iterations):
        grover_oracle(qc, target, n_qubits)
        grover_diffusion(qc, n_qubits)
    qc.measure(range(n_qubits), range(n_qubits))
    return qc

def run_grover_once(target, n_qubits, shots=1024, transpile_opt=3, warmup=True, use_statevector=False):
    """
    Run a single Grover execution: returns dict:
    {
      'iterations': int,
      'success_rate': float,
      'elapsed_exec_time': float (seconds),
      'counts': dict,
      'transpile_time': float (seconds)
    }
    """
    iterations = compute_optimal_iterations(n_qubits)
    qc = build_grover_circuit(target, n_qubits, iterations)
    simulator = AerSimulator(method='automatic')

    t0 = now()
    qc_transpiled = transpile(qc, simulator, optimization_level=transpile_opt)
    transpile_time = now() - t0

    if warmup:
        try:
            _ = simulator.run(qc_transpiled, shots=min(64, shots)).result()
        except Exception:
            pass

    t0 = now()
    job = simulator.run(qc_transpiled, shots=shots)
    result = job.result()
    elapsed_exec = now() - t0

    counts = result.get_counts()
    target_bin = format(target, f'0{n_qubits}b')
    success = counts.get(target_bin, 0) / shots

    return {
        'iterations': iterations,
        'success_rate': success,
        'elapsed_exec_time': elapsed_exec,
        'counts': counts,
        'transpile_time': transpile_time
    }

def run_grover_repeated(target, n_qubits, shots=1024, repeats=3, **kwargs):
    """
    Run Grover `repeats` times and return aggregated medians.
    """
    records = []
    for _ in range(repeats):
        r = run_grover_once(target, n_qubits, shots=shots, **kwargs)
        records.append(r)
    # aggregate medians for numeric fields
    iterations = int(np.median([r['iterations'] for r in records]))
    success_rate = float(np.median([r['success_rate'] for r in records]))
    elapsed_exec_time = float(np.median([r['elapsed_exec_time'] for r in records]))
    transpile_time = float(np.median([r['transpile_time'] for r in records]))
    counts = records[-1]['counts']  # return last counts (representative)
    return {
        'iterations': iterations,
        'success_rate': success_rate,
        'elapsed_exec_time': elapsed_exec_time,
        'transpile_time': transpile_time,
        'counts': counts
    }

if __name__ == "__main__":
    # quick demo
    print("Quantum search demo (Grover). This will run a small example.")
    res = run_grover_once(target=1, n_qubits=3, shots=1024)
    print("Result:", res)
