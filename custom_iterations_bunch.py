import random
import math

# Funzione per eseguire un'iterazione personalizzata
def _custom_iteration(model, graph, current_iteration):
    actual_status = model.status.copy()
    new_status = actual_status.copy()
    count_new_infected = 0
    dict_new_status = {}
    for node in graph.nodes():
        if actual_status[node] == 1:  # Nodo infetto
            for neighbor in graph.neighbors(node):
                if actual_status[neighbor] == 0:  # Nodo suscettibile
                    infection_risk =  custom_infection_probability(neighbor, graph)
                    if random.random() < infection_risk:
                        new_status[neighbor] = 1  # Diventa infetto
                        dict_new_status[neighbor] = 1
                        count_new_infected = count_new_infected + 1
    model.status = new_status
    current_iteration_results = model.iteration_bunch(1)[0]
    
    #add dict_new status to the current iteration status
    for key in dict_new_status.keys():
        current_iteration_results["status"][key] = dict_new_status[key]
    current_iteration_results["status_delta"][0] = count_new_infected
    return current_iteration_results

def custom_iteration_bunch(model, g, num_iterations): 
    # Esecuzione della simulazione personalizzata
    iterations = []
    for i in range(num_iterations):
        iteration_status = _custom_iteration(model, g, current_iteration=i)
        iterations.append(iteration_status)
    return iterations

# Funzione di probabilità di infezione personalizzata usando una sigmoide
def custom_infection_probability(node, graph):
    # Esempio di calcolo usando una sigmoide degli attributi del nodo
    #attribute = graph.nodes[node]['percentage_of_knowledge']  # Usa uno degli attributi
    #sigmoid = 1 / (1 + math.exp(-attribute))
    return random.uniform(0.01, 0.1)  # Probabilità casuale
