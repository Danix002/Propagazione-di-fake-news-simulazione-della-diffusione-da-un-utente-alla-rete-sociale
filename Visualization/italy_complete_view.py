import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

def italy_reference_map():
    comuni = gpd.read_file("Visualization\\Limiti01012024\\Limiti01012024\\Com01012024\\Com01012024_WGS84.shp")
    province = gpd.read_file("Visualization\\Limiti01012024\\Limiti01012024\\ProvCM01012024\\ProvCM01012024_WGS84.shp")
    regioni = gpd.read_file("Visualization\\Limiti01012024\\Limiti01012024\\Reg01012024\\Reg01012024_WGS84.shp")
    ripartizioni_geo = gpd.read_file("Visualization\\Limiti01012024\\Limiti01012024\\RipGeo01012024\\RipGeo01012024_WGS84.shp")

    grigio_chiaro = '#AAAAAA'  
    grigio_scuro = '#666666'

    ax = comuni.plot(color='#F0F0F0', edgecolor=grigio_chiaro, linewidth=0.8, alpha=0.1, figsize=(10, 10))
    province.plot(ax=ax, color='#F0F0F0', alpha=0.2, edgecolor='gray', linewidth=0.9)
    regioni.plot(ax=ax, color='#F0F0F0', alpha=0.3, edgecolor=grigio_scuro, linewidth=1)

    confine_italia = regioni.unary_union
    gpd.GeoSeries([confine_italia]).boundary.plot(ax=ax, edgecolor='#555555', linewidth=1.1)
    return ax

    # plt.show()