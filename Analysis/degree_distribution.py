import networkx as nx
import matplotlib.pyplot as plt



# A function that takes two graphs as input, calculates the degree of each node, and plots degree distribution comparison
def plot_degree_distribution(model_graph, real_graph):
    degree_model_net = dict(nx.degree(model_graph))
    degree_real_net = dict(nx.degree(real_graph))
    
    degree_sequence_model = sorted(degree_model_net.values(), reverse=True)
    degree_sequence_real = sorted(degree_real_net.values(), reverse=True)
    
    average_degree_model = sum(degree_sequence_model) / model_graph.number_of_nodes()
    average_degree_real = sum(degree_sequence_real) / real_graph.number_of_nodes()
    
    fig = plt.figure()
    fig.suptitle('Degree Distribution', fontsize=12, fontweight='bold')
    
    ax = fig.add_subplot(111)
    ax.plot(degree_sequence_model, 'b-', label='Artificial Network')
    ax.plot(degree_sequence_real, 'r-', label='Real Network')
    ax.set_title('Degree Distribution')
    ax.set_xlabel('Nodes')
    ax.set_ylabel('Degree')
    ax.axhline(y=average_degree_model, color='b', linestyle='--', label='Average Degree Artificial Network')
    ax.axhline(y=average_degree_real, color='r', linestyle='--', label='Average Degree Real Network')
    ax.legend()
    
    plt.show()
    fig.savefig('degree_distribution.png')
    
    
    
    # Create two graphs
g1 = nx.barabasi_albert_graph(11, 3)
g2 = nx.barabasi_albert_graph(10, 1)

connectivity = nx.node_connectivity(g1)
diameter = nx.diameter(g1)


plot_degree_distribution(g1, g2)

