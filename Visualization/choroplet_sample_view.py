import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import simulation_artificial_model as sam
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import mplcursors 
from IPython.display import display
import matplotlib.colors as mcolors
from shapely.geometry import Point
from matplotlib.colorbar import Colorbar
import matplotlib.patches as mpatches
import matplotlib as mpl
mpl.rcParams.update(mpl.rcParamsDefault)


def _add_legend(ax, ticks, labels, my_title, max_count):
    legend_handles = [
        mpatches.Patch(
            facecolor=_color_density(tick, max_count, my_title),
            edgecolor= '#555555',
            linewidth=1,
            label=label
        )
        for tick, label in zip(ticks, labels)
    ]
    ax.legend(handles=legend_handles, title=my_title, loc='lower right')


def _count_nodes(lat, lng, status, index_iteration, test):
    nodes_status = []
    if(status == 'Infected'):
        nodes_status = sam.get_infected_node(index_iteration, test)
    if(status == 'Recovered'):
        nodes_status = sam.get_recovered_node(index_iteration, test)
    if(status == 'Susceptible'):
        nodes_status = sam.get_susceptible_node(index_iteration, test)
    count = 0
    for el in nodes_status:
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

def create_sample_choroplet_view(status, index_iteration, test):
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
            'count_nodes': _count_nodes(city['lat'], city['lng'], status, index_iteration, test)
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
                count = count + el['count_nodes'] 
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

    regioni = gpd.read_file("Visualization\\Limiti01012024\\Limiti01012024\\Reg01012024\\Reg01012024_WGS84.shp")

    grigio_scuro = '#555555'
    bianco = '#FFFFFF'
    fig, ax = plt.subplots(figsize=(10, 10))  
    for reg in regions_counts:
        specific_region = regioni[regioni["DEN_REG"] == reg['region']]
        if (not specific_region.empty):
            color_region = _color_density(reg['count'], max_count, status)
            print("Regione: " + reg['region'] + ", " + status + ": " + str(reg['count']) + ", color: " + color_region)
            specific_region.plot(ax=ax, color=color_region, edgecolor=grigio_scuro, linewidth=1)  
            # Aggiungi le informazioni per l'hover
            """mplcursors.cursor(hover=True).connect(
                    "add", lambda sel: sel.annotation.set_text(
                        f"{reg['region']}: {status} {reg['count']}"
                        )
                    )"""
        else:
            print("Regione: " + reg['region'] + " non trovata")

    ax.axis('off') 

    # Aggiungi la legenda
    if(max_count == 0):
        max_count = 120
    step = int(max_count / 4)
    ticks = list(range(0, max_count + 1, step))  # Ticks per la legenda
    labels = [str(i) for i in ticks]  # Etichette per la legenda
    _add_legend(plt.gca(), ticks, labels, status, max_count)

    ax.set_title(status + " in test " + str(test) + " (iterations n°: "+ str(index_iteration) + ")", loc='center')

    plt.savefig("Visualization/img_output/choroplet_sample_view_"+ status + "_" + str(test) +".png")

    plt.show()
    

# Run in Jupyter Notebook
create_sample_choroplet_view(str(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))