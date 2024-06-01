import numpy as np
import geopandas as gpd
from shapely.geometry import Point

# Carica il file CSV
file_path = 'simplemaps_worldcities/worldcities.csv'
cities = gpd.read_file(file_path)

def get_spatial_coordinate():
    # Filtra solo le città italiane
    italy_cities = cities[cities['country'] == 'Italy']

    # Verifica se ci sono città italiane nel dataset
    if italy_cities.empty:
        raise ValueError("Nessuna città trovata per l'Italia nel file CSV.")
    else:
        # Seleziona una città casuale tra quelle italiane
        city = italy_cities.sample(n=1)
        # Stampa le informazioni della città selezionata
        print(city)

    """"coordinate = city['lat' == '']
    # Numero di nodi da generare
    num_nodes = 10
    nodes = []

    # Genera punti randomici e verifica se sono all'interno dell'Italia
    while len(nodes) < num_nodes:
        point = generate_random_point()
        if italy.contains(point).any():
            nodes.append((point.x, point.y))

    # Mostra le coordinate dei nodi
    for idx, node in enumerate(nodes, start=1):
        print(f"Node {idx}: Longitude = {node[0]}, Latitude = {node[1]}")"""
