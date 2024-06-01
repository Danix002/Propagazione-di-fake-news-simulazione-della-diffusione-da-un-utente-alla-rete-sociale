import os
import matplotlib.pyplot as plt
import geopandas as gpd

file_path = "Visualization\\ne_10m_admin_0_countries\\ne_10m_admin_0_countries.shp"

# Verifica se il file esiste
if os.path.exists(file_path):
    # Carica il file shapefile
    world = gpd.read_file(file_path)
    # Estrai i confini dell'Italia
    italy = world[world['NAME'] == 'Italy']
    # Visualizza i confini dell'Italia
    italy.plot()
    # Mostra la mappa
    plt.show()
else:
    print("Il file non esiste nel percorso specificato.")