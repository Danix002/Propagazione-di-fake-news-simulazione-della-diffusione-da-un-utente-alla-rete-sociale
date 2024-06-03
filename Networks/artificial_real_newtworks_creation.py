import networkx as nx
import networkx as nx
import numpy as np
import geopandas as gpd
import random
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import attribute.age as ag
import attribute.instruction as ins
import attribute.spatial_coordinate as sc

def _set_all_nodes_attribute(real_network, artificial_network):
    file_path = 'italy_cities.csv'
    cities = gpd.read_file(file_path)
   
    for real_node, artificial_node in zip(real_network.nodes(), artificial_network.nodes()):
        instruction_type = ins.get_instruction_type()
        real_network.nodes[real_node]['instruction'] = instruction_type
        artificial_network.nodes[artificial_node]['instruction'] = instruction_type
        instruction_probabilities = ins.get_probability_infection_for_instruction(instruction_type)
        real_network.nodes[real_node]['probability_infection_for_instruction'] = instruction_probabilities
        artificial_network.nodes[artificial_node]['probability_infection_for_instruction'] = instruction_probabilities
        
        node_age = ag.get_node_age_from_gaussian()
        real_network.nodes[real_node]['age'] = node_age
        artificial_network.nodes[artificial_node]['age'] = node_age
        real_network.nodes[real_node]['probability_infection_for_age'] = ag.get_probability_infection_for_age(node_age)
        artificial_network.nodes[artificial_node]['probability_infection_for_age'] = ag.get_probability_infection_for_age(node_age)
        
        city = cities.sample(n=1)
        latitude = sc.get_spatial_coordinate_latitude(city)
        longitude = sc.get_spatial_coordinate_longitude(city)
        real_network.nodes[real_node]['latitude'] = latitude
        real_network.nodes[real_node]['longitude'] = longitude
        artificial_network.nodes[artificial_node]['latitude'] = latitude
        artificial_network.nodes[artificial_node]['longitude'] = longitude  
    return real_network, artificial_network


def _rank_model_graph_generate(n, m):
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


# Function to read edgelist and create graph
def _create_graph_from_edgelist(filename):
    G = nx.Graph()  
    with open(filename, 'r') as file:
        for line in file:     
            node1, node2, weight = line.split()
            G.add_edge(int(node1), int(node2), weight=int(weight))
    return G


def _snowball_sampling(G, start_node, num_nodes):
    nodes = set([start_node])
    queue = [start_node]
    while len(nodes) < num_nodes and queue:
        current = queue.pop(0)
        neighbors = set(G.neighbors(current)) - nodes
        queue.extend(neighbors)
        nodes.update(neighbors)
        
    # Generate the subgraph from the sampled nodes
    sampled_subgraph = G.subgraph(nodes).copy()
    return sampled_subgraph


def _create_real_network():
    #check if a file graphml file called "real_network_graph" exist in the current folder
    try:
        real_network = nx.read_graphml('Network/real_network_graph.graphml')
    except:
        print("Real network not found, creating it from edgelist")
        real_network = _create_graph_from_edgelist('Network/higgs-retweet_network/higgs-retweet_network.edgelist')       
        #create a sampling of 10.000 nodes from the network
        #get node with the highest degree 
        start_node = max(dict(real_network.degree()).items(), key=lambda x: x[1])[0]     
        real_network = _snowball_sampling(real_network, start_node, 10)    
        nx.write_graphml(real_network, 'real_network_graph.graphml')
    return real_network


def _create_artificial_network(number_of_nodes, m=5):
    
    #check if a file graphml file called "artificial_network_graph" exist in the current folder
    try:
        artificial_network = nx.read_graphml('Network/artificial_network_graph.graphml')  
    except:
        print("Artificial network not found, creating it from edgelist")
        artificial_network = _rank_model_graph_generate(number_of_nodes, m)  
        nx.write_graphml(artificial_network, 'Network/artificial_network_graph.graphml')  
    return artificial_network

def get_simulation_network(getModel = True):
    real_network = _create_real_network()
    artificial_network = _create_artificial_network(real_network.number_of_nodes(), 3)
    real_network, artificial_network = _set_all_nodes_attribute(real_network, artificial_network)
 
    if(getModel):
        return artificial_network
    return real_network

get_simulation_network()