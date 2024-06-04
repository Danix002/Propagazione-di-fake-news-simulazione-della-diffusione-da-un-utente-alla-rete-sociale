import networkx as nx
import matplotlib.pyplot as plt
import json
from networkx.readwrite import json_graph

# A function that takes two graphs as input, calculates various centralities, and then plots the comparison
def plot_centralities(model_graph, real_graph):
    degree_centrality_model = nx.degree_centrality(model_graph)
    degree_centrality_real = nx.degree_centrality(real_graph)
    
    closeness_centrality_model = nx.closeness_centrality(model_graph)
    closeness_centrality_real = nx.closeness_centrality(real_graph)
    
    betweenness_centrality_model = nx.betweenness_centrality(model_graph)
    betweenness_centrality_real = nx.betweenness_centrality(real_graph)
    
    eigenvector_centrality_model = nx.eigenvector_centrality(model_graph)
    eigenvector_centrality_real = nx.eigenvector_centrality(real_graph)
    
    fig, axs = plt.subplots(2, 2, figsize=(10, 10))
    fig.suptitle('Centralities Comparison between Real and Artificial Network', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    
    # Plot degree centrality
    axs[0, 0].plot(list(degree_centrality_model.values()), label='Artificial Network')
    axs[0, 0].plot(list(degree_centrality_real.values()), label='Real Network')
    axs[0, 0].set_title('Degree Centrality')
    axs[0, 0].legend()
    
    # Plot closeness centrality
    axs[0, 1].plot(list(closeness_centrality_model.values()), label='Artificial Network')
    axs[0, 1].plot(list(closeness_centrality_real.values()), label='Real Network')
    axs[0, 1].set_title('Closeness Centrality')
    axs[0, 1].legend()
    
    # Plot betweenness centrality
    axs[1, 0].plot(list(betweenness_centrality_model.values()), label='Artificial Network')
    axs[1, 0].plot(list(betweenness_centrality_real.values()), label='Real Network')
    axs[1, 0].set_title('Betweenness Centrality')
    axs[1, 0].legend()
    
    # Plot eigenvector centrality
    axs[1, 1].plot(list(eigenvector_centrality_model.values()), label='Artificial Network')
    axs[1, 1].plot(list(eigenvector_centrality_real.values()), label='Real Network')
    axs[1, 1].set_title('Eigenvector Centrality')
    axs[1, 1].legend()
    
    plt.show()
    fig.savefig('centralities_comparison.png')
    
    
# read a graph from json file
with open('real_network.json') as f:
    data = json.load(f)
    model_net = json_graph.node_link_graph(data)
    



