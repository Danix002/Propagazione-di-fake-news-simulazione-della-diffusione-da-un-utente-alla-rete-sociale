import matplotlib
# Controlla se l'ambiente ha un display disponibile
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

# Definire i parametri del modello
n = 100 # Numero totale di nodi
m = 10 # Numero di archi da aggiungere ad ogni nuovo nodo

# Generare la rete con il modello di Barabasi-Albert
#G = nx.barabasi_albert_graph(n, m)
#nx.write_graphml(G, "Barabasi-Albert-Graph.graphml")
# Creare un grafo vuoto

# Disegnare il grafo
plt.figure(figsize=(10, 6))

plt.title("Barabasi-Albert Graph")
#plt.show()

# Salvare la figura in un file


# Network Definition
g = nx.erdos_renyi_graph(1000, 0.1)

# Model Selection
model = ep.SIRModel(g)

# Model Configuration
config = mc.Configuration()
config.add_model_parameter('beta', 0.6) # Infection probability S -> I
config.add_model_parameter('gamma', 0.3) # Recovery rate I -> R
config.add_model_parameter("fraction_infected", 0.001) # 4 infected nodes at start in the network.

model.set_initial_status(config)

# Simulation multiple execution
e_n = 4 # Execution number = to number of infection sets
i_n = 10 # Iteration Number - number of days
infection_sets = [(0, 1), (2, 3), (4, 5), (6, 7)]

# Simulation
iterations = model.iteration_bunch(200)
trends = model.build_trends(iterations)
print(model)
# Show simulation
viz = DiffusionTrend(model, trends)
viz.plot("diffusion_SIR.png")

# Estrazione dei dati statistici

#nx.write_graphml(G, "Barabasi-Albert-Graph.graphml")
# Libreria NDLib: simulazione di diffusione di una fakenews utilizzando il modello SIR

# Plotting degli stati e dati statistici

# Debunking (classificazione del punto di partenza)
