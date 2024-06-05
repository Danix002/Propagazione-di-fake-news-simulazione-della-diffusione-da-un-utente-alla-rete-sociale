import networkx as nx
import matplotlib.pyplot as plt
import json
from networkx.readwrite import json_graph

# A function that takes two graphs as input, calculates various centralities, and then plots the comparison
def plot_centralities(model_graph = nx.Graph(), real_graph = nx.Graph()):
    
    degree_centrality_model = nx.degree_centrality(model_graph)
    degree_centrality_real = nx.degree_centrality(real_graph)
    
    closeness_centrality_model = nx.closeness_centrality(model_graph)
    closeness_centrality_real = nx.closeness_centrality(real_graph)
    
    betweenness_centrality_model = nx.betweenness_centrality(model_graph)
    betweenness_centrality_real = nx.betweenness_centrality(real_graph)
    
    eigenvector_centrality_model = nx.eigenvector_centrality(model_graph)
    eigenvector_centrality_real = nx.eigenvector_centrality(real_graph)
    
    #write centralities to file.txt divide by model and real
    with open('centralities_model.txt', 'w') as f:
        f.write(str(degree_centrality_model))
        f.write(str(closeness_centrality_model))
        f.write(str(betweenness_centrality_model))
        f.write(str(eigenvector_centrality_model))
    
    with open('centralities_real.txt', 'w') as f:
        f.write(str(degree_centrality_real))
        f.write(str(closeness_centrality_real))
        f.write(str(betweenness_centrality_real))
        f.write(str(eigenvector_centrality_real))
    
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
    

model_net = None
# read a graph from json file
with open('artificial_network_graph.json') as f:
    data = json.load(f)
    model_net = json_graph.node_link_graph(data)

# read a graph from json file
real_net = None
with open('eal_network_graph.json') as f:
    data = json.load(f)
    real_net = json_graph.node_link_graph(data)
    
plot_centralities(model_net, real_net)

    
    



