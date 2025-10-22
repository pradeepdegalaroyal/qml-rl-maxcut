"""
Quantum-Inspired RL Optimization for Max-Cut Problem using QAOA
- Solves Max-Cut on a 4-node graph with Qiskit.
- RL-inspired: Iterative parameter optimization mimics policy updates.
- Supports CLI execution and visualization with Matplotlib.
"""
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from qiskit_algorithms import QAOA
from qiskit_algorithms.optimizers import COBYLA
from qiskit.primitives import Sampler
from qiskit.quantum_info import SparsePauliOp

# Define Max-Cut problem (4-node graph)
G = nx.Graph()
G.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 0), (1, 3)])
weights = {(i, j): 1.0 for i, j in G.edges}

# Preprocess adjacency matrix for quantum operator
def create_maxcut_operator(G, weights):
    n = G.number_of_nodes()
    terms = []
    coeffs = []
    for i, j in G.edges:
        w = weights.get((i, j), 1.0)
        pauli_string = ['I'] * n
        pauli_string[i] = 'Z'
        pauli_string[j] = 'Z'
        terms.append(''.join(pauli_string))
        coeffs.append(w / 2)
    return SparsePauliOp.from_list(list(zip(terms, coeffs)))

# Convert integer state to binary array
def state_to_binary(state, num_nodes):
    return [int(x) for x in format(state, f'0{num_nodes}b')]

# Set up QAOA
qaoa = QAOA(optimizer=COBYLA(maxiter=100), reps=2, sampler=Sampler())

# Run QAOA
operator = create_maxcut_operator(G, weights)
result = qaoa.compute_minimum_eigenvalue(operator)
optimal_value = -result.eigenvalue.real
solution = state_to_binary(result.best_measurement['state'], G.number_of_nodes())

# Visualize results
def plot_graph(G, solution):
    colors = ['r' if solution[node] == 0 else 'b' for node in G.nodes]
    pos = nx.spring_layout(G)
    nx.draw(G, pos, node_color=colors, with_labels=True)
    plt.title(f"Max-Cut Solution (Value: {optimal_value:.2f})")
    plt.savefig("maxcut_solution.png")
    plt.close()

print(f"Optimal Cut Value: {optimal_value:.2f}")
print(f"Best Configuration: {solution}")
plot_graph(G, solution)
