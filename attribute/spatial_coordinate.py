import numpy as np
import geopandas as gpd
from shapely.geometry import Point
import csv 

def get_spatial_coordinate_latitude():
    file_path = 'italy_cities.csv'
    cities = gpd.read_file(file_path)
    city = cities.sample(n=1) 
    latitude = city['lat'].values[0] 
    return latitude

def get_spatial_coordinate_longitude():
    file_path = 'italy_cities.csv'
    cities = gpd.read_file(file_path)
    city = cities.sample(n=1) 
    longitude = city['lng'].values[0]
    return longitude

