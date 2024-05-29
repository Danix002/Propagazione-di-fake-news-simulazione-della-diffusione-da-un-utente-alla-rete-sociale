import networkx as nx
import ndlib.models.ModelConfig as mc
import ndlib.models.epidemics as sir
import random

# Creazione di un grafo
g = nx.erdos_renyi_graph(100, 0.1)

# Assegnazione di una probabilità di infezione casuale a ciascun nodo
for node in g.nodes():
    g.nodes[node]['infection_risk'] = random.uniform(0.01, 0.1)

# Configurazione del modello
model = sir.SIRModel(g)
cfg = mc.Configuration()

# Aggiunta dei parametri del modello
cfg.add_model_parameter('gamma', 0.01)  # Tasso di recupero
cfg.add_model_parameter('beta', 0.0)    # Tasso di infezione globale a 0, lo gestiremo manualmente

# Configurazione dello stato iniziale
cfg.add_model_initial_configuration("Infected", [0])
model.set_initial_status(cfg)

# Funzione per eseguire un'iterazione personalizzata
def custom_iteration(model, graph):
    actual_status = model.status.copy()
    new_status = actual_status.copy()
    
    for node in graph.nodes():
        if actual_status[node] == 1:  # Nodo infetto
            for neighbor in graph.neighbors(node):
                if actual_status[neighbor] == 0:  # Nodo suscettibile
                    infection_risk = graph.nodes[neighbor]['infection_risk']
                    if random.random() < infection_risk:
                        new_status[neighbor] = 1  # Diventa infetto
    
    # Aggiornamento dei nodi recuperati
    for node in graph.nodes():
        if actual_status[node] == 1:
            if random.random() < model.params['model']['gamma']:
                new_status[node] = 2  # Diventa recuperato
    
    model.status = new_status
    return model.status

# Esecuzione della simulazione personalizzata
iterations = []
for i in range(200):
    iteration_status = custom_iteration(model, g)
    iterations.append(iteration_status.copy())

# Stampa dell'output delle iterazioni
for i in range(len(iterations)):
    print(f"Iteration {i}: {iterations[i]}")