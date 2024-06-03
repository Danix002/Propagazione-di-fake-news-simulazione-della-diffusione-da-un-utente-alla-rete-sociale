import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'Visualization')))
import Visualization.choroplet_complete_multiple_view as ccmv

iteration = input("Inserisci il numero d'iterazione che vuoi visualizzare (il numero massimo di iterazioni per test lo trovi nella riga 'Stable status' del relativo test): ")
cities_flag = input("Vuoi visualizzare anche le città (scrivi 'Si' se vuoi visualizzarle, 'No' altrimenti): ")
choose_test = input("Ci siamo quasi, come ultima cosa scegli il test che vuoi visualizzare: ")

if (int(choose_test) in range(1, 6)) and (cities_flag == 'Si' or cities_flag == 'No'):
    ccmv.create_complete_multiple_choroplet_view(index_iteration=int(iteration), test=int(choose_test), cities_flag = str(cities_flag))
else:
    print("Il test selezionato non è valido.")