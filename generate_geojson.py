import geopandas as gpd

# Carica il file shapefile della mappa dell'Italia
italy_shapefile = "Visualization\Limiti01012024\Limiti01012024\Reg01012024\Reg01012024_WGS84.shp"
gdf = gpd.read_file(italy_shapefile)

# Salva il geodataframe come GeoJSON
geojson_path = "italy.geojson"
gdf.to_file(geojson_path, driver="GeoJSON")