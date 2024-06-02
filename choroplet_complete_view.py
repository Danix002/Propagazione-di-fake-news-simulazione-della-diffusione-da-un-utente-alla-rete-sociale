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

def _add_legend_for_infected(ax, ticks, labels):
    legend_handles = [
        mpatches.Patch(
            facecolor=_color_density(tick, max_count_infected, status='Infected'),
            edgecolor= '#555555',
            linewidth=1,
            label=label
        )
        for tick, label in zip(ticks, labels)
    ]
    ax.legend(handles=legend_handles, title='Infetti', loc='lower right')

def _add_legend_for_recovered(ax, ticks, labels):
    legend_handles = [
        mpatches.Patch(
            facecolor=_color_density(tick, max_count_recovered, status='Recovered'),
            edgecolor= '#555555',
            linewidth=1,
            label=label
        )
        for tick, label in zip(ticks, labels)
    ]
    ax.legend(handles=legend_handles, title='Ricoverati', loc='lower right')

def _add_legend_for_suscetible(ax, ticks, labels):
    legend_handles = [
        mpatches.Patch(
            facecolor=_color_density(tick, max_count_suscetible, status='Suscetible'),
            edgecolor= '#555555',
            linewidth=1,
            label=label
        )
        for tick, label in zip(ticks, labels)
    ]
    ax.legend(handles=legend_handles, title='Suscettibili', loc='lower right')

def _count_infected(lat, lng):
    infected_node = sam.get_infected_node()
    count = 0
    for el in infected_node:
        if (el['latitude'] == lat and el['longitude'] == lng):
            count = count + 1
    return count

def _count_recovered(lat, lng):
    recovered_node = sam.get_recovered_node()
    count = 0
    for el in recovered_node:
        if (el['latitude'] == lat and el['longitude'] == lng):
            count = count + 1
    return count

def _count_suscetible(lat, lng):
    suscetible_node = sam.get_susceptible_node()
    count = 0
    for el in suscetible_node:
        if (el['latitude'] == lat and el['longitude'] == lng):
            count = count + 1
    return count

def _color_density(number, max_count, status):
    #number_of_nodes_in_simulation = sam.get_number_of_nodes_in_simulation()
    if(status == 'Infected'):
        color = (1, 0, 0)
    if(status == 'Recovered'):
        color = (0, 1, 0)
    if(status == 'Suscetible'):
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
        'count_infected': _count_infected(city['lat'], city['lng']),
        'count_recovered': _count_recovered(city['lat'], city['lng']),
        'count_suscetible': _count_suscetible(city['lat'], city['lng'])
    }) 

regions_counts = [
    {"region": "Abruzzo", "count_infected": 0, "count_recovered": 0, "count_suscetible": 0},
    {"region": "Basilicata", "count_infected": 0, "count_recovered": 0, "count_suscetible": 0},
    {"region": "Calabria", "count_infected": 0, "count_recovered": 0, "count_suscetible": 0},
    {"region": "Campania", "count_infected": 0, "count_recovered": 0, "count_suscetible": 0},
    {"region": "Emilia-Romagna", "count_infected": 0, "count_recovered": 0, "count_suscetible": 0},
    {"region": "Friuli Venezia Giulia", "count_infected": 0, "count_recovered": 0, "count_suscetible": 0},
    {"region": "Lazio", "count_infected": 0, "count_recovered": 0, "count_suscetible": 0},
    {"region": "Liguria", "count_infected": 0, "count_recovered": 0, "count_suscetible": 0},
    {"region": "Lombardy", "count_infected": 0, "count_recovered": 0, "count_suscetible": 0},
    {"region": "Marche", "count_infected": 0, "count_recovered": 0, "count_suscetible": 0},
    {"region": "Molise", "count_infected": 0, "count_recovered": 0, "count_suscetible": 0},
    {"region": "Piedmont", "count_infected": 0, "count_recovered": 0, "count_suscetible": 0},
    {"region": "Puglia", "count_infected": 0, "count_recovered": 0, "count_suscetible": 0},
    {"region": "Sardegna", "count_infected": 0, "count_recovered": 0, "count_suscetible": 0},
    {"region": "Sicilia", "count_infected": 0, "count_recovered": 0, "count_suscetible": 0},
    {"region": "Tuscany", "count_infected": 0, "count_recovered": 0, "count_suscetible": 0},
    {"region": "Trentino-Alto Adige", "count_infected": 0, "count_recovered": 0, "count_suscetible": 0},
    {"region": "Umbria", "count_infected": 0, "count_recovered": 0, "count_suscetible": 0},
    {"region": "Valle d'Aosta", "count_infected": 0, "count_recovered": 0, "count_suscetible": 0},
    {"region": "Veneto", "count_infected": 0, "count_recovered": 0, "count_suscetible": 0}
]

max_count_infected = 0
max_count_recovered = 0
max_count_suscetible = 0
for reg in regions_counts:
    count_infected = 0
    count_recovered = 0
    count_suscetible = 0
    for el in city_data:
        if(el['region'] == reg['region']):
            count_infected = count_infected + el['count_infected'] 
            count_recovered = count_recovered + el['count_recovered'] 
            count_suscetible = count_suscetible + el['count_suscetible']
    reg['count_infected'] = count_infected
    reg['count_recovered'] = count_recovered
    reg['count_suscetible'] = count_suscetible
    if(count_infected > max_count_infected):
         max_count_infected = count_infected
    if(count_recovered > max_count_recovered):
         max_count_recovered = count_recovered
    if(count_suscetible > max_count_suscetible):
         max_count_suscetible = count_suscetible
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
    legend_for_cities = icvc.italy_reference_map_with_cities(show_principal_cities_only=True, my_ax = my_ax)
    for reg in regions_counts:
        specific_region = regioni[regioni["DEN_REG"] == reg['region']]
        if (not specific_region.empty):
            if my_ax == ax1:
                color_region = _color_density(reg['count_infected'], max_count_infected, status='Infected')
            elif my_ax == ax2:
                color_region = _color_density(reg['count_recovered'], max_count_recovered, status='Recovered')
            elif my_ax == ax3:
                color_region = _color_density(reg['count_suscetible'], max_count_suscetible, status='Suscetible')
            specific_region.plot(ax=my_ax, color=color_region, edgecolor=grigio_scuro, linewidth=1)
            print("Regione: " + reg['region'] + ", infetti: " +  str(reg['count_infected']) +
                ", ricoverati: " +  str(reg['count_recovered']) +
                ", suscettibili: " +  str(reg['count_suscetible']))
        else:
            print("Regione: " + reg['region'] + " non trovata")

# Aggiungi la legenda
step_for_infected = int(max_count_infected / 4)
ticks_for_infected = list(range(0, max_count_infected + 1, step_for_infected))  # Ticks per la legenda
labels_for_infected = [str(i) for i in ticks_for_infected]  # Etichette per la legenda
_add_legend_for_infected(ax1, ticks_for_infected, labels_for_infected)

step_for_recovered = int(max_count_recovered / 4)
ticks_for_recovered = list(range(0, max_count_recovered + 1, step_for_recovered))  # Ticks per la legenda
labels_for_recovered = [str(i) for i in ticks_for_recovered]  # Etichette per la legenda
_add_legend_for_recovered(ax2, ticks_for_recovered, labels_for_recovered)

if(max_count_suscetible == 0):
    max_count_suscetible = 120
step_for_suscetible = int(max_count_suscetible / 4)
ticks_for_suscetible = list(range(0, max_count_suscetible + 1, step_for_suscetible))  # Ticks per la legenda
labels_for_suscetible = [str(i) for i in ticks_for_suscetible]  # Etichette per la legenda
_add_legend_for_suscetible(ax3, ticks_for_suscetible, labels_for_suscetible)


plt.savefig("Visualization/img_output/choroplet_complete_view.png")

plt.show()    