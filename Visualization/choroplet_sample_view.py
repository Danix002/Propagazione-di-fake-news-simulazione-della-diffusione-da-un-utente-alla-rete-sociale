import sys
import os
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import mplcursors
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from IPython.display import display
import matplotlib.colors as mcolors
from shapely.geometry import Point
from matplotlib.colorbar import Colorbar
import matplotlib.patches as mpatches
import matplotlib as mpl
mpl.rcParams.update(mpl.rcParamsDefault)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import simulation_model as sam

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

region_data_list = []

regioni = gpd.read_file("Visualization/Limiti01012024/Limiti01012024/Reg01012024/Reg01012024_WGS84.shp")

for reg in regions_counts:
    specific_region = regioni[regioni["DEN_REG"] == reg['region']]
    region_data = {
    "region_name": reg['region'],
    "region_bounds": specific_region.bounds,
    "region_paths": specific_region.geometry,
    "region_centers": specific_region.centroid
    }
    region_data_list.append(region_data)
  
fig, ax = plt.subplots(figsize=(10, 10))

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
    if status == 'Infected':
        nodes_status = sam.get_infected_node(index_iteration, test)
    if status == 'Recovered':
        nodes_status = sam.get_recovered_node(index_iteration, test)
    if status == 'Susceptible':
        nodes_status = sam.get_susceptible_node(index_iteration, test)
    count = 0
    for el in nodes_status:
        if el['latitude'] == lat and el['longitude'] == lng:
            count += 1
    return count

def _color_density(number, max_count, status):
    if status == 'Infected':
        color = (1, 0, 0)
    if status == 'Recovered':
        color = (0, 1, 0)
    if status == 'Susceptible':
        color = (0, 0, 1)
    if max_count != 0:
        hsv_color = mcolors.rgb_to_hsv(color)
        hsv_color[1] *= number / max_count
        rgb_color = mcolors.hsv_to_rgb(hsv_color)
        hex_color = mcolors.rgb2hex(rgb_color)
    else:
        hex_color = '#FFFFFF'
    return hex_color

def create_sample_choroplet_view(status, index_iteration):
    test = sam.get_choosed_test()
    file_path = 'italy_cities.csv'
    cities = gpd.read_file(file_path)

    city_data = []
    for index, city in cities.iterrows():
        city_data.append({
            'city': city['city'],
            'lat': city['lat'],
            'lng': city['lng'],
            'region': city['admin_name'],
            'count_nodes': _count_nodes(city['lat'], city['lng'], status, index_iteration, test)
        })

    max_count = 0
    for reg in regions_counts:
        count = 0
        for el in city_data:
            if el['region'] == reg['region']:
                count += el['count_nodes']
        reg['count'] = count
        if count > max_count:
            max_count = count
        if reg['region'] == 'Friuli Venezia Giulia':
            reg['region'] = 'Friuli-Venezia Giulia'
        if reg['region'] == 'Piedmont':
            reg['region'] = 'Piemonte'
        if reg['region'] == 'Lombardy':
            reg['region'] = 'Lombardia'
        if reg['region'] == 'Tuscany':
            reg['region'] = 'Toscana'

    grigio_scuro = '#555555'
    for reg in regions_counts:
        specific_region = regioni[regioni["DEN_REG"] == reg['region']]
        if not specific_region.empty:
            color_region = _color_density(reg['count'], max_count, status)
            print(f"Regione: {reg['region']}, {status}: {reg['count']}, color: {color_region}")
            specific_region.plot(ax=ax, color=color_region, edgecolor=grigio_scuro, linewidth=1)
        else:
            print(f"Regione: {reg['region']} non trovata")

    ax.axis('off')

    if max_count <= 4:
        max_count = 120

    step = int(max_count / 4)
    ticks = list(range(0, max_count + 1, step))
    labels = [str(i) for i in ticks]
    _add_legend(plt.gca(), ticks, labels, status, max_count)

    ax.set_title(f"{status} in test {test} (iterations n°: {index_iteration})", loc='center')

    plt.savefig(f"Visualization/img_output/choroplet_sample_view_{status}_{test}.png")
    plt.savefig(f"Visualization/svg_output/choroplet_sample_view_{status}_{test}.svg", format = "svg")

    plt.show()

# Run in Jupyter Notebook
create_sample_choroplet_view(str(sys.argv[1]), int(sys.argv[2]))

