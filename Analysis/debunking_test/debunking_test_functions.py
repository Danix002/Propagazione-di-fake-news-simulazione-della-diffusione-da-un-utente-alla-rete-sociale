import networkx as nx
import dynetx as dn
import matplotlib.pyplot as plt
import math
import custom_iterations_bunch as cib
import random
import ndlib.models.ModelConfig as mc
from bokeh.io import output_notebook, show
from ndlib.viz.bokeh.DiffusionTrend import DiffusionTrend
from bokeh.io import export_png
from bokeh.plotting import output_file, save
from ndlib.viz.mpl.DiffusionTrend import DiffusionTrend
from ndlib.viz.bokeh.DiffusionPrevalence import DiffusionPrevalence
from ndlib.viz.mpl.TrendComparison import DiffusionTrendComparison
import ndlib.models.ModelConfig as mc
import ndlib.models.CompositeModel as gc
import ndlib.models.compartments as cpm
import json
from networkx.readwrite import json_graph

def print_test_results(name_test, iterations, initial_status_count):
    # visualize all iteration but merge iteration that have the same status
    print("\n\n<---------TEST: ", name_test, "--------->\n")
    
    print("\nINITIAL STATUS ", initial_status_count)
    for i  in range(0, len(iterations)):
        node_delta_variation = [0, 0, 0]
        
        if i > 0:
            node_delta_variation[0] = iterations[i]["node_count"][0] - iterations[i-1]["node_count"][0]
            node_delta_variation[1] = iterations[i]["node_count"][1] - iterations[i-1]["node_count"][1]
            node_delta_variation[2] = iterations[i]["node_count"][2] - iterations[i-1]["node_count"][2]
            
        if i==0:
            node_delta_variation[0] = iterations[i]["node_count"][0] - initial_status_count[0]
            node_delta_variation[1] = iterations[i]["node_count"][1] - initial_status_count[1]
            node_delta_variation[2] = iterations[i]["node_count"][2] - initial_status_count[2]
            
        # add 'node_count' in the print of the iteration with a cute format
        print("Iteration: ", i,"NewSusceptible:", node_delta_variation[0], "NewInfected: ", node_delta_variation[1], "NewRecovered: ", node_delta_variation[2], "node count: ", iterations[i]["node_count"])
        
        
        # if status is the same of the previous iteration for 5 time, print "Stable status"
        if i > 5:
            if iterations[i]["status"] == iterations[i-1]["status"] == iterations[i-2]["status"] == iterations[i-3]["status"] == iterations[i-4]["status"]:
                print("Stable status - end of the simulation at iteration ",i," of ", len(iterations))
                break
    print("\n\n<---------END TEST: ", name_test, "--------->\n")
                 
def write_graph_to_file(g, file_name, iterations = None, only_initial_iteration = False, initial_status = None):
   
    
    if only_initial_iteration:
        count_infected = 0
        count_recovered = 0
        count_susceptible = 0
        for key in initial_status.keys():
                    if initial_status[key] == 1:  # State infected
                        g.nodes[key]['color'] = 'red'
                        count_infected += 1
                        
                    if initial_status[key] == 2: # State recovered
                        g.nodes[key]['color'] = 'green'
                        count_recovered += 1
                    
                    if initial_status[key] == 0:  # State suceptible
                        g.nodes[key]['color'] = 'blue'
                        count_susceptible +=1
                          
        #write the graph to a file
        nx.write_graphml(g, file_name)
        return {0: count_susceptible, 1: count_infected, 2: count_recovered}
                    
    for i in range(0, len(iterations)):
        node_statuses = iterations[i]["status"]
        for key in node_statuses.keys():
            if node_statuses[key] == 1:  # State infected
                g.nodes[key]['color'] = 'red'
            if node_statuses[key] == 2: # State recovered
                g.nodes[key]['color'] = 'green'
            if node_statuses[key] == 0:  # State suceptible
                g.nodes[key]['color'] = 'blue'
    
        
    #write the graph to a file
    nx.write_graphml(g, file_name)

def _build_test_model(g, fake_news_credibility):
    model = gc.CompositeModel(g)

    # Add the statuses of the model
    model.add_status("Susceptible")
    model.add_status("Infected")
    model.add_status("Recovered")

    config = mc.Configuration()
    config.add_model_parameter('fraction_infected', 0.08)

    # Transition from Susceptible to Infected
    c1 = cpm.NodeStochastic(0, triggering_status = "Infected")
    model.add_rule("Susceptible", "Infected", c1)

    # Transition from Infected to Recovered
    c2 = cpm.NodeThreshold(None, triggering_status = "Recovered")
    model.add_rule("Infected", "Recovered", c2)

    # Setting the threshold for each node
    for key in g.nodes().keys():
        custom_infection_probability = cib.custom_infection_probability(key, g, fake_news_credibility)
        if(custom_infection_probability > 0.3):
            config.add_node_configuration("threshold", key, custom_infection_probability-0.2)
        else:
            config.add_node_configuration("threshold", key, 0.1)

    return model, config

def make_test_1_debunking(g, num_iterations, fake_news_credibility, num_hub):
    #-- DEBUNKING TEST 1: setting as initial recovered seed all the hub of the graph, using the degree centrality
    
    model, config = _build_test_model(g, fake_news_credibility)
    intial_seed = []

    # Get the degree centrality of the nodes
    degree_centrality = nx.degree_centrality(g)

    hub_nodes = sorted(degree_centrality, key=degree_centrality.get, reverse=True)
    sorted_hubs = hub_nodes[:num_hub]

    # Add the hub nodes to the initial seed
    for node in sorted_hubs:
        intial_seed.append(node)

    config.add_model_initial_configuration("Recovered", intial_seed)
    model.set_initial_status(config)
    
    initial_status_count = write_graph_to_file(g, "Analysis/debunking_test/test_results/test1/inital_status_infection_and_debunking_test_1_hubs.graphml", only_initial_iteration=True, initial_status = model.status)
    # Esecution of the simulation
    iterations = cib.custom_iteration_bunch(model, g, num_iterations, fake_news_credibility)

    # Visualization of the simulation results
    name_test = "Debunking test 1: setting as initial recovered seed "+ str(num_hub) + " hub of the graph"
    
    data = nx.node_link_data(g)
    with open('Analysis/debunking_test/test_results/test1/inital_status_infection_and_debunking_test_1_hubs.json', 'w') as outfile:
        json.dump(data, outfile)

    print_test_results(name_test, iterations, initial_status_count)
    
    write_graph_to_file(g, "Analysis/debunking_test/test_results/test1/final_status_infection_and_debunking_test_1_hubs.graphml", iterations)
    
    data = nx.node_link_data(g)
    with open('Analysis/debunking_test/test_results/test1/final_status_infection_and_debunking_test_1_hubs.json', 'w') as outfile:
        json.dump(data, outfile)
        
    build_trend_plot(model, iterations, 1)
    return iterations

def make_test_2_debunking(g, num_iterations, fake_news_credibility, num_bridging_nodes):
    #-- DEBUNKING TEST 2: setting the 20% with the highest betweennes centrality as initial seed
    model, config = _build_test_model(g, fake_news_credibility)
    intial_seed = []
    betweenness_centrality = nx.betweenness_centrality(g, normalized=True)

    """
    num_nodes = g.number_of_nodes()
    num_bridging_nodes = math.ceil(num_nodes * 0.1)
    """


    sorted_nodes = sorted(betweenness_centrality, key=betweenness_centrality.get, reverse=True)
    bridging_nodes = sorted_nodes[:num_bridging_nodes]

    # Add the nodes to the initial seed
    for node in bridging_nodes:
        intial_seed.append(node)

    config.add_model_initial_configuration("Recovered", intial_seed)
    model.set_initial_status(config)

    initial_status_count =  write_graph_to_file(g, "Analysis/debunking_test/test_results/test2/inital_status_infection_and_debunking_test_2_hubs.graphml", only_initial_iteration=True, initial_status = model.status)
    
    data = nx.node_link_data(g)
    with open('Analysis/debunking_test/test_results/test2/inital_status_infection_and_debunking_test_2_hubs.json', 'w') as outfile:
        json.dump(data, outfile)
        
    # Esecution of the simulation
    iterations = cib.custom_iteration_bunch(model, g, num_iterations, fake_news_credibility)

    # Visualization of the simulation results
    name_test = "Debunking test 2: setting as initial recovered seed the "+ str(num_bridging_nodes) + " bridges nodes"
    print_test_results(name_test, iterations, initial_status_count)
    
    write_graph_to_file(g, "Analysis/debunking_test/test_results/test2/final_status_infection_and_debunking_test_2_hubs.graphml", iterations)
    
    data = nx.node_link_data(g)
    with open('Analysis/debunking_test/test_results/test2/final_status_infection_and_debunking_test_2_hubs.json', 'w') as outfile:
        json.dump(data, outfile)
        
    build_trend_plot(model, iterations, 2)
    
    return iterations

def make_test_3_debunking(g, num_iterations, fake_news_credibility, num_initial_seed):
    #-- DEBUNKING TEST 3: setting a random number of nodes as initial seed
    model, config = _build_test_model(g, fake_news_credibility)
    intial_seed = []
    
    """
    num_nodes = g.number_of_nodes()
    num_random_nodes = math.ceil(num_nodes * 0.1)
    """
    random_nodes = random.sample(list(g.nodes()), num_initial_seed)

    # Add the nodes to the initial seed
    for node in random_nodes:
        intial_seed.append(node)

    config.add_model_initial_configuration("Recovered", intial_seed)
    model.set_initial_status(config)

    initial_status_count =  write_graph_to_file(g, "Analysis/debunking_test/test_results/test3/inital_status_infection_and_debunking_test_3_hubs.graphml", only_initial_iteration=True, initial_status = model.status)
    
    data = nx.node_link_data(g)
    with open('Analysis/debunking_test/test_results/test3/inital_status_infection_and_debunking_test_3_hubs.json', 'w') as outfile:
        json.dump(data, outfile)
        
    # Esecution of the simulation
    iterations = cib.custom_iteration_bunch(model, g, num_iterations, fake_news_credibility)
    
    # Visualization of the simulation results
    name_test = "Debunking test 3: setting a random number of "+ str(num_initial_seed) + "nodes as initial seed"
    print_test_results(name_test, iterations, initial_status_count)
    
    write_graph_to_file(g, "Analysis/debunking_test/test_results/test3/final_status_infection_and_debunking_test_3_hubs.graphml", iterations)
    
    data = nx.node_link_data(g)
    with open('Analysis/debunking_test/test_results/test3/final_status_infection_and_debunking_test_3_hubs.json', 'w') as outfile:
        json.dump(data, outfile)
        
    build_trend_plot(model, iterations, 3)
    return iterations
    
def make_test_4_debunking(g, num_iterations, fake_news_credibility, num_highest_eigenvector):
    #-- DEBUNKING TEST 4: setting the n  with the highest eigenvector centrality as initial seed
    model, config = _build_test_model(g, fake_news_credibility)
    intial_seed = []
    
    eigenvector_centrality = nx.eigenvector_centrality(g, max_iter=1000)

    sorted_nodes = sorted(eigenvector_centrality, key=eigenvector_centrality.get, reverse=True)
    highest_eigenvector_nodes = sorted_nodes[:num_highest_eigenvector]

    # Add the nodes to the initial seed
    for node in highest_eigenvector_nodes:
        intial_seed.append(node)

    config.add_model_initial_configuration("Recovered", intial_seed)
    model.set_initial_status(config)

    initial_status_count =  write_graph_to_file(g, "Analysis/debunking_test/test_results/test4/inital_status_infection_and_debunking_test_4_hubs.graphml", only_initial_iteration=True, initial_status = model.status)
    
    data = nx.node_link_data(g)
    with open('Analysis/debunking_test/test_results/test4/inital_status_infection_and_debunking_test_4_hubs.json', 'w') as outfile:
        json.dump(data, outfile)
        
    # Esecution of the simulation
    iterations = cib.custom_iteration_bunch(model, g, num_iterations, fake_news_credibility)

    # Visualization of the simulation results
    name_test = "Debunking test 4: setting as initial recovered seed the "+ str(num_highest_eigenvector) + " nodes with the highest eigenvector centrality"
    print_test_results(name_test, iterations, initial_status_count)
    
    write_graph_to_file(g, "Analysis/debunking_test/test_results/test4/final_status_infection_and_debunking_test_4_hubs.graphml", iterations)
    
    data = nx.node_link_data(g)
    with open('Analysis/debunking_test/test_results/test4/final_status_infection_and_debunking_test_4_hubs.json', 'w') as outfile:
        json.dump(data, outfile)
        
    build_trend_plot(model, iterations, 4)
    return iterations

def make_test_5_debunking(g, num_iterations, fake_news_credibility, num_highest_closeness):
    #-- DEBUNKING TEST 5: setting the n  nodes with the highest closeness centrality nodes as initial seed
    model, config = _build_test_model(g, fake_news_credibility)
    intial_seed = []
    
    closeness_centrality = nx.closeness_centrality(g)

    sorted_nodes = sorted(closeness_centrality, key=closeness_centrality.get, reverse=True)
    highest_closeness_nodes = sorted_nodes[:num_highest_closeness]

    # Add the nodes to the initial seed
    for node in highest_closeness_nodes:
        intial_seed.append(node)

    config.add_model_initial_configuration("Recovered", intial_seed)
    model.set_initial_status(config)

    initial_status_count =  write_graph_to_file(g, "Analysis/debunking_test/test_results/test5/inital_status_infection_and_debunking_test_5_hubs.graphml", only_initial_iteration=True, initial_status = model.status)
    
    data = nx.node_link_data(g)
    with open('Analysis/debunking_test/test_results/test5/inital_status_infection_and_debunking_test_5_hubs.json', 'w') as outfile:
        json.dump(data, outfile)
        
    # Esecution of the simulation
    iterations = cib.custom_iteration_bunch(model, g, num_iterations, fake_news_credibility)

    # Visualization of the simulation results
    name_test = "Debunking test 5: setting as initial recovered seed the "+ str(num_highest_closeness) + " nodes with the highest closeness centrality"
    print_test_results(name_test, iterations, initial_status_count)
    
    write_graph_to_file(g, "Analysis/debunking_test/test_results/test5/final_status_infection_and_debunking_test_5_hubs.graphml", iterations)
    
    data = nx.node_link_data(g)
    with open('Analysis/debunking_test/test_results/test5/final_status_infection_and_debunking_test_5_hubs.json', 'w') as outfile:
        json.dump(data, outfile)
        
    build_trend_plot(model, iterations, 5)
    return iterations
    
def build_trend_plot(model, iterations, test):
    trends = model.build_trends(iterations)
    viz = DiffusionTrend(model, trends)
    viz.plot(filename="Analysis/debunking_test/test_results/test"+str(test)+"/trend_plot_test_"+str(test)+".png")
  
  