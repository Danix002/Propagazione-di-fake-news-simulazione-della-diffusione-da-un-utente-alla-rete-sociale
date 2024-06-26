import numpy as np

def get_instruction_type():
    # Percentuali di persone che usano Twitter per diversi livelli di istruzione
    percent_unknown = 21
    percent_high_school = 13
    percent_university = 24

    # Definizione degli intervalli per le categorie di istruzione
    intervals = {
        "unknown": (0, percent_unknown),
        "high_school": (percent_unknown, percent_unknown + percent_high_school),
        "university": (percent_unknown + percent_high_school, percent_unknown + percent_high_school + percent_university),
        "post_graduate": (percent_unknown + percent_high_school + percent_university, 100)
    }

    # Campiona un valore da intervals
    random_value = np.random.randint(0, 100)
    if random_value < intervals["unknown"][1]:
        return "Unknown"
    
    if intervals["high_school"][0] <= random_value < intervals["high_school"][1]:
        return "high_school"
    
    if intervals["university"][0] <= random_value < intervals["university"][1]:
        return "university"
    
    if intervals["post_graduate"][0] <= random_value < intervals["post_graduate"][1]:
        return "post_graduate"
    


def get_probability_infection_for_instruction(node_instruction):
    peso_diploma = 0.8
    peso_laurea = 0.6
    peso_formazione_dopo_laurea = 0.4
    
    if node_instruction == "high_school":
        x_values = peso_diploma
    elif node_instruction == "university":
        x_values = peso_laurea
    elif node_instruction == "post_graduate":
        x_values = peso_formazione_dopo_laurea
    else:
        # Assegna un valore casuale in caso di input non riconosciuto
        x_values = np.random.choice([peso_diploma, peso_laurea, peso_formazione_dopo_laurea])
        
    probability = 0.5
    
    if x_values == peso_diploma:
        # La probabilità di infezione è tra 0.2 e 0.7
        probability = np.random.uniform(0.2, peso_diploma)

    if x_values == peso_laurea:
        # La probabilità di infezione è tra 0.2 e 0.5
        probability = np.random.uniform(0.2, peso_laurea)
        
    if x_values == peso_formazione_dopo_laurea:
        # La probabilità di infezione è tra 0.2 e 0.4
        probability = np.random.uniform(0.6, peso_formazione_dopo_laurea)
    
    #arrotonda la probabilità a 2 decimali
    probability = round(probability, 2)
    
    return probability

