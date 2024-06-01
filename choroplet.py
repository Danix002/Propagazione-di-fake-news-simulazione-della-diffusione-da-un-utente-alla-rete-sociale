import simulation_artificial_model as sam
import Visualization.italy_complete_view as icv
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

def _add_legend(ax, ticks, labels):
    legend_handles = [mpatches.Patch(color=_color_density(tick, max_count), label=label) for tick, label in zip(ticks, labels)]
    ax.legend(handles=legend_handles, title='Infetti', loc='lower right')


def _count_infected(lat, lng):
    infected_node = sam.get_infected_node()
    count = 0
    for el in infected_node:
        if (el['latitude'] == lat and el['longitude'] == lng):
            count = count + 1
    return count

def _color_density(number, max_count):
    #number_of_nodes_in_simulation = sam.get_number_of_nodes_in_simulation()
    color = (1, 0, 0)
    hsv_color = mcolors.rgb_to_hsv(color)
    hsv_color[1] *= number / max_count
    #hsv_color[1] *= number / number_of_nodes_in_simulation
    rgb_color = mcolors.hsv_to_rgb(hsv_color)
    hex_color = mcolors.rgb2hex(rgb_color)
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
        'count_infected': _count_infected(city['lat'], city['lng'])
    }) 

grigio_scuro = '#666666'

regions_counts = [
    {"region": "Abruzzo", "count": 0},
    {"region": "Basilicata", "count": 0},
    {"region": "Calabria", "count": 0},
    {"region": "Campania", "count": 0},
    {"region": "Emilia-Romagna", "count": 0},
    {"region": "Friuli Venezia Giulia", "count": 0},
    {"region": "Lazio", "count": 0},
    {"region": "Liguria", "count": 0},
    {"region": "Lombardy", "count": 0},
    {"region": "Marche", "count": 0},
    {"region": "Molise", "count": 0},
    {"region": "Piedmont", "count": 0},
    {"region": "Puglia", "count": 0},
    {"region": "Sardegna", "count": 0},
    {"region": "Sicilia", "count": 0},
    {"region": "Tuscany", "count": 0},
    {"region": "Trentino-Alto Adige", "count": 0},
    {"region": "Umbria", "count": 0},
    {"region": "Valle d'Aosta", "count": 0},
    {"region": "Veneto", "count": 0}
]

max_count = 0
for reg in regions_counts:
    count = 0
    for el in city_data:
        if(el['region'] == reg['region']):
            count = count + el['count_infected'] 
    reg['count'] = count
    if(count > max_count):
         max_count = count
    if(reg['region'] == 'Friuli Venezia Giulia'):
          reg['region'] = 'Friuli-Venezia Giulia'
    if(reg['region'] == 'Piedmont'):
          reg['region'] = 'Piemonte'
    if(reg['region'] == 'Lombardy'):
          reg['region'] = 'Lombardia'
    if(reg['region'] == 'Tuscany'):
          reg['region'] = 'Toscana'

italy_map = icv.italy_reference_map()
regioni = gpd.read_file("Visualization\\Limiti01012024\\Limiti01012024\\Reg01012024\\Reg01012024_WGS84.shp")

for reg in regions_counts:
    specific_region = regioni[regioni["DEN_REG"] == reg['region']]
    if (not specific_region.empty):
        color_region = _color_density(reg['count'], max_count)
        print("Regione: " + reg['region'] + ", infetti: " +  str(reg['count']) + ", color: " + color_region)
        specific_region.plot(ax=italy_map, color=color_region, alpha=0.3, edgecolor=grigio_scuro, linewidth=1)
    else:
        print("Regione: " + reg['region'] + " non trovata")

# Aggiungi la legenda
step = 10
ticks = list(range(0, max_count + 1, step))  # Ticks per la legenda
labels = [str(i) for i in ticks]  # Etichette per la legenda
_add_legend(plt.gca(), ticks, labels)

plt.show()    