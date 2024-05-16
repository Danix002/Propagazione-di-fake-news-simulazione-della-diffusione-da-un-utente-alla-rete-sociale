# Creazione di una rete sociale simile a twitter attraverso un modello generativo
import networkx as nx
import dynetx as dn
import matplotlib.pyplot as plt
from past.builtins import xrange
#import ndlib.models.ModelConfig as mc
#import ndlib.models.dynamic as dm
#import ndlib.models.epidemics as ep
#from ndlib.utils import multi_runs
#from ndlib.viz.mpl.DiffusionTrend import DiffusionTrend
#from ndlib.viz.mpl.TrendComparison import DiffusionTrendComparison

# Definire i parametri del modello
n = 100000  # Numero totale di nodi
m = 10    # Numero di archi da aggiungere ad ogni nuovo nodo

# Generare la rete con il modello di Barabasi-Albert
G = nx.barabasi_albert_graph(n, m)
nx.write_graphml(G, "Barabasi-Albert-Graph.graphml")

# Disegnare il grafo
plt.figure(figsize=(10, 6))
pos = nx.spring_layout(G)  # Posizionamento dei nodi
nx.draw_networkx(G, pos, with_labels=False, node_size=200, node_color='blue', edge_color='gray', alpha=0.7)
plt.title("Barabasi-Albert Graph")
#plt.show()

# Salvare la figura in un file
#plt.savefig("barabasi_albert_graph.png")
#plt.close()  # Chiude la figura per liberare memoria





# Estrazione dei dati statistici 





# Libreria NDLib: simulazione di diffusione di una fakenews utilizzando il modello SIR





# Plotting degli stati e dati statistici





# Debunking (classificazione del punto di partenza)