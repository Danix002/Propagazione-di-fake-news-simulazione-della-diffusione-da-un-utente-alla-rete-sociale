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
import geopandas as gpd
import artificial_network_generate as ang
import custom_iterations_bunch as cib
from Analysis.debunking_test.debunking_test_functions import make_test_1_debunking, make_test_2_debunking, make_test_3_debunking, make_test_4_debunking, make_test_5_debunking
import Networks.artificial_real_newtworks_creation as atr
    
    

# 1) Creation of a Barabasi-Albert graph with Rank model extension
artificial_network = atr.get_simulation_network(getModel = False)


file_path = 'italy_cities.csv'
cities = gpd.read_file(file_path)



# 3) Simulation of the diffusion process on the graph

fake_news_credibility = 0.7

#-- DEBUNKING TEST 1: setting as initial recovered seed all the hub of the graph, using the degree centrality
iterations_test_one = make_test_1_debunking(artificial_network, 50, fake_news_credibility,  3)

#-- DEBUNKING TEST 2: setting the n nodes with the highes betweennes centrality as initial seed
iterations_test_two = make_test_2_debunking(artificial_network, 50, fake_news_credibility, 3)

#-- DEBUNKING TEST 3: setting a random number of nodes as initial seed
iterations_test_three = make_test_3_debunking(artificial_network, 50, fake_news_credibility, 5)

#-- DEBUNKING TEST 4: setting the n nodes with the highest eigenvector centrality nodes as initial seed
iterations_test_four = make_test_4_debunking(artificial_network, 50, fake_news_credibility, 2)

#-- DEBUNKING TEST 5: setting the n  nodes with the highest closeness centrality nodes as initial seed
iterations_test_five = make_test_5_debunking(artificial_network, 50, fake_news_credibility, 3)

def get_infected_node(index_iteration, test):
    infected_node = []
    if(test == 1):
        for i  in range(0, index_iteration):
            node_statuses = iterations_test_one[i]["status"]
            for key in node_statuses.keys():
                if node_statuses[key] == 1:  # State infected
                    infected_node.append(artificial_network.nodes()[key])
    if(test == 2):
        for i  in range(0, index_iteration):
            node_statuses = iterations_test_two[i]["status"]
            for key in node_statuses.keys():
                if node_statuses[key] == 1:  # State infected
                    infected_node.append(artificial_network.nodes()[key])
    if(test == 3):
        for i  in range(0, index_iteration):
            node_statuses = iterations_test_three[i]["status"]
            for key in node_statuses.keys():
                if node_statuses[key] == 1:  # State infected
                    infected_node.append(artificial_network.nodes()[key])
    if(test == 4):
        for i  in range(0, index_iteration):
            node_statuses = iterations_test_four[i]["status"]
            for key in node_statuses.keys():
                if node_statuses[key] == 1:  # State infected
                    infected_node.append(artificial_network.nodes()[key])
    if(test == 5):
        for i  in range(0, index_iteration):
            node_statuses = iterations_test_five[i]["status"]
            for key in node_statuses.keys():
                if node_statuses[key] == 1:
                    infected_node.append(artificial_network.nodes()[key])
                    
    return infected_node

def get_recovered_node(index_iteration, test):
    recovered_node = []
    if(test == 1):
        for i  in range(0, index_iteration):
            node_statuses = iterations_test_one[i]["status"]
            for key in node_statuses.keys(): # State recovered
                if node_statuses[key] == 2:
                    recovered_node.append(artificial_network.nodes()[key])
    if(test == 2):
        for i  in range(0, index_iteration):
            node_statuses = iterations_test_two[i]["status"]
            for key in node_statuses.keys(): # State recovered
                if node_statuses[key] == 2:
                    recovered_node.append(artificial_network.nodes()[key])
    if(test == 3):
        for i  in range(0, index_iteration):
            node_statuses = iterations_test_three[i]["status"]
            for key in node_statuses.keys(): # State recovered
                if node_statuses[key] == 2:
                    recovered_node.append(artificial_network.nodes()[key])
    if(test == 4):
        for i  in range(0, index_iteration):
            node_statuses = iterations_test_four[i]["status"]
            for key in node_statuses.keys(): # State recovered
                if node_statuses[key] == 2:
                    recovered_node.append(artificial_network.nodes()[key])
    if(test == 5):
        for i  in range(0, index_iteration):
            node_statuses = iterations_test_five[i]["status"]
            for key in node_statuses.keys(): # State recovered
                if node_statuses[key] == 2:
                    recovered_node.append(artificial_network.nodes()[key])
    
    return recovered_node           

def get_susceptible_node(index_iteration, test):
    susceptible_node = []
    if(test == 1):
        for i  in range(0, index_iteration):
            node_statuses = iterations_test_one[i]["status"]
            for key in node_statuses.keys():  # State susceptible
                if node_statuses[key] == 0:
                    susceptible_node.append(artificial_network.nodes()[key])
    if(test == 2):
        for i  in range(0, index_iteration):
            node_statuses = iterations_test_two[i]["status"]
            for key in node_statuses.keys():  # State susceptible
                if node_statuses[key] == 0:
                    susceptible_node.append(artificial_network.nodes()[key])
    if(test == 3):
        for i  in range(0, index_iteration):
            node_statuses = iterations_test_three[i]["status"]
            for key in node_statuses.keys():  # State susceptible
                if node_statuses[key] == 0:
                    susceptible_node.append(artificial_network.nodes()[key])
    if(test == 4):
        for i  in range(0, index_iteration):
            node_statuses = iterations_test_four[i]["status"]
            for key in node_statuses.keys():  # State susceptible
                if node_statuses[key] == 0:
                    susceptible_node.append(artificial_network.nodes()[key])
    if(test == 5):
        for i  in range(0, index_iteration):
            node_statuses = iterations_test_five[i]["status"]
            for key in node_statuses.keys():
                if node_statuses[key] == 0:
                    susceptible_node.append(artificial_network.nodes()[key])
    
    return susceptible_node

def get_number_of_nodes_in_simulation():
    return n

