import numpy as np

#get the probability of infection based on the age of the node, 


def age_probability_infection(age):
    probability = 0.5
    
    if 15 <= age <= 20:
        #probability is between 0.2 and 0.7
        probability = np.random.uniform(0.2, 0.7)
        
    if 20 < age <= 50:
        #probability is between 0.2 and 0.5
        probability = np.random.uniform(0.2, 0.5)
    
    if 51 < age <= 70:
        #probability is between 0.2 and 0.9
        probability = np.random.uniform(0.2, 0.9)
    
    #round the probability to 2 decimal places
    return round(probability, 2)
    
def get_node_age_from_gaussian():
    # Parametri della distribuzione gaussiana
    mu = 32  # Età media
    sigma = 10  # Deviazione standard
    min_age = 15  # Età minima
    max_age = 70  # Età massima

    # Genera valori casuali da una distribuzione gaussiana discreta
    ages = np.round(np.random.normal(mu, sigma, 1000))

    # Limita i valori generati al range [15, 70]
    ages = np.clip(ages, min_age, max_age)

    # Estrai un singolo valore casuale dall'array delle età
    random_age = int(np.random.choice(ages))
    return random_age