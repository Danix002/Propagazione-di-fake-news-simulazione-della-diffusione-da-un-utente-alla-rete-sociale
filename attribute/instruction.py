import numpy as np

def sigmoid(x, c=0):
    return 100 / (1 + np.exp(-(x - c)))

def _sample_gaussian_percentages(intervals):
    sampled_value = None
    while sampled_value is None:
        # Campiona un valore da una distribuzione gaussiana standard
        value = np.random.normal(loc=0, scale=1)
        # Normalizza il valore al range [0, 100] basato sulle percentuali
        normalized_value = max(0, min(100, value * 100))
        # Verifica in quale intervallo ricade il valore normalizzato
        for interval_name, interval_range in intervals.items():
            if interval_range[0] <= normalized_value < interval_range[1]:
                sampled_value = interval_name
                break
    return sampled_value

def get_instruction_type_gaussian():
    # Percentuali di persone che usano Twitter per diversi livelli di istruzione
    percent_unknown = 21
    percent_high_school = 13
    percent_university = 24
    #percent_post_graduate = 32

    # Definizione degli intervalli per le categorie di istruzione
    intervals = {
        "unknown": (0, percent_unknown),
        "high_school": (percent_unknown, percent_unknown + percent_high_school),
        "university": (percent_unknown + percent_high_school, percent_unknown + percent_high_school + percent_university),
        "post_graduate": (percent_unknown + percent_high_school + percent_university, 100)
    }

    # Campionamento di un valore basato sulle percentuali
    sampled_value = _sample_gaussian_percentages(intervals)
    return sampled_value

def get_instruction_attribute(node_instruction):
    peso_diploma = 50
    peso_laurea = 40
    peso_formazione_dopo_laurea = 30
    peso_unknown = np.random.choice(["peso_diploma", "peso_laurea", "peso_formazione_dopo_laurea"], p=[50, 40, 30])

    if(node_instruction == "unknown"):
        x_values = peso_unknown
    
    if(node_instruction == "high_school"):
        x_values = peso_diploma

    if(node_instruction == "university"):
        x_values = peso_laurea

    if(node_instruction == "post_graduate"):
        x_values = peso_formazione_dopo_laurea

    y_values = sigmoid(x_values, c=90)  # Imposta c vicino a 90 per una pendenza ripida vicino a 100

    # Estrazione casuale di un valore utilizzando la sigmoide traslata
    random_value = np.random.choice(y_values)

    print("Valore estratto casualmente:", random_value)

    return random_value