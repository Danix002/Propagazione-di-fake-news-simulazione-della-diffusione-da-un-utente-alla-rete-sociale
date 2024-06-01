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


def print_iterations_results(iterations):
    # visualize all iteration but merge iteration that have the same status
    #print initial status
    print("INITIAL STATUS AT ITERATION 0 - ", iterations[0]["node_count"])
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
        #add 'node_count' in the print of the iteration
        
        print("Iteration: ", i, "newInfected: ", count_infected, "newRecovered: ", count_recovered, "node count: ", iterations[i]["node_count"])
        """ 
        #if status is the same for the next iteration, merge the iteration in the print of the iteration
        while i < len(iterations) - 1 and iterations[i]["status"] == iterations[i + 1]["status"]:
            i += 1
        #print final status
        if i < len(iterations) - 1:
            print("FINAL STATUS AT ITERATION: Stable stat ", i, " - ", iterations[i]["node_count"])
        else:
            print("FINAL STATUS AT ITERATION: Stable stat ", i, " - ", iterations[i]["node_count"])   
        """
# 1) Creation of a Barabasi-Albert graph with Rank model extension

n = 10000 # Numero totale di nodi
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
c2 = cpm.NodeThreshold(None, triggering_status = "Infected")
model.add_rule("Infected", "Recovered", c2)


#setting threshold for each node
for i in g.nodes():
    config.add_node_configuration("threshold", i, cib.custom_infection_probability(i, g, fake_news_credibility))

model.set_initial_status(config)



# Esecution of the simulation
iterations = cib.custom_iteration_bunch(model, g, 1000, fake_news_credibility)
print_iterations_results(iterations)




# 4) Visualization of the simulation
colors = ["blue"] * len(g.nodes)
for i in range(0, len(iterations)):
    node_statuses = iterations[i]["status"]
    for key in node_statuses.keys():
        if node_statuses[key] == 1:  # State infected
            colors[key] = 'red'
        elif node_statuses[key] == 2: # State recovered
            colors[key] = 'green'
        else: # State suscetible
            colors[key] = 'blue'

# Add the 'color' attribute to the nodes
for node, color in zip(g.nodes(), colors):
    g.nodes[node]['color'] = color


# Show simulation
trends = model.build_trends(iterations)

#viz = DiffusionTrend(model, trends)
#viz.plot()  # Visualizza il grafico con Matplotlib

# Salva la figura
#plt.savefig("diffusion_SIR.png")

nx.write_graphml(g, "Barabasi-Albert-Graph.graphml")

# Debunking (classificazione del punto di partenza)
