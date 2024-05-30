import numpy as np

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