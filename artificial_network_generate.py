import networkx as nx
import numpy as np





def rank_model_graph_generate(n, m):
    G = nx.complete_graph(m)
    for new_node in range(m, n):
        degrees = np.array([G.degree(node) for node in G.nodes()])
        ranks = np.argsort(degrees)
        
        rank_probabilities = (ranks + 1) / np.sum(ranks + 1)
        
        existing_nodes = list(G.nodes())
        chosen_nodes = np.random.choice(existing_nodes, m, replace=False, p=rank_probabilities)
        
        for node in chosen_nodes:
            G.add_edge(new_node, node)
            
    return G