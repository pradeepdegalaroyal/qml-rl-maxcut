# qaoa_maxcut.py
"""
Quantum-Inspired RL Optimization for Max-Cut Problem using QAOA
- Solves Max-Cut on a 4-node graph with Qiskit.
- RL-inspired: Iterative parameter optimization mimics policy updates.
- Supports CLI execution and visualization with Matplotlib.
"""
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from qiskit import Aer
from qiskit_algorithms import QAOA
from qiskit_algorithms.optimizers import COBYLA
from qiskit.primitives import Sampler

G = nx.Graph()
G.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 0), (1, 3)])
weights = {(i, j): 1.0 for i, j in G.edges}

def create_maxcut_operator(G, weights):
    n = G.number_of_nodes()
    operator = np.zeros((2**n, 2**n))
    for i, j in G.edges:
        w = weights.get((i, j), 1.0)
        for k in range(2**n):
            if (k >> i) & 1 != (k >> j) & 1:
                operator[k, k] += w
    return operator

backend = Aer.get_backend('qasm_simulator')
qaoa = QAOA(optimizer=COBYLA(maxiter=100), reps=2, sampler=Sampler())
operator = create_maxcut_operator(G, weights)
result = qaoa.compute_minimum_eigenvalue(operator)
optimal_value = -result.eigenvalue
optimal_params = result.optimal_parameters

def plot_graph(G, solution):
    colors = ['r' if solution[node] == 0 else 'b' for node in G.nodes]
    pos = nx.spring_layout(G)
    nx.draw(G, pos, node_color=colors, with_labels=True)
    plt.title(f"Max-Cut Solution (Value: {optimal_value:.2f})")
    plt.savefig("maxcut_solution.png")
    plt.show()

solution = result.best_measurement['state']
print(f"Optimal Cut Value: {optimal_value:.2f}")
print(f"Best Configuration: {solution}")
plot_graph(G, solution)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run QAOA for Max-Cut with RL-inspired optimization.")
    parser.add_argument("--nodes", type=int, default=4, help="Number of graph nodes")
    args = parser.parse_args()
    print(f"Running QAOA on {args.nodes}-node graph...")
