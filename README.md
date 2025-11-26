# Quantum Search: Grover's Algorithm vs Classical Search

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Qiskit](https://img.shields.io/badge/Qiskit-Latest-purple)
![License](https://img.shields.io/badge/License-MIT-green)

A comprehensive comparison of classical linear search and Grover's quantum search algorithm, demonstrating the quadratic speedup advantage of quantum computing.

## 🌟 Project Overview

This project implements and compares two fundamental search algorithms:

1. **Classical Linear Search**: O(N) complexity - searches through each element sequentially
2. **Grover's Quantum Search**: O(√N) complexity - uses quantum superposition and amplitude amplification

### Key Features

- ✅ Complete implementation of Grover's algorithm
- ✅ Comprehensive benchmarking suite
- ✅ Enhanced visualizations with highlighted targets
- ✅ Performance comparison across different problem sizes
- ✅ Interactive Jupyter notebook tutorial
- ✅ Detailed circuit analysis and statistics

## 📊 The Quantum Advantage

For a dataset of **N** elements:
- **Classical**: Requires ~N/2 steps on average, N in worst case
- **Quantum**: Requires only ~π√N/4 iterations
- **Speedup**: Quadratic improvement (e.g., 1000 elements → ~32 iterations)

| Dataset Size | Classical Steps | Quantum Steps | Speedup |
|--------------|-----------------|---------------|---------|
| 4            | 4               | 1             | 4.0x    |
| 16           | 16              | 3             | 5.3x    |
| 64           | 64              | 6             | 10.7x   |
| 256          | 256             | 12            | 21.3x   |

## 🚀 Getting Started

### Prerequisites

```bash
Python 3.8 or higher
pip (Python package manager)
```

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/quantum-search.git
cd quantum-search
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install qiskit qiskit-aer matplotlib numpy jupyter
```

### Quick Start

#### Run Classical Search
```bash
python classical_search.py
```

#### Run Quantum Search Simulation
```bash
python quantum_search_sim.py
```

#### Run Comprehensive Benchmark
```bash
python benchmark.py
```

#### Generate Enhanced Visualizations
```bash
python visualize_results.py
```

#### Launch Jupyter Tutorial
```bash
jupyter notebook quantum_search_tutorial.ipynb
```

## 📁 Project Structure

```
quantum-search/
├── Python Codes/
│   ├── classical_search.py          # Linear search implementation
│   ├── quantum_search_sim.py        # Grover's algorithm simulation
│   └── test_plot_clean.py           # Test plotting functionality
├── benchmark.py                      # Comprehensive performance comparison
├── visualize_results.py              # Enhanced visualization suite
├── quantum_search_tutorial.ipynb    # Interactive tutorial
├── requirements.txt                  # Python dependencies
└── README.md                         # This file
```

## 🔬 How Grover's Algorithm Works

### The Algorithm Steps

1. **Initialization**: Create equal superposition of all states
   ```
   |ψ⟩ = (1/√N) Σ|x⟩
   ```

2. **Oracle**: Mark the target state by flipping its phase
   ```
   O|x⟩ = -|x⟩ if x is target, |x⟩ otherwise
   ```

3. **Diffusion**: Amplify the amplitude of the target state
   ```
   D = 2|ψ⟩⟨ψ| - I
   ```

4. **Repeat**: Apply oracle and diffusion ~π√N/4 times

5. **Measure**: Observe the target with high probability

### Geometric Intuition

Grover's algorithm rotates the quantum state in a 2D plane:
- Initial state: uniform superposition (all states equally likely)
- Each iteration: rotates toward the target state
- Optimal iterations: stops when target has maximum amplitude

## 📈 Benchmarking Results

Run the benchmark to see performance across different problem sizes:

```bash
python benchmark.py
```

**Sample Output:**
```
Qubits   Size       Classical    Quantum      Speedup    Success Rate
---------------------------------------------------------------------------
1        2          2            1            2.00       100.0%
2        4          4            1            4.00       100.0%
3        8          8            2            4.00       98.4%
4        16         16           3            5.33       97.9%
5        32         32           5            6.40       96.8%
6        64         64           6            10.67      95.2%
7        128        128          9            14.22      93.8%
8        256        256          12           21.33      92.5%
```

### Generated Visualizations

1. **benchmark_results.png**: 4-panel complexity comparison
   - Steps comparison (linear vs log scale)
   - Speedup factor analysis
   - Success rate tracking

2. **enhanced_distribution.png**: Measurement outcomes with highlighted target

3. **probability_evolution.png**: Target probability across iterations

4. **circuit_statistics.png**: Gate counts and circuit depth

5. **comprehensive_summary.png**: Complete analysis dashboard

## 🎨 Visualization Features

The enhanced visualization suite provides:

- **Highlighted Target States**: Red bars clearly mark the searched element
- **Probability Evolution**: Track amplitude amplification over iterations
- **Circuit Analysis**: Detailed gate statistics and circuit structure
- **Success Rate Tracking**: Monitor algorithm performance
- **Comparison Dashboards**: Side-by-side classical vs quantum

## 📚 Learning Resources

### Jupyter Notebook Tutorial

The included notebook (`quantum_search_tutorial.ipynb`) covers:

1. Introduction to quantum search
2. Mathematical foundations
3. Step-by-step implementation
4. Interactive examples
5. Visualization exercises
6. Challenges and extensions

### Key Concepts Explained

**Superposition**: Quantum states exist in multiple states simultaneously
```python
# Create superposition with Hadamard gates
qc.h(range(n_qubits))
```

**Phase Kickback**: Oracle marks target by phase flip
```python
# Oracle flips phase of target state
grover_oracle(qc, target, n_qubits)
```

**Amplitude Amplification**: Diffusion operator amplifies target amplitude
```python
# Diffusion increases target probability
grover_diffusion(qc, n_qubits)
```

## 🔧 Configuration

### Adjusting Parameters

**In `benchmark.py`:**
```python
max_qubits = 8        # Maximum problem size (2^8 = 256 elements)
shots = 1024          # Number of measurements per run
```

**In `visualize_results.py`:**
```python
n_qubits = 6          # Number of qubits (dataset size = 2^6 = 64)
target = 42           # Element to search for
shots = 2048          # Measurement shots
```

**In `quantum_search_sim.py`:**
```python
n_qubits = 6          # Problem size
target = 5            # Target index
```

## 🧪 Running Tests

Test the plotting functionality:
```bash
python test_plot_clean.py
```

Verify Qiskit installation:
```python
import qiskit
print(qiskit.__version__)
```

## 📊 Performance Considerations

### Classical Search
- **Best case**: O(1) - target is first element
- **Average case**: O(N/2) - target in middle
- **Worst case**: O(N) - target is last element

### Quantum Search
- **Always**: O(√N) iterations
- **Trade-off**: Quantum overhead vs speedup
- **Sweet spot**: Large datasets (N > 100)

### Simulation Limits

- **Up to 10 qubits**: Fast simulation (~1024 elements)
- **11-20 qubits**: Slower, requires more RAM
- **20+ qubits**: Requires high-performance computing

## 🎯 Use Cases

Grover's algorithm is useful for:

1. **Unstructured Search**: No prior ordering information
2. **Database Search**: Finding records in unsorted databases
3. **Cryptography**: Breaking symmetric encryption (theoretical)
4. **Constraint Satisfaction**: Finding solutions to NP problems
5. **Optimization**: Combined with other quantum algorithms

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- [ ] Add noise models for realistic quantum simulation
- [ ] Implement multiple target search
- [ ] Create web-based interactive demo
- [ ] Add more visualization types
- [ ] Optimize for larger qubit counts
- [ ] Add unit tests
- [ ] Implement on real quantum hardware

## 📖 References

1. **Grover's Original Paper**: 
   - Grover, L. K. (1996). "A fast quantum mechanical algorithm for database search"
   - [arXiv:quant-ph/9605043](https://arxiv.org/abs/quant-ph/9605043)

2. **Qiskit Documentation**:
   - [Grover's Algorithm Tutorial](https://qiskit.org/textbook/ch-algorithms/grover.html)
   - [Qiskit API Reference](https://qiskit.org/documentation/)

3. **Nielsen & Chuang**: "Quantum Computation and Quantum Information"
   - Chapter 6: Quantum Search Algorithms

4. **IBM Quantum Learning**:
   - [IBM Quantum Experience](https://quantum-computing.ibm.com/)

## 🛠️ Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'qiskit'`
```bash
pip install qiskit qiskit-aer
```

**Issue**: Matplotlib plots not showing
```bash
# For non-interactive environments
plt.savefig('output.png')  # Instead of plt.show()
```

**Issue**: Out of memory for large circuits
```python
# Reduce problem size
n_qubits = 8  # Instead of 10+
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- IBM Quantum team for Qiskit framework
- Lov Grover for the quantum search algorithm
- Quantum computing community for educational resources

## 📧 Contact

For questions, suggestions, or collaboration:
- **GitHub**: [Your GitHub Profile]
- **Email**: [Your Email]
- **LinkedIn**: [Your LinkedIn]

---

**Happy Quantum Computing! 🚀⚛️**

*"If you think you understand quantum mechanics, you don't understand quantum mechanics." - Richard Feynman*
