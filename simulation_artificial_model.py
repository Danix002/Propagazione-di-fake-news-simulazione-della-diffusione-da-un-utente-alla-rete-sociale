import matplotlib
matplotlib.use('Qt5Agg')
import networkx as nx
import dynetx as dn
import matplotlib.pyplot as plt
from past.builtins import xrange
import ndlib.models.ModelConfig as mc
import ndlib.models.dynamic as dm
import ndlib.models.epidemics as ep
from ndlib.utils import multi_runs
from ndlib.viz.mpl.DiffusionTrend import DiffusionTrend
from ndlib.viz.bokeh.DiffusionPrevalence import DiffusionPrevalence
from ndlib.viz.mpl.TrendComparison import DiffusionTrendComparison
import random
import ndlib.models.CompositeModel as gc
import stochastic_attribute_model as sm
import ndlib.models.compartments as cpm

n = 2000 # Numero totale di nodi
m = 3 # Numero di archi da aggiungere ad ogni nuovo nodo

# Network Definition
g = nx.barabasi_albert_graph(n, m)

# Add node attributes for infection risk
credibility_of_fake_news = 0.4 # Parametro assegnato manualmente in base alla tipologia di fake-news con cui si vuole provare il processo di diffusione e sfatamento 
for node in g.nodes():
    g.nodes[node]['percentage_of_knowledge'] = random.uniform(0.5, 1.5)
    g.nodes[node]['probability_of_fat-checking'] = random.uniform(0.5, 1.5)
    g.nodes[node]['distance_from_the_center_of_diffusion'] = random.uniform(0.5, 1.5)
    g.nodes[node]['age'] = random.uniform(0.5, 1.5)
    g.nodes[node]['probability_of_forgetting'] = random.uniform(0.5, 1.5)
    g.nodes[node]['infection_risk'] = random.uniform(0.5, 1.5)

# Model Selection
model = gc.CompositeModel(g)

# Model statuses
model.add_status("Susceptible")
model.add_status("Infected")
model.add_status("Removed")

c1 = cpm.NodeStochastic(0.02, triggering_status = "Infected")
#c1 = sm.stochastic_attribute_model(0.1, attribute = "infection_risk", triggering_status = "Infected") 
model.add_rule("Susceptible", "Infected", c1)
config = mc.Configuration()
config.add_model_parameter("fraction_infected", 0.2)

# Simulation multiple execution
#e_n = 4 # Execution number = to number of infection sets
#i_n = 10 # Iteration Number - number of days
#infection_sets = [(0, 1), (2, 3), (4, 5), (6, 7)]

model.set_initial_status(config)

# Simulation
iterations = model.iteration_bunch(300)

# Colori dei nodi in base al loro stato
colors = ["blue"] * len(g.nodes)
for i in range(0, len(iterations)):
    node_statuses = iterations[i]['status']
    for key in node_statuses.keys():
        if node_statuses[key] == 1:  # Stato infetto
            colors[key] = 'red'
        else:
            colors[key] = 'blue'

# Add the 'color' attribute to the nodes
for node, color in zip(g.nodes(), colors):
    g.nodes[node]['color'] = color

# Show simulation
#viz = DiffusionTrend(model, trends)
#viz.plot("diffusion_SIR.png")
nx.write_graphml(g, "Barabasi-Albert-Graph.graphml")

# Estrazione dei dati statistici

# Plotting degli stati e dati statistici

# Debunking (classificazione del punto di partenza)
