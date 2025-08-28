import choix
import networkx as nx
import numpy as np

np.set_printoptions(precision=3, suppress=True)

n_items = 5
data = [
    (1, 0),
    (0, 4),
    (3, 1),
    (0, 2),
    (2, 4),
    (4, 3),
]

graph = nx.DiGraph(incoming_graph_data=data)
nx.draw(graph, with_labels=True)

params = choix.ilsr_pairwise(n_items, data)
print(params)
#
print("ranking (worst to best):", np.argsort(params))
#
# prob_1_wins, prob_4_wins = choix.probabilities([1, 4], params)
# print("Prob(1 wins over 4): {:.2f}".format(prob_1_wins))
#
# n_items = 4
# data = [
#     (3, 2),
#     (2, 1),
#     (1, 0)
# ]
#
# graph = nx.DiGraph(incoming_graph_data=data)
# nx.draw(graph, with_labels=True)
#
# choix.ilsr_pairwise(n_items, data)
#
# choix.ilsr_pairwise(n_items, data, alpha=0.01)
