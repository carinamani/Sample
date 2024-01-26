# -*- coding: utf-8 -*-
"""
Created on Fri Jan 26 17:21:40 2024

@author: carinamani

This script calculates the total land use dedicated to the production of maize within the US by overlaying geo-refferenced CSV data from IFPRI with county boundaires.
The output is a map. 

"""

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from shapely.geometry import box
import matplotlib.pyplot as plt

### Read in parquet on global crop production and drop all values that aren't in the USA 
crop_production_raw = pd.read_parquet('Inputs/spam2010V2r0_global_area.parquet')
crop_USA = crop_production_raw[crop_production_raw['iso3'] == 'USA']

### Convert crop production to GeoDataFrame using XY coordinates in CSV and clip by bounding box for continental USA
geometry = [Point(xy) for xy in zip(crop_USA['x'], crop_USA['y'])]
crop_USA = gpd.GeoDataFrame(crop_USA, geometry=geometry, crs='EPSG:4326') 
bounding_box = box(-131.894536,23.869037,-64.570317,50.322327)# defines bounding box for continental USA
crop_USA_clip = crop_USA[crop_USA.geometry.within(bounding_box)]

### Import shapefile with boundaries of USA counties and clip to bounding box
counties = gpd.read_file('Inputs/county_boundaries/cb_2018_us_county_20m.shp')
counties_continental = counties[counties.geometry.within(bounding_box)]

### Join crop data and county boundaries and sum the area within each county
crop_join = gpd.sjoin(crop_USA_clip, counties_continental, how='left', op='within')
maize_area_sum = crop_join.groupby('NAME')['maiz_a'].sum()
counties_maize = counties_continental.merge(maize_area_sum, left_on='NAME', right_index=True)

### Plot counties by maize production, format, and save as a JPG
fig, ax = plt.subplots(1, 1, figsize=(12, 8))
counties_maize.plot(column='maiz_a', cmap='Oranges', linewidth=0.4, ax=ax, edgecolor='0.8', legend=False)
ax.set_axis_off()
cbar = plt.colorbar(ax.collections[0], ax=ax, orientation='horizontal', fraction=0.05, pad=0.1)
cbar.set_label('Hectares')
plt.title('Land used for maize production by US county', fontdict={'fontsize': 20, 'fontfamily': 'Verdana'})

plt.savefig('maize_production_map.jpg', format='jpg', dpi=300, bbox_inches='tight')



