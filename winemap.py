#!/usr/bin/env python
# coding: utf-8

# In[1]:


# TO DO
# Add coordinate points for addresses of wineries
# Regional map .shp for more accurate regions/appelations?


# In[2]:


# Aidan Loten, asloten@gmail.com, 1/18/2020

import geopandas as gpd

shapefile_states = 'C:\\Users\\aslot\\miniconda3\\envs\\winemap\\ne_10m_admin_1_states_provinces\\ne_10m_admin_1_states_provinces.shp'
shapefile_countries = 'C:\\Users\\aslot\\miniconda3\\envs\\winemap\\ne_110m_admin_0_countries\\ne_110m_admin_0_countries.shp'
# shapefile_states geodataframe columns below
# index(['featurecla', 'scalerank', 'adm1_code', 'diss_me', 'iso_3166_2',
#        'wikipedia', 'iso_a2', 'adm0_sr', 'name', 'name_alt', 'name_local',
#        'type', 'type_en', 'code_local', 'code_hasc', 'note', 'hasc_maybe',
#        'region', 'region_cod', 'provnum_ne', 'gadm_level', 'check_me',
#        'datarank', 'abbrev', 'postal', 'area_sqkm', 'sameascity', 'labelrank',
#        'name_len', 'mapcolor9', 'mapcolor13', 'fips', 'fips_alt', 'woe_id',
#        'woe_label', 'woe_name', 'latitude', 'longitude', 'sov_a3', 'adm0_a3',
#        'adm0_label', 'admin', 'geonunit', 'gu_a3', 'gn_id', 'gn_name',
#        'gns_id', 'gns_name', 'gn_level', 'gn_region', 'gn_a1_code',
#        'region_sub', 'sub_code', 'gns_level', 'gns_lang', 'gns_adm1',
#        'gns_region', 'min_label', 'max_label', 'min_zoom', 'wikidataid',
#        'name_ar', 'name_bn', 'name_de', 'name_en', 'name_es', 'name_fr',
#        'name_el', 'name_hi', 'name_hu', 'name_id', 'name_it', 'name_ja',
#        'name_ko', 'name_nl', 'name_pl', 'name_pt', 'name_ru', 'name_sv',
#        'name_tr', 'name_vi', 'name_zh', 'ne_id', 'geometry'],
#       dtype='object')

# Read shapefiles using Geopandas, gdf_states is used for countries with wine to add regional detail
gdf_states = gpd.read_file(shapefile_states)[['admin','adm0_a3','name','region','geometry']]
gdf_states.columns = ['country','country_code','state_name','region_name','geometry']
gdf_countries = gpd.read_file(shapefile_countries)[['ADMIN', 'ADM0_A3', 'geometry']]
gdf_countries.columns = ['country','country_code','geometry']
# Drop row corresponding to 'Antarctica' in gdf_countries
gdf_countries = gdf_countries.drop(gdf_countries.index[159])
# Find numeric index of Antarctica for gdf_states and remove (only works by printing)
print(gdf_states[gdf_states['country'] == 'Antarctica'].index.tolist())
gdf_states = gdf_states.drop(gdf_states.index[1721])
gdf_states = gdf_states.drop(gdf_states.index[2547])


# In[3]:


# Importing wine data

import pandas as pd
import numpy as np

#Read csv file using pandas
datafile_2 = 'C:\\Users\\aslot\\miniconda3\\envs\\winemap\\wine_bottles.csv'
df_bottles = pd.read_csv(datafile_2, names = ['product','vintage','producer','region','country','code','avg_price','critics_score','style','latitude','longitude','img_path','img_link'], skiprows = 1)

# Create a list of country codes in wine collection (hope to make this dynamic, low priority)
country_codes = ['FRA','DEU','ITA','USA',
             'AUS','NZL',
            'ZAF','ESP','ARG','PRT','CHL','GBR']

# Remove countries in country_codes from gdf_countries
gdf_countries = gdf_countries[~gdf_countries['country_code'].isin(country_codes)]
# Remove countries not in country_codes from gdf_states
gdf_states = gdf_states[gdf_states['country_code'].isin(country_codes)]


# Create a list to use to create df_wine_agg (dataframe)
agg_data = []

def aggregate_data(country_code):
    '''
    Append a list of a countries' data to agg_data containing: country_code,
    count, avg price, avg score
    '''
    temp = [country_code]
    count = df_bottles[df_bottles['code'] == country_code]['code'].count()
    avg_price = df_bottles[df_bottles['code'] == country_code]['avg_price'].sum() / count # in $ / 750mL
    avg_score = df_bottles[df_bottles['code'] == country_code]['critics_score'].sum() / count
    # Append data to temp
    temp.extend((count,avg_price,avg_score))
    # Append temp list to global agg_data list
    agg_data.append(temp)

#  Populate list for df
for country_code in country_codes:
    aggregate_data(country_code)

# Create dataframe to potentially merge with gdf for map plot hover function by country data
df_wine_agg = pd.DataFrame(agg_data, columns = ['code','count','avg_price','avg_score'])


# In[4]:


# Get unique list of producers to pull data for prep_producer_df function
producers =  df_bottles['producer'].unique()
agg_data_2 = []

def prep_producer_df(producer):
    '''
    Prepare list of lists for df_producers
    '''
    temp = [producer]
    count = df_bottles[df_bottles['producer'] == producer]['producer'].count()
    region = df_bottles[df_bottles['producer'] == producer]['region'].unique()[0]
    country = df_bottles[df_bottles['producer'] == producer]['country'].unique()[0]
    
    # Exception to avoid errors when count for a country == 0
    try:
        avg_price = df_bottles[df_bottles['producer'] == producer]['avg_price'].sum() / count # in $ / 750mL
        avg_score = df_bottles[df_bottles['producer'] == producer]['critics_score'].sum() / count
    except: 
        avg_price = 0
        avg_score = 0
        
    latitude = df_bottles[df_bottles['producer'] == producer]['latitude'].unique()[0]
    longitude = df_bottles[df_bottles['producer'] == producer]['longitude'].unique()[0]
    
    # Append data to temp
    temp.extend((count,region,country,avg_price,avg_score,latitude,longitude))
    # Append temp list to global agg_data list
    agg_data_2.append(temp)

# Populate list for df    
for producer in producers:
    prep_producer_df(producer)

df_producers = pd.DataFrame(agg_data_2, columns = ['producer','count','region','country','avg_price','avg_score','latitude','longitude'])


# In[5]:


# Merge dataframes gdf_states and gdf_countries
gdf_agg = gdf_states.append(gdf_countries)
# Merge dataframes gdf_agg and df_wine
merged = gdf_agg.merge(df_wine_agg, left_on = 'country_code', right_on = 'code', how = 'left')
#Replace NaN values to string 'No data'.
merged.fillna('No data', inplace = True)


import json

# Read data to json
merged_json = json.loads(merged.to_json())

# Convert to String-like object
json_data = json.dumps(merged_json)


# In[6]:


# Plotting
# Partially modeled on: https://towardsdatascience.com/a-complete-guide-to-an-interactive-geographical-map-using-python-f4c5197e23e0

from bokeh.io import curdoc, output_notebook, show, output_file, export_png
from bokeh.plotting import figure, ColumnDataSource
from bokeh.models import HoverTool, PanTool, WheelZoomTool, GeoJSONDataSource, LinearColorMapper, ColorBar
from bokeh.layouts import widgetbox, row, column
from bokeh.palettes import brewer

#Input GeoJSON source that contains features for plotting.
geosource = GeoJSONDataSource(geojson = json_data)

#Define a sequential multi-hue color palette.
palette = brewer['YlGnBu'][8]

#Reverse color order so that dark blue is highest bottle count.
palette = palette[::-1]

#Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors.
color_mapper = LinearColorMapper(palette = palette, low = 0, high = 16, nan_color = '#d9d9d9')

#Define custom tick labels for color bar.
tick_labels = {'0': '1 Bottle', '2': '2', '4':'4', '6':'6', '8':'8', '10':'10', '12':'12','14':'14', '16':'>16 Bottles'}

# #Add hover tool , sleeping data for hovering over countries and regions
# hover = HoverTool(tooltips = [ ('Country','@country'),('State','@state_name'),('Region','@region_name'),('Number of Bottles in Country', '@count')])

#Create color bar. 
color_bar = ColorBar(color_mapper=color_mapper, label_standoff=8,width = 500, height = 20,
border_line_color=None, location = (0,0), orientation = 'horizontal', major_label_overrides = tick_labels)

#Create figure object.
plot = figure(title = 'Uncorked: Wine/Spirit Collection By Origin', plot_height = 600 , plot_width = 950, toolbar_location = 'right', tools = [PanTool(), WheelZoomTool()])
plot.xgrid.grid_line_color = None
plot.ygrid.grid_line_color = None

#Add patch renderer to figure. 
plot.patches('xs','ys', source = geosource, fill_color = {'field' :'count', 'transform' : color_mapper},
          line_color = 'black', line_width = 0.25, fill_alpha = 1)

# Add source for winery circles
v_source = ColumnDataSource(data=dict(
    longitude = df_producers['longitude'],
    latitude = df_producers['latitude'],
    producer = df_producers['producer'],
    count = df_producers['count'],
    region = df_producers['region'],
    country = df_producers['country'],
    avg_price = df_producers['avg_price'],
    avg_score = df_producers['avg_score']
    ))


vineyard_renderers = []
# Add wineries GPS location as circles
v = plot.circle(x='longitude', y='latitude', size=10, source=v_source, color="red", alpha=0.5)
vineyard_renderers.append(v)

# Add hover tool for wineries
plot.add_tools(HoverTool(
        renderers=vineyard_renderers,
        tooltips=[('Producer','@producer'),
                  ('Count','@count bottle(s)'),
                  ('Region','@region'),
                  ('Country','@country'),
                  ('Avg. Price','$@avg_price / 750mL'),
                  ('Avg. Score','@avg_score / 100')]))

#Specify figure layout.
plot.add_layout(color_bar, 'below')

output_file('winemap.html')

#Display figure inline in Jupyter Notebook.
output_notebook()

#Display figure.
show(plot)


# In[ ]:




