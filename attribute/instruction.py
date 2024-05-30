import numpy as np

def sigmoid(x, c=0):
    return 100 / (1 + np.exp(-(x - c)))


# Generazione di valori casuali da una distribuzione gaussiana basata sulle percentuali
def _sample_gaussian_percentages(intervals):
    sampled_value = None
    while sampled_value is None:
        # Campiona un valore da una distribuzione gaussiana standard
        value = np.random.normal(loc=0, scale=1)
        # Normalizza il valore al range [0, 100]
        normalized_value = max(0, min(100, (value + 3) * 16.67))  # Scala il valore alla media 50 e deviazione standard 16.67
        # Verifica in quale intervallo ricade il valore normalizzato
        for interval in intervals:
            if interval[0] <= normalized_value < interval[1]:
                sampled_value = normalized_value
                break
    return sampled_value


def get_instruction_type_gaussian():
    # Percentuali di persone che usano Twitter per diversi livelli di istruzione
    percent_pre_highschool = 21
    percent_high_school = 13
    percent_university = 24
    percent_post_graduate = 32

    # Definizione degli intervalli per le categorie di istruzione
    intervals = {
        "before_highschool": (0, percent_pre_highschool),
        "high_school": (percent_pre_highschool, percent_pre_highschool + percent_high_school),
        "university": (percent_pre_highschool + percent_high_school, percent_pre_highschool + percent_high_school + percent_university),
        "post_graduate": (percent_pre_highschool + percent_high_school + percent_university, 100)
    }

    # Campionamento di un valore basato sulle percentuali
    sampled_value = _sample_gaussian_percentages(intervals)
    return sampled_value

def get_instruction_attribute(node_instruction):
    peso_prima_diploma = 70
    peso_diploma = 50
    peso_laurea = 40
    peso_formazione_dopo_laurea = 30


    if(node_instruction == "PD"):
        x_values = peso_prima_diploma
    
    if(node_instruction == "D"):
        x_values = peso_diploma

    if(node_instruction == "L"):
        x_values = peso_laurea

    if(node_instruction == "PL"):
        x_values = peso_formazione_dopo_laurea

    y_values = sigmoid(x_values, c=90)  # Imposta c vicino a 90 per una pendenza ripida vicino a 100

    # Estrazione casuale di un valore utilizzando la sigmoide traslata
    random_value = np.random.choice(y_values)

    print("Valore estratto casualmente:", random_value)

    return random_value