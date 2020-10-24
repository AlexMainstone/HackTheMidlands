#!/usr/bin/env python
# coding: utf-8

# In[146]:


# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 10:52:55 2020

@author: Tea
"""
import pandas as pd
import os
import json
import folium
import json # or import geojson

#url = 'https://coronavirus.data.gov.uk/downloads/csv/coronavirus-cases_latest.csv'
#r = requests.get(url, allow_redirects=True)
#open('all_covid.csv', 'wb').write(r.content)


colsuse = [0,3,4,5]
nameuse = ['location','date','conf_cases','rate']


file1 = pd.read_csv("all_covid.csv",skiprows = 1,usecols = colsuse, names = nameuse)
dataframe = pd.DataFrame(file1)
loc = dataframe['location']
dates = dataframe['date']


# In[147]:


def get_loc(place):

    indx = [i for i, x in enumerate(loc) if x == place]
    dates_loc = dates[indx[0]:indx[-1]]
    return indx,dates_loc


# In[148]:


last_day = '2020-10-21'
indx_dates = [i for i, x in enumerate(dates) if x == last_day]

newdataframe = dataframe.iloc[indx_dates]
single_loc = list(newdataframe['location'])
rates = list(newdataframe['rate'])


# In[149]:


from branca.utilities import split_six
import geopandas as gpd
#state_geo = 'https://opendata.arcgis.com/datasets/3a4667c2e625435ba427ae95a438724f_0.geojson'
state_geo = 'https://opendata.arcgis.com/datasets/ae90afc385c04d869bc8cf8890bd1bcd_3.geojson'
file_geo = gpd.read_file(state_geo)


# In[150]:


newgeofile = file_geo[['objectid','lad17nm','long','lat','st_areashape','st_lengthshape','geometry']]


# In[151]:


localaut = list(newgeofile['lad17nm'])
indxaut = list(newgeofile['objectid'])

indexnew = []
rates_geo = []
for i in range(len(localaut)):
    for j in range(len(single_loc)):
        if localaut[i] == single_loc[j]:
            rates_geo.append(rates[j])
            indexnew.append(i)
            break
        


# In[152]:


print(len(rates_geo))


# In[153]:


import numpy as np
usegeo = newgeofile.iloc[indexnew]
usegeo['rates'] = rates_geo


# In[154]:



#state_geo = 'https://martinjc.github.io/UK-GeoJSON/json/eng/topo_lad.json'
#print(state_geo)
myscale = (usegeo['rates'].quantile((0,0.1,0.75,0.9,0.98,1))).tolist()
m = folium.Map(location=[55, 1.5], zoom_start=5.5)
m.choropleth(
    geo_data=state_geo,
    data=usegeo,
    columns=['objectid', 'rates'],
    key_on='feature.properties.objectid',
    fill_color='YlGnBu',
    threshold_scale=myscale,
    fill_opacity=0.5,
    line_opacity=0.9,
    legend_name='Infection Rate',
    highlight=True)
display(m)

