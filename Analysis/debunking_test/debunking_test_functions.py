import networkx as nx
import dynetx as dn
import matplotlib.pyplot as plt
import math
import custom_iterations_bunch as cib
import random

def print_test_results(name_test, iterations):
    # visualize all iteration but merge iteration that have the same status
    print("\n\n<---------TEST: ", name_test, "--------->\n")
    
    print("\nINITIAL STATUS AT ITERATION 0 - ", iterations[0]["node_count"])
    for i  in range(1, len(iterations)):
        node_statuses = iterations[i]["status"]
        count_susceptible = 0
        count_infected = 0
        count_recovered = 0
        for key in node_statuses.keys():
            if node_statuses[key] == 1:
                count_infected += 1
            elif node_statuses[key] == 2:
                count_recovered += 1
            else:
                count_susceptible += 1
        # add 'node_count' in the print of the iteration
        print("Iteration: ", i, "newInfected: ", count_infected, "newRecovered: ", count_recovered, "node count: ", iterations[i]["node_count"])
        
        # if status is the same of the previous iteration for 5 time, print "Stable status"
        if i > 5:
            if iterations[i]["status"] == iterations[i-1]["status"] == iterations[i-2]["status"] == iterations[i-3]["status"] == iterations[i-4]["status"]:
                print("Stable status - end of the simulation at iteration ",i," of ", len(iterations))
                break
       
def write_graph_to_file(g, file_name, iterations):
    colors = ["blue"] * len(g.nodes)
    for i in range(0, len(iterations)):
        node_statuses = iterations[i]["status"]
        for key in node_statuses.keys():
            if node_statuses[key] == 1:  # State infected
                colors[key] = 'red'
            if node_statuses[key] == 2: # State recovered
                colors[key] = 'green'
                
    # Add the 'color' attribute to the nodes
    for node, color in zip(g.nodes(), colors):
        g.nodes[node]['color'] = color
        
    #write the graph to a file
    nx.write_graphml(g, file_name)


def make_test_1_debunking(g, model, config, num_iterations, fake_news_credibility):
    #-- DEBUNKING TEST 1: setting as initial recovered seed all the hub of the graph, using the degree centrality
    intial_seed = []

    # Get the degree centrality of the nodes
    degree_centrality = nx.degree_centrality(g)

    # Get the nodes (10%) with the highest degree centrality
    num_nodes = g.number_of_nodes()
    num_hub_nodes = math.ceil(num_nodes * 0.1)

    hub_nodes = sorted(degree_centrality, key=degree_centrality.get, reverse=True)
    sorted_hubs = hub_nodes[:num_hub_nodes]

    # Add the hub nodes to the initial seed
    for node in sorted_hubs:
        intial_seed.append(node)

    config.add_model_initial_configuration("Recovered", intial_seed)
    model.set_initial_status(config)

    # Esecution of the simulation
    iterations = cib.custom_iteration_bunch(model, g, num_iterations, fake_news_credibility)

    # Visualization of the simulation results
    name_test = "Debunking test 1: setting as initial recovered seed all the hub of the graph"
    print_test_results(name_test, iterations)
    write_graph_to_file(g, "debunking_test_1_hubs.graphml", iterations)
    
    return iterations

def make_test_2_debunking(g, model, config, num_iterations, fake_news_credibility):
    #-- DEBUNKING TEST 2: setting the 20% with the highest betweennes centrality as initial seed
    intial_seed = []
    betweenness_centrality = nx.betweenness_centrality(g, normalized=True)

    num_nodes = g.number_of_nodes()
    num_bridging_nodes = math.ceil(num_nodes * 0.2)

    sorted_nodes = sorted(betweenness_centrality, key=betweenness_centrality.get, reverse=True)
    bridging_nodes = sorted_nodes[:num_bridging_nodes]

    # Add the hub nodes to the initial seed
    for node in bridging_nodes:
        intial_seed.append(node)

    config.add_model_initial_configuration("Recovered", intial_seed)
    model.set_initial_status(config)

    # Esecution of the simulation
    iterations = cib.custom_iteration_bunch(model, g, num_iterations, fake_news_credibility)

    # Visualization of the simulation results
    name_test = "Debunking test 2: setting as initial recovered seed all the local bridges nodes"
    print_test_results(name_test, iterations)
    write_graph_to_file(g, "debunking_test_2_hubs.graphml", iterations)
    
    return iterations

def make_test_3_debunking(g, model, config, num_iterations, fake_news_credibility):
    #-- DEBUNKING TEST 3: setting a random number of nodes as initial seed
    intial_seed = []
    num_nodes = g.number_of_nodes()
    num_random_nodes = math.ceil(num_nodes * 0.1)
    random_nodes = random.sample(list(g.nodes()), num_random_nodes)

    # Add the hub nodes to the initial seed
    for node in random_nodes:
        intial_seed.append(node)

    config.add_model_initial_configuration("Recovered", intial_seed)
    model.set_initial_status(config)

    # Esecution of the simulation
    iterations = cib.custom_iteration_bunch(model, g, num_iterations, fake_news_credibility)

    # Visualization of the simulation results
    name_test = "Debunking test 3: setting a random number of nodes as initial seed"
    print_test_results(name_test, iterations)
    write_graph_to_file(g, "debunking_test_3_hubs.graphml", iterations)
    
    return iterations
    
    