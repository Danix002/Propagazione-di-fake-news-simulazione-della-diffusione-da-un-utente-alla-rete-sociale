import matplotlib
matplotlib.use('Qt5Agg')
import networkx as nx
import ndlib.models.ModelConfig as mc
import ndlib.models.CompositeModel as gc
import ndlib.models.compartments as cpm
import matplotlib.pyplot as plt
import random
import dynetx as dn
import matplotlib.pyplot as plt
from ndlib.utils import multi_runs
import math
import ndlib.models.ModelConfig as mc
import ndlib.models.epidemics as ep
import ndlib.models.compartments.NodeNumericalAttribute as na
import numpy as np
import custom_iterations_bunch as cib
import attribute.age as ag
import attribute.instruction as ins
import attribute.spatial_coordinate as sc
import geopandas as gpd
import artificial_network_generate as ang
import custom_iterations_bunch as cib
from Analysis.debunking_test.debunking_test_functions import make_test_1_debunking, make_test_2_debunking, make_test_3_debunking

    
# 1) Creation of a Barabasi-Albert graph with Rank model extension
n = 2000 # Numero totale di nodi
m = 3 # Numero di archi da aggiungere ad ogni nuovo nodo

# 1.1) Add all the attributes to the nodes
g = ang.rank_model_graph_generate(n, m)
file_path = 'italy_cities.csv'
cities = gpd.read_file(file_path)

for node in g.nodes():
    g.nodes[node]['instruction'] = ins.get_instruction_type()
    g.nodes[node]['probability_infection_for_instruction'] = ins.get_probability_infection_for_instruction(g.nodes[node]['instruction'])
    g.nodes[node]['age'] = ag.get_node_age_from_gaussian()
    g.nodes[node]['probability_infection_for_age'] = ag.get_probability_infection_for_age(g.nodes[node]['age'])
    city = cities.sample(n=1)
    g.nodes[node]['latitude'] = sc.get_spatial_coordinate_latitude(city)
    g.nodes[node]['longitude']  = sc.get_spatial_coordinate_longitude(city)
   
# 2) Getting all necessary statistics of the graph

# 3) Simulation of the diffusion process on the graph

fake_news_credibility = 0.7

#-- DEBUNKING TEST 1: setting as initial recovered seed all the hub of the graph, using the degree centrality
iterations_test_one = make_test_1_debunking(g, 50, fake_news_credibility,  150)

#-- DEBUNKING TEST 2: setting the 20% with the highes betweennes centrality as initial seed
iterations_test_two = make_test_2_debunking(g, 50, fake_news_credibility, 150)

#-- DEBUNKING TEST 3: setting a random number of nodes as initial seed
iterations_test_three = make_test_3_debunking(g, 50, fake_news_credibility, 150)


def get_infected_node():
    infected_node = []
    for i  in range(1, len(iterations_test_one)):
        node_statuses = iterations_test_one[i]["status"]
        for key in node_statuses.keys():
            if node_statuses[key] == 1:  # State infected
              infected_node.append(g.nodes()[key])
    return infected_node

def get_recovered_node():
    recovered_node = []
    for i  in range(1, len(iterations_test_one)):
        node_statuses = iterations_test_one[i]["status"]
        for key in node_statuses.keys(): # State recovered
            if node_statuses[key] == 2:
                recovered_node.append(g.nodes()[key])
    return recovered_node

def get_susceptible_node():
    susceptible_node = []
    
    for i  in range(1, len(iterations_test_one)):
        node_statuses = iterations_test_one[i]["status"]
        for key in node_statuses.keys():  # State recovered
            if node_statuses[key] == 0:
                susceptible_node.append(g.nodes()[key])
    return susceptible_node

def get_number_of_nodes_in_simulation():
    return n