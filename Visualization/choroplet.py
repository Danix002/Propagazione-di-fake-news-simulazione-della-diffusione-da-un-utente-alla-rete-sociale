import simulation_artificial_model as sam
import italy_complete_view as icv
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import mplcursors 
from shapely.geometry import Point

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
        'count_infected': count_infected(city['city'])
    }) 

#italy_map = icv.italy_reference_map()


def count_infected(city):
    infected_node = sam.get_infected_node()
    