# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 17:42:20 2023

@author: yewei
"""

file_dir0 = r'D:\YEWEI\project\traffic\road_each\G42'
file_dir1 = r'D:\YEWEI\project\traffic\202310-公路交通一张图\1.基础地理信息'

# import geopandas as gpd
# import pandas as pd
# import matplotlib.pyplot as plt

# road = gpd.read_file(file_dir0+"\G42.shp")
# boundary = gpd.read_file(file_dir1+"\四川省_省界.shp")

import shapefile
file = shapefile.Reader(file_dir0+"\G42.shp")
file_fields = file.fields

import numpy as np 
shape_record = file.shapeRecords()
#polyline线条的经纬度
position = []
for record in shape_record:
    points = record.shape.points
    parts  = record.shape.parts
    position.append(points[parts[-1]:])
    print(points[parts[-1]:]) #1513段，每段经纬度点均在


