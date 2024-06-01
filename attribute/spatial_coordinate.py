import numpy as np
import geopandas as gpd
from shapely.geometry import Point
import csv 

def get_spatial_coordinate_latitude(city):
    latitude = city['lat'].values[0]
    return latitude

def get_spatial_coordinate_longitude(city):   
    longitude = city['lng'].values[0]
    return longitude