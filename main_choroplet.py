import Visualization.choroplet_sample_view as csv
import Visualization.choroplet_complete_view as ccv

choose_choroplet = input("Sono disponibili due choroplet con due livelli di dettaglio differenti, se vuoi visualizzare quella più dettagliata premi 1, altrimenti 0: ")
iteration = input("Inserisci il numero d'iterazione che vuoi visualizzare sulla choroplet: ")
choose_test = input("Ci siamo quasi, come ultima cosa scegli il test che vuoi visualizzare sulla choroplet: ")
if(int(choose_choroplet) == 0):
    if(int(choose_test) == 1):
        csv.create_sample_choroplet_view(status='Recovered', index_iteration=int(iteration), test=1)
        csv.create_sample_choroplet_view(status='Infected', index_iteration=int(iteration), test=1)
        csv.create_sample_choroplet_view(status='Susceptible',index_iteration=int(iteration), test=1)
    if(int(choose_test) == 2):
        csv.create_sample_choroplet_view(status='Recovered', index_iteration=int(iteration), test=2)
        csv.create_sample_choroplet_view(status='Infected', index_iteration=int(iteration), test=2)
        csv.create_sample_choroplet_view(status='Susceptible',index_iteration=int(iteration), test=2)
    if(int(choose_test) == 3):
        csv.create_sample_choroplet_view(status='Recovered', index_iteration=int(iteration), test=3)
        csv.create_sample_choroplet_view(status='Infected', index_iteration=int(iteration), test=3)
        csv.create_sample_choroplet_view(status='Susceptible',index_iteration=int(iteration), test=3)
    if(int(choose_test) == 4):
        csv.create_sample_choroplet_view(status='Recovered', index_iteration=int(iteration), test=4)
        csv.create_sample_choroplet_view(status='Infected', index_iteration=int(iteration), test=4)
        csv.create_sample_choroplet_view(status='Susceptible',index_iteration=int(iteration), test=4)
    if(int(choose_test) == 5):
        csv.create_sample_choroplet_view(status='Recovered', index_iteration=int(iteration), test=5)
        csv.create_sample_choroplet_view(status='Infected', index_iteration=int(iteration), test=5)
        csv.create_sample_choroplet_view(status='Susceptible', index_iteration=int(iteration), test=5)
elif(int(choose_choroplet) == 1):
    if(int(choose_test) == 1):
        ccv.create_complete_choroplet_view(index_iteration=int(iteration), test=1)
    if(int(choose_test) == 2):
        ccv.create_complete_choroplet_view(index_iteration=int(iteration), test=2)
    if(int(choose_test) == 3):
        ccv.create_complete_choroplet_view(index_iteration=int(iteration), test=3)
    if(int(choose_test) == 4):
        ccv.create_complete_choroplet_view(index_iteration=int(iteration), test=4)
    if(int(choose_test) == 5):
        ccv.create_complete_choroplet_view(index_iteration=int(iteration), test=5)