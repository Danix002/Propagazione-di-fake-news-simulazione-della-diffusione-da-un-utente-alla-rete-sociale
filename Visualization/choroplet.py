import simulation_artificial_model as sam
import italy_complete_view as icv
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import mplcursors 
import matplotlib.colors as mcolors
from shapely.geometry import Point


def _count_infected(lat, lng):
    infected_node = sam.get_infected_node()
    count = 0
    for el in infected_node:
        if (el['latitude'] == lat and el['longitude'] == lng):
            count = count + 1
    return count

def _color_density(numero):
    """
    Calcola il colore in base alla densità del numero dato.
    
    Parametri:
        numero (float): Il numero da cui calcolare la densità del colore.
        colore_base (str): Il colore di base per la gradazione (predefinito: 'blue').
    
    Ritorna:
        str: Il colore in formato esadecimale (es. '#RRGGBB').
    """
    base_color = 'red'
    norm_numero = numero / float(sam.get_number_of_nodes_in_simulation())  
    cmap = mcolors.get_cmap('viridis')
    colore_densita = cmap(norm_numero)
    colore_esadecimale = mcolors.rgb2hex(colore_densita)
    return colore_esadecimale

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
        'count_infected': _count_infected(city['lat'], city['lng'])
    }) 

grigio_scuro = '#666666'
italy_map = icv.italy_reference_map()

regioni = gpd.read_file("Visualization\\Limiti01012024\\Limiti01012024\\Reg01012024\\Reg01012024_WGS84.shp")
color_density = _color_density()
regioni.plot(ax=italy_map, color='#F0F0F0', alpha=0.3, edgecolor=grigio_scuro, linewidth=1)

    