# quantum_search_sim.py
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from math import pi, sqrt, floor
import matplotlib.pyplot as plt

# ----------------------------
# Helper functions
# ----------------------------

def grover_oracle(qc, target, n_qubits):
    """Apply oracle that flips the phase of the target state."""
    target_bin = format(target, f'0{n_qubits}b')
    
    # Apply X gates to flip qubits for target state
    for i, bit in enumerate(target_bin):
        if bit == '0':
            qc.x(i)
    
    # Apply multi-controlled Z
    if n_qubits == 1:
        qc.z(0)
    else:
        qc.h(n_qubits-1)
        qc.mcx(list(range(n_qubits-1)), n_qubits-1)  # multi-controlled X
        qc.h(n_qubits-1)
    
    # Revert X gates
    for i, bit in enumerate(target_bin):
        if bit == '0':
            qc.x(i)

def grover_diffusion(qc, n_qubits):
    """Apply the Grover diffusion operator."""
    qc.h(range(n_qubits))
    qc.x(range(n_qubits))
    
    # multi-controlled Z
    if n_qubits == 1:
        qc.z(0)
    else:
        qc.h(n_qubits-1)
        qc.mcx(list(range(n_qubits-1)), n_qubits-1)
        qc.h(n_qubits-1)
    
    qc.x(range(n_qubits))
    qc.h(range(n_qubits))

def grover_search(target, n_qubits):
    """Build Grover's algorithm circuit and run simulation."""
    qc = QuantumCircuit(n_qubits, n_qubits)
    
    # Initialize superposition
    qc.h(range(n_qubits))
    
    # Number of iterations
    N = 2 ** n_qubits
    iterations = floor((pi/4) * sqrt(N))
    
    for _ in range(iterations):
        grover_oracle(qc, target, n_qubits)
        grover_diffusion(qc, n_qubits)
    
    # Measurement
    qc.measure(range(n_qubits), range(n_qubits))
    
    # Run simulation
    simulator = AerSimulator()
    qc_transpiled = transpile(qc, simulator)
    result = simulator.run(qc_transpiled).result()
    counts = result.get_counts()
    
    return counts, qc

# ----------------------------
# Main Execution
# ----------------------------
if __name__ == "__main__":
    n_qubits = 6  # Change number of qubits here
    target = 5    # Target value to search for
    
    counts, qc = grover_search(target, n_qubits)
    
    print(f"Target: {target}")
    print("Measurement counts:", counts)
    
    # Draw quantum circuit
    print("\nQuantum Circuit:")
    print(qc.draw(output='text'))
    
    # Plot results
    plt.figure(figsize=(8,5))
    plt.bar(counts.keys(), counts.values())
    plt.xlabel('States')
    plt.ylabel('Counts')
    plt.title('Grover Search Simulation')
    plt.show()
