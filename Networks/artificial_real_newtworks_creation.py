import networkx as nx
import networkx as nx
import numpy as np
import geopandas as gpd
import random
import sys
import os
import json
from networkx.readwrite import json_graph
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
        #add the neighbors to the nodes set, but when len nodes > num_nodes break
        for node in neighbors:
            nodes.add(node)
            queue.append(node)
            if len(nodes) >= num_nodes:
                break
        
       
        
        
    # Generate the subgraph from the sampled nodes
    sampled_subgraph = G.subgraph(nodes).copy()

    return sampled_subgraph



def random_walk(G, start_node, length):
    walk = [start_node]
    current_node = start_node
    for _ in range(length - 1):
        neighbors = list(G.neighbors(current_node))
        if neighbors:
            current_node = random.choice(neighbors)
            walk.append(current_node)
        else:
            break
    return walk



def _create_real_network():
    new_created = False
    #check if a file graphml file called "real_network_graph" exist in the current folder
    try:
        real_network = nx.read_graphml('Networks/real_network_graph.graphml')
    except:
        new_created = True
        print("Real network not found, creating it from edgelist")
        real_network = _create_graph_from_edgelist('Networks/higgs-retweet_network/higgs-retweet_network.edgelist')       
    
        start_node = random.choice(list(real_network.nodes()))

        real_network = _snowball_sampling(real_network, start_node, 3000)
           
    return real_network, new_created


def _create_artificial_network(number_of_nodes, m=5):
    new_created = False 
    #check if a file graphml file called "artificial_network_graph" exist in the current folder
    try:
        artificial_network = nx.read_graphml('Networks/artificial_network_graph.graphml')  
    except:
        new_created = True  
        print("Artificial network not found, creating it from real network")
        artificial_network = nx.barabasi_albert_graph(number_of_nodes, m) 
    return artificial_network, new_created

def get_simulation_network(getModel = True):
    real_network, real_create = _create_real_network()
    artificial_network, artificial_create = _create_artificial_network(real_network.number_of_nodes(), 30)
    
    real_network, artificial_network = _set_all_nodes_attribute(real_network, artificial_network)

    if(real_create):
        nx.write_graphml(real_network, 'Networks/real_network_graph.graphml')
        data = nx.node_link_data(real_network)
        with open('Networks/real_network_graph.json', 'w') as outfile:
            json.dump(data, outfile)
        
    if(artificial_create):
        nx.write_graphml(artificial_network, 'Networks/artificial_network_graph.graphml') 
        data = nx.node_link_data(artificial_network)
        with open('Networks/artificial_network_graph.json', 'w') as outfile:
            json.dump(data, outfile)
            
    if(getModel):
        return artificial_network
    return real_network