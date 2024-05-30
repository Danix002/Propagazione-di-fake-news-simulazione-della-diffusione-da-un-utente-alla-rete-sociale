import networkx as nx
# Estrazione dei dati statistici 

# Proprietà strtutturali
def extract_statistic_data(g):
    degree = nx.degree(g)
    num_nodes = g.number_of_nodes()
    num_edges = g.number_of_edges()
    average_degree = sum(dict(degree).values()) / num_nodes
    degree = nx.degree(g)
    num_nodes = g.number_of_nodes()
    num_edges = g.number_of_edges()
    average_degree = sum(dict(degree).values()) / num_nodes
    average_shortest_path = nx.average_shortest_path_length(g)
    connectivity = nx.node_connectivity(g)
    diametro = nx.diameter(g)

    # Coefficiente di clustering della rete per capire la chiusura di triangoli
    average_clustering = nx.average_clustering(g)
    # Find all the hubs of the network
    hubs = [node for node in g.nodes() if g.degree(node) > 2]
    # Number of hubs
    num_hubs = len(hubs)

    degree_centrality = nx.degree_centrality(g)
    closeness_centrality = nx.closeness_centrality(g)
    betweenness_centrality = nx.betweenness_centrality(g)
    eigenvector_centrality = nx.eigenvector_centrality(g)
