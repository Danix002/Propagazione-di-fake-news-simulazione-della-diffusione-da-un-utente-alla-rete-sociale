import italy_complete_view as icv
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import mplcursors 
from shapely.geometry import Point
from copy import copy

def italy_reference_map_with_cities(show_principal_cities_only, my_ax = None):
    file_path = 'italy_cities.csv'
    cities = gpd.read_file(file_path)

    # Inizializza una lista per contenere i dati delle città
    city_data = []

    # Cicla attraverso tutte le città e aggiungi i loro dati alla lista
    for index, city in cities.iterrows():
        city_data.append({
            'city': city['city'],
            'lat': city['lat'],
            'lng': city['lng']
        }) 

    if my_ax:
        italy_map = icv.italy_reference_map(my_ax)
    else:
        italy_map = icv.italy_reference_map()

    principal_city = {
        'city': ['L\'Aquila', 'Potenza', 'Catanzaro', 'Naples', 'Bologna', 'Trieste', 'Rome', 'Genoa', 'Milan', 'Ancona', 'Campobasso', 'Turin', 'Bari', 'Cagliari', 'Palermo', 'Florence', 'Trento', 'Perugia', 'Aosta', 'Venice'],
    }

    # Crea un DataFrame da questi dati
    df = pd.DataFrame(city_data)

    # Filtra il DataFrame solo per le città principali
    filtered_df = df[df['city'].isin(principal_city['city'])]
    geometry = [Point(xy) for xy in zip(filtered_df['lng'], filtered_df['lat'])]
    gdf = gpd.GeoDataFrame(filtered_df, geometry=geometry, crs="EPSG:4326")
    gdf = gdf.to_crs("EPSG:32632")
    gdf.plot(ax=italy_map, color='black', markersize=20, label='Principal Cities', zorder=5)
    # Aggiungi etichette con il nome delle città vicino ai punti
    for x, y, label in zip(gdf.geometry.x, gdf.geometry.y, gdf['city']):
        italy_map.annotate(label, xy=(x, y), xytext=(3, 3), textcoords="offset points", zorder=6)
    
    # Filtra il DataFrame per le città non principali
    filtered_df = df[~df['city'].isin(principal_city['city'])]
    geometry = [Point(xy) for xy in zip(filtered_df['lng'], filtered_df['lat'])]
    gdf = gpd.GeoDataFrame(filtered_df, geometry=geometry, crs="EPSG:4326")
    gdf = gdf.to_crs("EPSG:32632")
    grigio_scuro = '#666666'
    gdf.plot(ax=italy_map, color=grigio_scuro, markersize=10, label='Other Cities', zorder=4)

    if(not(show_principal_cities_only)):
        # Aggiungi etichette con il nome delle città vicino ai punti
        for x, y, label in zip(gdf.geometry.x, gdf.geometry.y, gdf['city']):
            italy_map.annotate(label, xy=(x, y), xytext=(3, 3), textcoords="offset points")

    # Remove axis frames
    #italy_map.axis('off') 
    # Aggiungi una legenda
    italy_map.legend()
    #plt.show()
   