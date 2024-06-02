import choroplet_sample_view as csv
import choroplet_complete_view as ccv

choose_choroplet = input("Sono disponibili due choroplet con due livelli di dettaglio differenti, se vuoi visualizzare quella più dettagliata premi 1, altrimenti 0: ")
iteration = input("Inserisci il numero d'iterazione che vuoi visualizzare sulla choroplet: ")
if(int(choose_choroplet) == 0):
    csv.create_sample_choroplet_view(status='Recovered', index_iteration=int(iteration), test=1)
    csv.create_sample_choroplet_view(status='Infected', index_iteration=int(iteration), test=1)
    csv.create_sample_choroplet_view(status='Susceptible',index_iteration=int(iteration), test=1)
    csv.create_sample_choroplet_view(status='Recovered', index_iteration=int(iteration), test=2)
    csv.create_sample_choroplet_view(status='Infected', index_iteration=int(iteration), test=2)
    csv.create_sample_choroplet_view(status='Susceptible',index_iteration=int(iteration), test=2)
    csv.create_sample_choroplet_view(status='Recovered', index_iteration=int(iteration), test=3)
    csv.create_sample_choroplet_view(status='Infected', index_iteration=int(iteration), test=3)
    csv.create_sample_choroplet_view(status='Susceptible',index_iteration=int(iteration), test=3)
elif(int(choose_choroplet) == 1):
    ccv.create_complete_choroplet_view(index_iteration=int(iteration), test=1)
    ccv.create_complete_choroplet_view(index_iteration=int(iteration), test=2)
    ccv.create_complete_choroplet_view(index_iteration=int(iteration), test=3)