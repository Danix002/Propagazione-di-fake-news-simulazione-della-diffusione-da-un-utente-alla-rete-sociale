import simulation_artificial_model as sam
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'Visualization')))
from Visualization import italy_complete_view_with_cities as icvc
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
import mplcursors 
import matplotlib.colors as mcolors
from shapely.geometry import Point
from matplotlib.colorbar import Colorbar
import matplotlib.patches as mpatches
from copy import copy

def get_legend_handles_labels(ax):
    # Ottieni tutti gli artisti presenti nell'asse
    handles, labels = ax.get_legend_handles_labels()
    
    # Se ci sono più artisti, includi solo quelli relativi alla legenda
    legend_handles = []
    for handle, label in zip(handles, labels):
        if isinstance(handle, matplotlib.patches.Patch):
            legend_handles.append(handle)
    return legend_handles, labels


def _add_legend_for_infected(ax, ticks, labels, max_count_infected):
    legend_handles = [
        mpatches.Patch(
            facecolor=_color_density(tick, max_count_infected, status='Infected'),
            edgecolor= '#555555',
            linewidth=1,
            label=label
        )
        for tick, label in zip(ticks, labels)
    ]
    return ax.legend(handles=legend_handles, title='Infetti', loc='lower right')

def _add_legend_for_recovered(ax, ticks, labels, max_count_recovered):
    legend_handles = [
        mpatches.Patch(
            facecolor=_color_density(tick, max_count_recovered, status='Recovered'),
            edgecolor= '#555555',
            linewidth=1,
            label=label
        )
        for tick, label in zip(ticks, labels)
    ]
    ax.legend(handles=legend_handles, loc='lower right')

def _add_legend_for_susceptible(ax, ticks, labels,max_count_susceptible):
    legend_handles = [
        mpatches.Patch(
            facecolor=_color_density(tick, max_count_susceptible, status='Susceptible'),
            edgecolor= '#555555',
            linewidth=1,
            label=label
        )
        for tick, label in zip(ticks, labels)
    ]
    ax.legend(handles=legend_handles, loc='lower right')

def _count_infected(lat, lng, i, test):
    infected_node = sam.get_infected_node(i, test)
    count = 0
    for el in infected_node:
        if (el['latitude'] == lat and el['longitude'] == lng):
            count = count + 1
    return count

def _count_recovered(lat, lng, i, test):
    recovered_node = sam.get_recovered_node(i, test)
    count = 0
    for el in recovered_node:
        if (el['latitude'] == lat and el['longitude'] == lng):
            count = count + 1
    return count

def _count_susceptible(lat, lng, i, test):
    susceptible_node = sam.get_susceptible_node(i, test)
    count = 0
    for el in susceptible_node:
        if (el['latitude'] == lat and el['longitude'] == lng):
            count = count + 1
    return count

def _color_density(number, max_count, status):
    #number_of_nodes_in_simulation = sam.get_number_of_nodes_in_simulation()
    if(status == 'Infected'):
        color = (1, 0, 0)
    if(status == 'Recovered'):
        color = (0, 1, 0)
    if(status == 'Susceptible'):
        color = (0, 0, 1)
    if(not(max_count == 0)):
        hsv_color = mcolors.rgb_to_hsv(color)
        hsv_color[1] *= number / max_count
        rgb_color = mcolors.hsv_to_rgb(hsv_color)
        hex_color = mcolors.rgb2hex(rgb_color)
    else:
        hex_color = '#FFFFFF'
    #hsv_color[1] *= number / number_of_nodes_in_simulation
    return hex_color

def create_complete_choroplet_view(index_iteration, test):
    file_path = 'italy_cities.csv'
    cities = gpd.read_file(file_path)

    # Inizializza una lista per contenere i dati delle città
    city_data = []

    # Cicla attraverso tutte le città e aggiungi i loro dati alla lista
    for index, city in cities.iterrows():
        city_data.append({
            'city': city['city'],
            'lat': city['lat'],
            'lng': city['lng'],
            'region' : city['admin_name'],
            'count_infected': _count_infected(city['lat'], city['lng'], index_iteration, test),
            'count_recovered': _count_recovered(city['lat'], city['lng'], index_iteration, test),
            'count_susceptible': _count_susceptible(city['lat'], city['lng'], index_iteration, test)
        }) 

    regions_counts = [
        {"region": "Abruzzo", "count_infected": 0, "count_recovered": 0, "count_susceptible": 0},
        {"region": "Basilicata", "count_infected": 0, "count_recovered": 0, "count_susceptible": 0},
        {"region": "Calabria", "count_infected": 0, "count_recovered": 0, "count_susceptible": 0},
        {"region": "Campania", "count_infected": 0, "count_recovered": 0, "count_susceptible": 0},
        {"region": "Emilia-Romagna", "count_infected": 0, "count_recovered": 0, "count_susceptible": 0},
        {"region": "Friuli Venezia Giulia", "count_infected": 0, "count_recovered": 0, "count_susceptible": 0},
        {"region": "Lazio", "count_infected": 0, "count_recovered": 0, "count_susceptible": 0},
        {"region": "Liguria", "count_infected": 0, "count_recovered": 0, "count_susceptible": 0},
        {"region": "Lombardy", "count_infected": 0, "count_recovered": 0, "count_susceptible": 0},
        {"region": "Marche", "count_infected": 0, "count_recovered": 0, "count_susceptible": 0},
        {"region": "Molise", "count_infected": 0, "count_recovered": 0, "count_susceptible": 0},
        {"region": "Piedmont", "count_infected": 0, "count_recovered": 0, "count_susceptible": 0},
        {"region": "Puglia", "count_infected": 0, "count_recovered": 0, "count_susceptible": 0},
        {"region": "Sardegna", "count_infected": 0, "count_recovered": 0, "count_susceptible": 0},
        {"region": "Sicilia", "count_infected": 0, "count_recovered": 0, "count_susceptible": 0},
        {"region": "Tuscany", "count_infected": 0, "count_recovered": 0, "count_susceptible": 0},
        {"region": "Trentino-Alto Adige", "count_infected": 0, "count_recovered": 0, "count_susceptible": 0},
        {"region": "Umbria", "count_infected": 0, "count_recovered": 0, "count_susceptible": 0},
        {"region": "Valle d'Aosta", "count_infected": 0, "count_recovered": 0, "count_susceptible": 0},
        {"region": "Veneto", "count_infected": 0, "count_recovered": 0, "count_susceptible": 0}
    ]

    max_count_infected = 0
    max_count_recovered = 0
    max_count_susceptible = 0
    for reg in regions_counts:
        count_infected = 0
        count_recovered = 0
        count_susceptible = 0
        for el in city_data:
            if(el['region'] == reg['region']):
                count_infected = count_infected + el['count_infected'] 
                count_recovered = count_recovered + el['count_recovered'] 
                count_susceptible = count_susceptible + el['count_susceptible']
        reg['count_infected'] = count_infected
        reg['count_recovered'] = count_recovered
        reg['count_susceptible'] = count_susceptible
        if(count_infected > max_count_infected):
            max_count_infected = count_infected
        if(count_recovered > max_count_recovered):
            max_count_recovered = count_recovered
        if(count_susceptible > max_count_susceptible):
            max_count_susceptible = count_susceptible
        if(reg['region'] == 'Friuli Venezia Giulia'):
            reg['region'] = 'Friuli-Venezia Giulia'
        if(reg['region'] == 'Piedmont'):
            reg['region'] = 'Piemonte'
        if(reg['region'] == 'Lombardy'):
            reg['region'] = 'Lombardia'
        if(reg['region'] == 'Tuscany'):
            reg['region'] = 'Toscana'

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20, 10))

    regioni = gpd.read_file("Visualization\\Limiti01012024\\Limiti01012024\\Reg01012024\\Reg01012024_WGS84.shp")

    grigio_scuro = '#666666'
    for my_ax in [ax1, ax2, ax3]:
        icvc.italy_reference_map_with_cities(show_principal_cities_only=True, my_ax = my_ax)
        for reg in regions_counts:
            specific_region = regioni[regioni["DEN_REG"] == reg['region']]
            if (not specific_region.empty):
                if my_ax == ax1:
                    color_region = _color_density(reg['count_infected'], max_count_infected, status='Infected')
                elif my_ax == ax2:
                    color_region = _color_density(reg['count_recovered'], max_count_recovered, status='Recovered')
                elif my_ax == ax3:
                    color_region = _color_density(reg['count_susceptible'], max_count_susceptible, status='Susceptible')
                specific_region.plot(ax=my_ax, color=color_region, edgecolor=grigio_scuro, linewidth=1)
                print("Regione: " + reg['region'] + ", infetti: " +  str(reg['count_infected']) +
                    ", ricoverati: " +  str(reg['count_recovered']) +
                    ", suscettibili: " +  str(reg['count_susceptible']))
            else:
                print("Regione: " + reg['region'] + " non trovata")

    # Aggiungi la legenda
    # Ottieni gli handles e le labels dalla legenda delle città
    handles_cities, labels_cities = ax1.get_legend_handles_labels()

    if(max_count_infected == 0):
        max_count_infected = 120
    step_for_infected = int(max_count_infected / 4)
    ticks_for_infected = list(range(0, max_count_infected + 1, step_for_infected))  # Ticks per la legenda
    labels_for_infected = [str(i) for i in ticks_for_infected]  # Etichette per la legenda
    legenda_infetti = _add_legend_for_infected(ax1, ticks_for_infected, labels_for_infected, max_count_infected)

    if(max_count_recovered == 0):
        max_count_recovered = 120
    step_for_recovered = int(max_count_recovered / 4)
    ticks_for_recovered = list(range(0, max_count_recovered + 1, step_for_recovered))  # Ticks per la legenda
    labels_for_recovered = [str(i) for i in ticks_for_recovered]  # Etichette per la legenda
    _add_legend_for_recovered(ax2, ticks_for_recovered, labels_for_recovered, max_count_recovered)

    if(max_count_susceptible == 0):
        max_count_susceptible = 120
    step_for_susceptible = int(max_count_susceptible / 4)
    ticks_for_susceptible = list(range(0, max_count_susceptible + 1, step_for_susceptible))  # Ticks per la legenda
    labels_for_susceptible = [str(i) for i in ticks_for_susceptible]  # Etichette per la legenda
    _add_legend_for_susceptible(ax3, ticks_for_susceptible, labels_for_susceptible, max_count_susceptible)

    # Ottieni gli handles e le labels dalla legenda degli infetti
    handles_infetti, labels_infetti = legenda_infetti.legendHandles, [t.get_text() for t in legenda_infetti.get_texts()]
    # Combina handles ed etichette
    all_handles = handles_cities + handles_infetti
    all_labels = labels_cities + labels_infetti
    # Aggiungi la legenda combinata all'asse ax1
    ax1.legend(all_handles, all_labels, loc='lower left')

    # Imposta il titolo 
    ax1.set_title('Infected', loc='center')
    ax2.set_title('Recovered', loc='center')
    ax3.set_title('Susceptible', loc='center')

    plt.savefig("Visualization/img_output/choroplet_complete_view.png")

    plt.show()    