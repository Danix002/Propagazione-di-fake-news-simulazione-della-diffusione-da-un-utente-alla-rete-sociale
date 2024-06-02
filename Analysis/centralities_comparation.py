import networkx as nx
import matplotlib.pyplot as plt



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
    
    
    # Create two graphs
g1 = nx.barabasi_albert_graph(11, 3)
g2 = nx.barabasi_albert_graph(10, 1)

connectivity = nx.node_connectivity(g1)
diameter = nx.diameter(g1)

plot_centralities(g1, g2)
