import italy_complete_view as icv
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Point

italy_map = icv.italy_reference_map()

data = {
    'city': ['Aquila', 'Potenza', 'Catanzaro', 'Naples', 'Bologna', 'Trieste', 'Rome', 'Genoa', 'Milan', 'Ancona', 'Campobasso', 'Turin', 'Bari', 'Cagliari', 'Palermo', 'Florence', 'Trento', 'Perugia', 'Aosta', 'Venice'],
    'lat': [42.3505, 40.6444, 38.8910, 40.8518, 44.4949, 45.6500, 41.9028, 44.4056, 45.4642, 43.6158, 41.5638, 45.0703, 41.1172, 39.2238, 38.1157, 43.7696, 46.0679, 43.1107, 45.7380, 45.4408],
    'lng': [13.3995, 15.8086, 16.5994, 14.2681, 11.3426, 13.8000, 12.4964, 8.9463, 9.1900, 13.5189, 14.6563, 7.6869, 16.8719, 9.1217, 13.3615, 11.2558, 11.1211, 12.3892, 7.3153, 12.3155]
}

# Crea un DataFrame da questi dati
df = pd.DataFrame(data)

# Crea una colonna geometrica nel DataFrame
geometry = [Point(xy) for xy in zip(df['lng'], df['lat'])]

# Crea un GeoDataFrame con le coordinate geografiche
gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")

# Converti il GeoDataFrame nel sistema di coordinate delle regioni (EPSG:32632)
gdf = gdf.to_crs("EPSG:32632")

# Aggiungi i punti sulla mappa
gdf.plot(ax=italy_map, color='red', markersize=20, label='Cities', zorder=5)

# Aggiungi etichette con il nome delle città vicino ai punti
for x, y, label in zip(gdf.geometry.x, gdf.geometry.y, gdf['city']):
    italy_map.annotate(label, xy=(x, y), xytext=(3, 3), textcoords="offset points")

# Aggiungi una legenda
plt.legend()

# Mostra la mappa
plt.show()