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
    

def choose_network():
    print("Choose the network you want to use for the simulation")
    print("1) Artificial Network")
    print("2) Real Network")
    choice = 0
    while choice != '1' and choice != '2':
        choice = input()
        if choice != '1' and choice != '2':
            print("Invalid choice, please choose between 1 and 2")
        if choice == '1':
            print("You choose the Artificial Network")
            # 1) Creation of a Barabasi-Albert graph with Rank model extension
            artificial_network = atr.get_simulation_network(getModel = True)
            return artificial_network
            
        if choice == '2':
            print("You choose the Real Network")
            # 2) Creation of a real network
            real_network = atr.get_simulation_network(getModel = False)
            return real_network
        
        return nx.Graph()

def choose_simulation_test():
    print("Choose the simulation test you want to run")
    print("1) Test 1: Degree Centrality")
    print("2) Test 2: Betweenness Centrality")
    print("3) Test 3: Random nodes")
    print("4) Test 4: Eigenvector Centrality")
    print("5) Test 5: Closeness Centrality")
    choice = 0
    while choice != '1' and choice != '2' and choice != '3' and choice != '4' and choice != '5':
        choice = input()
        if choice != '1' and choice != '2' and choice != '3' and choice != '4' and choice != '5':
            print("Invalid choice, please choose between 1 and 5")
    
    print("\nYou choose test ", choice, ". Simulation is starting...") 
    return int(choice)

simulated_network = choose_network()
print(simulated_network.number_of_nodes())
test_simulation = choose_simulation_test()

file_path = 'italy_cities.csv'
cities = gpd.read_file(file_path)


# 3) Simulation of the diffusion process on the graph
fake_news_credibility = 0.7

# choose the test specified by the user
if test_simulation == 1:
    #-- DEBUNKING TEST 1: setting as initial recovered seed all the hub of the graph, using the degree centrality
    iterations_test_one = make_test_1_debunking(simulated_network, 50, fake_news_credibility,  120)
if test_simulation == 2:
    #-- DEBUNKING TEST 2: setting the n nodes with the highes betweennes centrality as initial seed
    iterations_test_two = make_test_2_debunking(simulated_network, 50, fake_news_credibility, 120)
if test_simulation == 3:
    #-- DEBUNKING TEST 3: setting a random number of nodes as initial seed
    iterations_test_three = make_test_3_debunking(simulated_network, 50, fake_news_credibility, 120)
if test_simulation == 4:
    try:
        #-- DEBUNKING TEST 4: setting the n nodes with the highest eigenvector centrality nodes as initial seed
        iterations_test_four = make_test_4_debunking(simulated_network, 50, fake_news_credibility, 120)
    except:
        print("Test 4 failed, eigenvector centrality calculation failed")

if test_simulation == 5:
    #-- DEBUNKING TEST 5: setting the n  nodes with the highest closeness centrality nodes as initial seed
    iterations_test_five = make_test_5_debunking(simulated_network, 50, fake_news_credibility, 120)

def get_infected_node(index_iteration, test):
    infected_node = []
    if(test == 1):
        for i  in range(0, index_iteration):
            node_statuses = iterations_test_one[i]["status"]
            for key in node_statuses.keys():
                if node_statuses[key] == 1:  # State infected
                    infected_node.append(simulated_network.nodes()[key])
    if(test == 2):
        for i  in range(0, index_iteration):
            node_statuses = iterations_test_two[i]["status"]
            for key in node_statuses.keys():
                if node_statuses[key] == 1:  # State infected
                    infected_node.append(simulated_network.nodes()[key])
    if(test == 3):
        for i  in range(0, index_iteration):
            node_statuses = iterations_test_three[i]["status"]
            for key in node_statuses.keys():
                if node_statuses[key] == 1:  # State infected
                    infected_node.append(simulated_network.nodes()[key])
    if(test == 4):
        for i  in range(0, index_iteration):
            node_statuses = iterations_test_four[i]["status"]
            for key in node_statuses.keys():
                if node_statuses[key] == 1:  # State infected
                    infected_node.append(simulated_network.nodes()[key])
    if(test == 5):
        for i  in range(0, index_iteration):
            node_statuses = iterations_test_five[i]["status"]
            for key in node_statuses.keys():
                if node_statuses[key] == 1:
                    infected_node.append(simulated_network.nodes()[key])
                    
    return infected_node

def get_recovered_node(index_iteration, test):
    recovered_node = []
    if(test == 1):
        for i  in range(0, index_iteration):
            node_statuses = iterations_test_one[i]["status"]
            for key in node_statuses.keys(): # State recovered
                if node_statuses[key] == 2:
                    recovered_node.append(simulated_network.nodes()[key])
    if(test == 2):
        for i  in range(0, index_iteration):
            node_statuses = iterations_test_two[i]["status"]
            for key in node_statuses.keys(): # State recovered
                if node_statuses[key] == 2:
                    recovered_node.append(simulated_network.nodes()[key])
    if(test == 3):
        for i  in range(0, index_iteration):
            node_statuses = iterations_test_three[i]["status"]
            for key in node_statuses.keys(): # State recovered
                if node_statuses[key] == 2:
                    recovered_node.append(simulated_network.nodes()[key])
    if(test == 4):
        for i  in range(0, index_iteration):
            node_statuses = iterations_test_four[i]["status"]
            for key in node_statuses.keys(): # State recovered
                if node_statuses[key] == 2:
                    recovered_node.append(simulated_network.nodes()[key])
    if(test == 5):
        for i  in range(0, index_iteration):
            node_statuses = iterations_test_five[i]["status"]
            for key in node_statuses.keys(): # State recovered
                if node_statuses[key] == 2:
                    recovered_node.append(simulated_network.nodes()[key])
    
    return recovered_node           

def get_susceptible_node(index_iteration, test):
    susceptible_node = []
    if(test == 1):
        for i  in range(0, index_iteration):
            node_statuses = iterations_test_one[i]["status"]
            for key in node_statuses.keys():  # State susceptible
                if node_statuses[key] == 0:
                    susceptible_node.append(simulated_network.nodes()[key])
    if(test == 2):
        for i  in range(0, index_iteration):
            node_statuses = iterations_test_two[i]["status"]
            for key in node_statuses.keys():  # State susceptible
                if node_statuses[key] == 0:
                    susceptible_node.append(simulated_network.nodes()[key])
    if(test == 3):
        for i  in range(0, index_iteration):
            node_statuses = iterations_test_three[i]["status"]
            for key in node_statuses.keys():  # State susceptible
                if node_statuses[key] == 0:
                    susceptible_node.append(simulated_network.nodes()[key])
    if(test == 4):
        for i  in range(0, index_iteration):
            node_statuses = iterations_test_four[i]["status"]
            for key in node_statuses.keys():  # State susceptible
                if node_statuses[key] == 0:
                    susceptible_node.append(simulated_network.nodes()[key])
    if(test == 5):
        for i  in range(0, index_iteration):
            node_statuses = iterations_test_five[i]["status"]
            for key in node_statuses.keys():
                if node_statuses[key] == 0:
                    susceptible_node.append(simulated_network.nodes()[key])
    
    return susceptible_node


def get_choosed_test():
    return test_simulation