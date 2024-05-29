import matplotlib
matplotlib.use('Qt5Agg')
import networkx as nx
import ndlib.models.ModelConfig as mc
import ndlib.models.CompositeModel as gc
import ndlib.models.compartments as cpm
import matplotlib.pyplot as plt
import random
import math
import ndlib.models.ModelConfig as mc
import ndlib.models.epidemics as ep
import ndlib.models.compartments.NodeNumericalAttribute as na
import numpy as np


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

# Funzione di probabilità di infezione personalizzata usando una sigmoide
def custom_infection_probability(node, graph):
    # Esempio di calcolo usando una sigmoide degli attributi del nodo
    attribute = graph.nodes[node]['percentage_of_knowledge']  # Usa uno degli attributi
    sigmoid = 1 / (1 + math.exp(-attribute))
    return sigmoid

n = 2000 # Numero totale di nodi
m = 3 # Numero di archi da aggiungere ad ogni nuovo nodo

# code for albert barabasi extension, rank model
g = rank_model_graph(n, m)

# Estrazione dei dati statistici 
"""
# Proprietà strtutturali
degree = nx.degree(g)
num_nodes = g.number_of_nodes()
num_edges = g.number_of_edges()
average_degree = sum(dict(degree).values()) / num_nodes
degree = nx.degree(g)
num_nodes = g.number_of_nodes()
num_edges = g.number_of_edges()
average_degree = sum(dict(degree).values()) / num_nodes
average_shortest_path = nx.average_shortest_path_length(g)
connectivity = nx.node_connectivity(g)
diametro = nx.diameter(g)

# Coefficiente di clustering della rete per capire la chiusura di triangoli
average_clustering = nx.average_clustering(g)
# Find all the hubs of the network
hubs = [node for node in g.nodes() if g.degree(node) > 2]
# Number of hubs
num_hubs = len(hubs)

degree_centrality = nx.degree_centrality(g)
closeness_centrality = nx.closeness_centrality(g)
betweenness_centrality = nx.betweenness_centrality(g)
eigenvector_centrality = nx.eigenvector_centrality(g)
"""


# Plotting degli stati e dati statistici

# Aggiunta di attributi ai nodi
for node in g.nodes():
    g.nodes[node]['percentage_of_knowledge'] = random.uniform(0.5, 1.5)
    g.nodes[node]['probability_of_fact-checking'] = random.uniform(0.5, 1.5)
    g.nodes[node]['distance_from_the_center_of_diffusion'] = random.uniform(0.5, 1.5)
    g.nodes[node]['age'] = random.uniform(0.5, 1.5)
    #g.nodes[node]['probability_of_forgetting'] = random.uniform(0.5, 1.5)
   
# Selezione del modello
model = gc.CompositeModel(g)

# Aggiunta degli stati del modello
model.add_status("Susceptible")
model.add_status("Infected")
model.add_status("Recovered")

config = mc.Configuration()
config.add_model_parameter('fraction_infected', 0.2)

# Definizione delle regole di transizione usando compartimenti
c1 = cpm.NodeStochastic(0.0, triggering_status = "Infected")
model.add_rule("Susceptible", "Infected", c1)

c2 = cpm.NodeThreshold(0.0, triggering_status = "Recovered")
model.add_rule("Infected", "Recovered", c2)

# Imposto una probabilità personalizzata per ogni nodo
for i in g.nodes():
    beta = custom_infection_probability(i, g)
    config.add_node_configuration("probability", i, beta)
    config.add_node_configuration("threshold", i, 0.0)

model.set_initial_status(config)

# Esecuzione della simulazione
iterations = model.iteration_bunch(20)
print(iterations)

# Colori dei nodi in base al loro stato
colors = ["blue"] * len(g.nodes)
for i in range(0, len(iterations)):
    node_statuses = iterations[i]['status']
    for key in node_statuses.keys():
        if node_statuses[key] == 1:  # Stato infetto
            colors[key] = 'red'
        elif node_statuses[key] == 2:
            colors[key] = 'green'
        else:
            colors[key] = 'blue'

# Add the 'color' attribute to the nodes
for node, color in zip(g.nodes(), colors):
    g.nodes[node]['color'] = color



# Show simulation
#viz = DiffusionTrend(model, trends)
#viz.plot("diffusion_SIR.png")
nx.write_graphml(g, "Barabasi-Albert-Graph.graphml")



# Debunking (classificazione del punto di partenza)
