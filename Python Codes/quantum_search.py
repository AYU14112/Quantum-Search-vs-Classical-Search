# quantum_search.py
"""
Quantum search (Grover) module - corrected & improved.
Requires qiskit and qiskit-aer for quantum runs. If not installed, the module will raise a helpful error.

Provided functions:
 - run_grover_once(target, n_qubits, shots=1024, transpile_opt=3, warmup=True)
 - run_grover_repeated(target, n_qubits, shots=1024, repeats=3, **kwargs)

Returns dicts for easy printing and plotting.
"""
from math import pi, asin
import numpy as np
import time

try:
    from qiskit import QuantumCircuit, transpile
    from qiskit_aer import AerSimulator
    _HAS_QISKIT = True
except Exception as e:
    _HAS_QISKIT = False
    _QISKIT_ERR = e

def now():
    return time.perf_counter()

def grover_oracle(qc, target, n_qubits):
    tbin = format(target, f'0{n_qubits}b')
    for i, b in enumerate(tbin):
        if b == '0':
            qc.x(i)
    if n_qubits == 1:
        qc.z(0)
    else:
        qc.h(n_qubits - 1)
        qc.mcx(list(range(n_qubits - 1)), n_qubits - 1)
        qc.h(n_qubits - 1)
    for i, b in enumerate(tbin):
        if b == '0':
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

def run_grover_once(target, n_qubits, shots=1024, transpile_opt=3, warmup=True):
    """
    Run Grover's algorithm once and return a dict with:
      - iterations, success_rate, elapsed_exec_time, counts, transpile_time
    Raises informative error if Qiskit/Aer is not installed.
    """
    if not _HAS_QISKIT:
        raise RuntimeError("Qiskit/Aer not found. Install qiskit and qiskit-aer to run quantum simulations. Error:\n" + str(_QISKIT_ERR))

    iterations = compute_optimal_iterations(n_qubits)
    qc = build_grover_circuit(target, n_qubits, iterations)

    # use AerSimulator() with default automatic method (works across Aer versions)
    simulator = AerSimulator()

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
        'success_rate': float(success),
        'elapsed_exec_time': float(elapsed_exec),
        'counts': counts,
        'transpile_time': float(transpile_time)
    }

def run_grover_repeated(target, n_qubits, shots=1024, repeats=3, transpile_opt=3, warmup=True):
    """
    Run the Grover circuit `repeats` times and return median-aggregated results.
    """
    records = []
    for _ in range(repeats):
        rec = run_grover_once(target, n_qubits, shots=shots, transpile_opt=transpile_opt, warmup=warmup)
        records.append(rec)
    iterations = int(np.median([r['iterations'] for r in records]))
    success = float(np.median([r['success_rate'] for r in records]))
    exec_time = float(np.median([r['elapsed_exec_time'] for r in records]))
    transpile_time = float(np.median([r['transpile_time'] for r in records]))
    counts = records[-1]['counts']
    return {
        'iterations': iterations,
        'success_rate': success,
        'elapsed_exec_time': exec_time,
        'counts': counts,
        'transpile_time': transpile_time
    }

if __name__ == "__main__":
    print("Quantum module quick test (requires qiskit + qiskit-aer).")
    try:
        out = run_grover_once(target=1, n_qubits=3, shots=256)
        print(out)
    except Exception as e:
        print("Error:", e)
