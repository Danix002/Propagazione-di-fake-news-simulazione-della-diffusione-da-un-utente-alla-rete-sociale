import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Estrazione dei dati statistici 
# Proprietà strtutturali
def extract_statistic_data(artificial_graph, real_graph):
    plot_graph_comparison(artificial_graph, real_graph)
    plot_degree_distribution(artificial_graph, real_graph)
    plot_centralities(artificial_graph, real_graph)
  

# A function that take two graph as input, calculate number of nodes, number of edges of each graph and plot the comparison in a subplots
def plot_graph_comparison(model_graph, real_graph):
    fig, axs = plt.subplots(3, 2)
    fig.suptitle('Graph Comparison', fontsize=12, fontweight='bold')
    #leayout the subplots
    
  
    plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.7, hspace=0.7)
    
    # Number of nodes, make the bar less wide
    axs[0, 0].bar(['Artificial Network', 'Real Network'], [model_graph.number_of_nodes(), real_graph.number_of_nodes()], color=['blue', 'red'], width=0.6)
    axs[0, 0].set_title('Number of Nodes')
    axs[0, 0].set_ylabel('Number of Nodes')
    
    
    # Number of edges, set the font size
    axs[0, 1].bar(['Artificial Network', 'Real Network'], [model_graph.number_of_edges(), real_graph.number_of_edges()], color=['blue', 'red'], width=0.6)
    axs[0, 1].set_title('Number of Edges')
    axs[0, 1].set_ylabel('Number of Edges')
    
    
    # Average shortest path
    average_shortest_path_model = nx.average_shortest_path_length(model_graph)
    average_shortest_path_real = nx.average_shortest_path_length(real_graph)
    axs[1, 0].bar(['Artificial Network', 'Real Network'], [average_shortest_path_model, average_shortest_path_real], color=['blue', 'red'], width=0.6)
    axs[1, 0].set_title('Average Shortest Path')
    axs[1, 0].set_ylabel('Average Shortest Path')
  
    # Diameter
    diameter_model = nx.diameter(model_graph)
    diameter_real = nx.diameter(real_graph)
    axs[1, 1].bar(['Artificial Network', 'Real Network'], [diameter_model, diameter_real], color=['blue', 'red'], width=0.6)
    axs[1, 1].set_title('Diameter')
    axs[1, 1].set_ylabel('Diameter')
    
    # Connectivty
    connectivity_model = nx.node_connectivity(model_graph)
    connectivity_real = nx.node_connectivity(real_graph)
    axs[2, 0].bar(['Artificial Network', 'Real Network'], [connectivity_model, connectivity_real], color=['blue', 'red'], width=0.6)
    axs[2, 0].set_title('Connectivity')
    axs[2, 0].set_ylabel('Connectivity')
    

    plt.legend()
    plt.show()
    fig.savefig('Analysis/statistic_plot/graph_comparison.png')
    
    
# A function that take two graph as input, calculate the degree of each node and plot degree distribution, the comparison between the two graphs
def plot_degree_distribution(model_graph, real_graph):
    degree_model_net = nx.degree(model_graph)
    degree_real_net = nx.degree(real_graph)
    average_degree_model = sum(dict(degree_model_net).values()) / model_graph.number_of_nodes()
    average_degree_real = sum(dict(degree_real_net).values()) / real_graph.number_of_nodes()
    
    degree_sequence_real = sorted([d for n, d in degree_model_net], reverse=True)  
    degree_sequence_model = sorted([d for n, d in degree_real_net], reverse=True)  
    
    #define a figure
    fig = plt.figure()
    fig.suptitle('Degree Distribution', fontsize=12, fontweight='bold')
    #define a subplot
    ax = fig.add_subplot(111)
    #plot the degree distribution
    ax.plot(degree_sequence_model, 'b-', label='Artificial Network')
    ax.plot(degree_sequence_real, 'r-', label='Real Network')
    ax.set_title('Degree Distribution')
    ax.set_xlabel('Nodes')
    ax.set_ylabel('Degree')
    ax.axhline(y=average_degree_model, color='b', linestyle='--', label='Average Degree Artificial Network')
    ax.axhline(y=average_degree_real, color='r', linestyle='--', label='Average Degree Real Network')
    ax.legend()
    
    plt.show()
    plt.plot()
    fig.savefig('Analysis/statistic_plot/degree_distribution.png')

    
    

# A function that take two graph as input, calculate every centralities and then plot the comparision between the two graphs, generate a subplots
def plot_centralities(model_graph, real_graph):

    # Calculate the centralities
    degree_centrality_model = nx.degree_centrality(model_graph)
    degree_centrality_real = nx.degree_centrality(real_graph)
    
    closeness_centrality_model = nx.closeness_centrality(model_graph)
    closeness_centrality_real = nx.closeness_centrality(real_graph)
    
    betweenness_centrality_model = nx.betweenness_centrality(model_graph)
    betweenness_centrality_real = nx.betweenness_centrality(real_graph)
    
    eigenvector_centrality_model = nx.eigenvector_centrality(model_graph)
    eigenvector_centrality_real = nx.eigenvector_centrality(real_graph)
    
   
    fig, axs = plt.subplots(2, 2)
    #make suptitle with bold and bigger font, color blue
    fig.suptitle('Centralities Comparation between Real and Artificial Network', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    
    # plot degree centrality
    axs[0, 0].plot(degree_centrality_model.values(), label='Artificial Network')
    axs[0, 0].plot(degree_centrality_real.values(), label='Real Network')
    axs[0, 0].set_title('Degree Centrality')
    axs[0, 0].legend()
    
    # plot closeness centrality
    axs[0, 1].plot(closeness_centrality_model.values(), label='Artificial Network')
    axs[0, 1].plot(closeness_centrality_real.values(), label='Real Network')
    axs[0, 1].set_title('Closeness Centrality')
    axs[0, 1].legend()
    
    # plot betweenness centrality
    axs[1, 0].plot(betweenness_centrality_model.values(), label='Artificial Network')
    axs[1, 0].plot(betweenness_centrality_real.values(), label='Real Network')
    axs[1, 0].set_title('Betweenness Centrality')
    axs[1, 0].legend()
    
    # Plot the eigenvector centrality
    axs[1, 1].plot(eigenvector_centrality_model.values(), label='Artificial Network')
    axs[1, 1].plot(eigenvector_centrality_real.values(), label='Real Network')
    axs[1, 1].set_title('Eigenvector Centrality')
    axs[1, 1].legend()
    
    
    
    plt.show()
    fig.savefig('Analysis/statistic_plot/centralities_comparation_real_vs_artificial_net.png')

    
#create two graphs
g1 = nx.barabasi_albert_graph(11, 3)
g2 = nx.barabasi_albert_graph(10, 1)

connectivity = nx.node_connectivity(g1)
diametro = nx.diameter(g1)

print("Connectivity: ", connectivity)
print("Diameter: ", diametro)
plot_graph_comparison(g1, g2)
plot_degree_distribution(g1, g2)
plot_centralities(g1, g2)