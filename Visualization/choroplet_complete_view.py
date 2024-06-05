import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import simulation_model as sam
import italy_complete_view_with_cities as icvc
import matplotlib
import matplotlib.colors as mcolors
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display
import matplotlib.colors as mcolors
from shapely.geometry import Point
from matplotlib.colorbar import Colorbar
import matplotlib.patches as mpatches
import matplotlib as mpl
mpl.rcParams.update(mpl.rcParamsDefault)

def get_legend_handles_labels(ax):
    # Ottieni tutti gli artisti presenti nell'asse
    handles, labels = ax.get_legend_handles_labels()
    # Se ci sono più artisti, includi solo quelli relativi alla legenda
    legend_handles = []
    for handle, label in zip(handles, labels):
        if isinstance(handle, matplotlib.patches.Patch):
            legend_handles.append(handle)
    return legend_handles, labels

def _add_legend(ax, ticks, labels, max_count, my_title):
    legend_handles = [
        mpatches.Patch(
            facecolor=_color_density(tick, max_count, my_title),
            edgecolor= '#555555',
            linewidth=1,
            label=label
        )
        for tick, label in zip(ticks, labels)
    ]
    return ax.legend(handles=legend_handles, title=my_title, loc='lower right')

def _count_nodes(lat, lng, index_iteration, test, status):
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

def create_complete_choroplet_view(status, index_iteration):
    test = sam.get_choosed_test()
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
            'count_nodes': _count_nodes(city['lat'], city['lng'], index_iteration, test, status)
        })

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

    fig, ax = plt.subplots(figsize=(10, 10)) 
    icvc.italy_reference_map_with_cities(show_principal_cities_only=True, my_ax = ax)
    regioni = gpd.read_file("Visualization\\Limiti01012024\\Limiti01012024\\Reg01012024\\Reg01012024_WGS84.shp")

    grigio_scuro = '#666666'
    for reg in regions_counts:
        specific_region = regioni[regioni["DEN_REG"] == reg['region']]
        if (not specific_region.empty):
            color_region = _color_density(reg['count'], max_count, status)
            print("Regione: " + reg['region'] + ", " + status + ": " + str(reg['count']) + ", color: " + color_region)
            specific_region.plot(ax=ax, color=color_region, edgecolor=grigio_scuro, linewidth=1)
        else:
            print("Regione: " + reg['region'] + " non trovata")

    # Aggiungi la legenda
    handles_cities, labels_cities = ax.get_legend_handles_labels()

    if max_count <= 4:
        max_count = 120

    step = int(max_count / 4)
    ticks = list(range(0, max_count + 1, step))  # Ticks per la legenda
    labels = [str(i) for i in ticks]  # Etichette per la legenda
    legenda_infetti =_add_legend(plt.gca(), ticks, labels, max_count, status)

    # Ottieni gli handles e le labels dalla legenda degli infetti
    handles_infetti, labels_infetti = legenda_infetti.legend_handles, [t.get_text() for t in legenda_infetti.get_texts()]
    # Combina handles ed etichette
    all_handles = handles_cities + handles_infetti
    all_labels = labels_cities + labels_infetti
    # Aggiungi la legenda combinata all'asse ax1
    ax.legend(all_handles, all_labels, loc='lower left')

    ax.set_title(status + " in test " + str(test) + " (iterations n°: "+ str(index_iteration) + ")", loc='center')

    plt.savefig("Visualization/img_output/choroplet_complete_view_"+ status + "_" + str(test) +".png")
    plt.savefig(f"Visualization/svg_output/choroplet_complete_view_{status}_{test}.svg", format = "svg")

    plt.show()


# Run in Jupyter Notebook
create_complete_choroplet_view(str(sys.argv[1]), int(sys.argv[2]))