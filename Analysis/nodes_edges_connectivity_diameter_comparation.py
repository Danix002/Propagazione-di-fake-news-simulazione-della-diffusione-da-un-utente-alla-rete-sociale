import networkx as nx
import matplotlib.pyplot as plt
import json
from networkx.readwrite import json_graph

# A function that takes two graphs as input, calculates number of nodes, number of edges of each graph, and plots the comparison in subplots
def plot_graph_comparison(model_graph, real_graph):
    fig, axs = plt.subplots(3, 2, figsize=(10, 10))
    fig.suptitle('Graph Comparison', fontsize=12, fontweight='bold')
    
    plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.7, hspace=0.7)
    
    # Number of nodes
    axs[0, 0].bar(['Artificial Network', 'Real Network'], [model_graph.number_of_nodes(), real_graph.number_of_nodes()], color=['blue', 'red'], width=0.6)
    axs[0, 0].set_title('Number of Nodes')
    axs[0, 0].set_ylabel('Number of Nodes')
    
    # Number of edges
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
    
    # Connectivity
    connectivity_model = nx.node_connectivity(model_graph)
    connectivity_real = nx.node_connectivity(real_graph)
    axs[2, 0].bar(['Artificial Network', 'Real Network'], [connectivity_model, connectivity_real], color=['blue', 'red'], width=0.6)
    axs[2, 0].set_title('Connectivity')
    axs[2, 0].set_ylabel('Connectivity')
    
    plt.show()
    fig.savefig('graph_comparison.png')

model_net = None
# read a graph from json file
with open('Networks/artificial_network_graph.json') as f:
    data = json.load(f)
    model_net = json_graph.node_link_graph(data)

# read a graph from json file
real_net = None
with open('Networks/real_network_graph.json') as f:
    data = json.load(f)
    real_net = json_graph.node_link_graph(data)
    

plot_graph_comparison(model_net, real_net)