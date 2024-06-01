import random
import math

# Funzione per eseguire un'iterazione personalizzata
def _custom_iteration(model, graph, fake_news_credibility):
    actual_status = model.status.copy()
    new_status = actual_status.copy()
    count_new_infected = 0
    dict_new_status = {}
    for node in graph.nodes():
        if actual_status[node] == 1:  # Nodo infetto
            for neighbor in graph.neighbors(node):
                if actual_status[neighbor] == 0:  # Nodo suscettibile
                    infection_risk =  custom_infection_probability(neighbor, graph, fake_news_credibility)
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

def custom_iteration_bunch(model, g, num_iterations, fake_news_credibility ): 
    # Esecuzione della simulazione personalizzata
    iterations = []
    for i in range(num_iterations):
        iteration_status = _custom_iteration(model, g, fake_news_credibility)
        iterations.append(iteration_status)
    return iterations

# Funzione di probabilità di infezione calcolata come media tra gli attributi del nodo
def custom_infection_probability(node, graph, fake_news_credibility):
    percentage_of_instruction_probability = graph.nodes[node]['probability_infection_for_instruction']
    age_probability = graph.nodes[node]['probability_infection_for_age']


    #probability depends 30% on the percentage of instruction, 20% on the age  and 50% on the fake news credibility
    #probability = (0.3 * percentage_of_instruction_probability) + (0.3 * age_probability) + (0.4 * fake_news_credibility)
    
    #probability is the mean of the three probabilities
    probability = (percentage_of_instruction_probability + age_probability + fake_news_credibility) / 3
    
    #round the probability to 2 decimal places
    probability = round(probability, 2)
    
    #print("Node: ", node, "Probability: ", probability)
    
    return probability
