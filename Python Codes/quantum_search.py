# quantum_search.py
from math import pi, asin
import time
import numpy as np

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

def compute_iterations(n):
    N = 2 ** n
    theta = asin(1 / np.sqrt(N))
    return max(1, int(round((pi / 4) / theta)))

def grover_oracle(qc, target, n):
    binary = format(target, f'0{n}b')
    for i, b in enumerate(binary):
        if b == '0':
            qc.x(i)
    qc.h(n - 1)
    qc.mcx(list(range(n - 1)), n - 1)
    qc.h(n - 1)
    for i, b in enumerate(binary):
        if b == '0':
            qc.x(i)

def diffusion(qc, n):
    qc.h(range(n))
    qc.x(range(n))
    qc.h(n - 1)
    qc.mcx(list(range(n - 1)), n - 1)
    qc.h(n - 1)
    qc.x(range(n))
    qc.h(range(n))

def run_grover(target_index, n, shots=1024, repeats=3):
    successes = []
    iterations = compute_iterations(n)

    for _ in range(repeats):
        qc = QuantumCircuit(n, n)
        qc.h(range(n))

        for _ in range(iterations):
            grover_oracle(qc, target_index, n)
            diffusion(qc, n)

        qc.measure(range(n), range(n))
        sim = AerSimulator()
        result = sim.run(transpile(qc, sim), shots=shots).result()
        counts = result.get_counts()

        target_bin = format(target_index, f'0{n}b')[::-1]
        successes.append(counts.get(target_bin, 0) / shots)

    return {
        "iterations": iterations,
        "success_rate": sum(successes) / len(successes)
    }

