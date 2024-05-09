import networkx as nx
import matplotlib.pyplot as plt

# Definire i parametri del modello
n = 100  # Numero totale di nodi
m = 2    # Numero di archi da aggiungere ad ogni nuovo nodo

# Generare la rete con il modello di Barabasi-Albert
G = nx.barabasi_albert_graph(n, m)

# Disegnare il grafo
plt.figure(figsize=(10, 6))
nx.draw(G, with_labels=False, node_size=50)
plt.title("Barabasi-Albert Graph")
plt.show()

