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

def rank_model_graph(n, m):
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

n = 200 # Numero totale di nodi
m = 3 # Numero di archi da aggiungere ad ogni nuovo nodo

# Code for albert barabasi extension, rank model
g = rank_model_graph(n, m)

# Aggiunta di attributi ai nodi
for node in g.nodes():
    g.nodes[node]['instruction'] = ins.get_instruction_type()
    g.nodes[node]['percentage_of_instruction'] = ins.get_instruction_probability(g.nodes[node]['instruction'])
    g.nodes[node]['probability_of_fact-checking'] = random.uniform(0.5, 1.5)
    g.nodes[node]['age'] = ag.get_node_age_from_gaussian()
    g.nodes[node]['probability_of_forgetting'] = random.uniform(0.5, 1.5)
   
# Selezione del modello
model = gc.CompositeModel(g)

# Aggiunta degli stati del modello
model.add_status("Susceptible")
model.add_status("Infected")
model.add_status("Recovered")

config = mc.Configuration()
config.add_model_parameter('fraction_infected', 0.2)


# Definizione delle regole di transizione usando compartimenti
c1 = cpm.NodeStochastic(0, triggering_status = "Infected")
model.add_rule("Susceptible", "Infected", c1)

c2 = cpm.NodeThreshold( 0, triggering_status = "Infected")
model.add_rule("Infected", "Recovered", c2)

# Imposto una probabilità personalizzata per ogni nodo
for i in g.nodes():
    beta = cib.custom_infection_probability(i, g)
    config.add_node_configuration("probability", i, beta)
    config.add_node_configuration("threshold", i, 0.5)

model.set_initial_status(config)

# Esecuzione della simulazione
iterations = cib.custom_iteration_bunch(model, g, 200)
print(iterations)

# Colori dei nodi in base al loro stato
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
print(trends)
#viz = DiffusionTrend(model, trends)
#viz.plot()  # Visualizza il grafico con Matplotlib

# Salva la figura
#plt.savefig("diffusion_SIR.png")

nx.write_graphml(g, "Barabasi-Albert-Graph.graphml")

# Debunking (classificazione del punto di partenza)
