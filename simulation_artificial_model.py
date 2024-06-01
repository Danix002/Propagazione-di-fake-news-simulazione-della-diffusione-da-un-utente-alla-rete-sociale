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
from ndlib.viz.mpl.DiffusionTrend import DiffusionTrend
from ndlib.viz.bokeh.DiffusionPrevalence import DiffusionPrevalence
from ndlib.viz.mpl.TrendComparison import DiffusionTrendComparison
import math
import ndlib.models.ModelConfig as mc
import ndlib.models.epidemics as ep
import ndlib.models.compartments.NodeNumericalAttribute as na
import numpy as np
import custom_iterations_bunch as cib
from bokeh.io import output_notebook, show
from ndlib.viz.bokeh.DiffusionTrend import DiffusionTrend
from bokeh.io import export_png
from bokeh.plotting import output_file, save
import attribute.age as ag
import attribute.instruction as ins
import attribute.spatial_coordinate as sc
import geopandas as gpd
import artificial_network_generate as ang


def print_test_results(name_test, iterations):
    # visualize all iteration but merge iteration that have the same status
    
    print("\n\n<---------TEST: ", name_test, "--------->\n")
    # print initial status
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

# 1) Creation of a Barabasi-Albert graph with Rank model extension
n = 200 # Numero totale di nodi
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

# 3.1) Model definition
fake_news_credibility = 0.7
model = gc.CompositeModel(g)

# Aggiunta degli stati del modello
model.add_status("Susceptible")
model.add_status("Infected")
model.add_status("Recovered")

config = mc.Configuration()
config.add_model_parameter('fraction_infected', 0.02)

# Transition from Susceptible to Infected
c1 = cpm.NodeStochastic(0, triggering_status = "Infected")
model.add_rule("Susceptible", "Infected", c1)

# Transition from Infected to Recovered
c2 = cpm.NodeThreshold(None, triggering_status = "Recovered")
model.add_rule("Infected", "Recovered", c2)

# setting threshold for each node
for i in g.nodes():
    config.add_node_configuration("threshold", i, cib.custom_infection_probability(i, g, fake_news_credibility)-0.1)

# 3.2) Configuration of the simulation

#-- DEBUNKING TEST 1: setting as initial recovered seed all the hub of the graph, using the degree centrality

intial_seed = []

# Get the degree centrality of the nodes
degree_centrality = nx.degree_centrality(g)

# Get the nodes (10%) with the highest degree centrality
num_hub_nodes = math.ceil(n * 0.1)

hub_nodes = sorted(degree_centrality, key=degree_centrality.get, reverse=True)[:num_hub_nodes]

# Add the hub nodes to the initial seed
for node in hub_nodes:
    intial_seed.append(node)
    
config.add_model_initial_configuration("Recovered", intial_seed)
model.set_initial_status(config)

# Esecution of the simulation
iterations = cib.custom_iteration_bunch(model, g, 50, fake_news_credibility)

# 4) Visualization of the simulation results
name_test = "Debunking test 1: setting as initial recovered seed all the hub of the graph"
print_test_results(name_test, iterations)
write_graph_to_file(g, "debunking_test_1_hubs.graphml", iterations)
# Show simulation
trends = model.build_trends(iterations)

#-- DEBUNKING TEST 2: 

#-- DEBUNKING TEST 3: 
#viz = DiffusionTrend(model, trends)
#viz.plot()  # Visualizza il grafico con Matplotlib

# Salva la figura
#plt.savefig("diffusion_SIR.png")


# Debunking (classificazione del punto di partenza)




def get_infected_node():
    infected_node = []
    for i  in range(1, len(iterations)):
        node_statuses = iterations[i]["status"]
        for key in node_statuses.keys():
            if node_statuses[key] == 1:  # State infected
              infected_node.append(g.nodes()[key])
    print(infected_node)
    return infected_node

def get_number_of_nodes_in_simulation():
    return n