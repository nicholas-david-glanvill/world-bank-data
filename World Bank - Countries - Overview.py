#!/usr/bin/env python
# coding: utf-8

# Instructions found here: https://pypi.org/project/world-bank-data/

# In[1]:


pip install world_bank_data


# In[2]:


import pandas as pd
import world_bank_data as wb


# In[3]:


wb.get_countries()


# 
# 
# 
# 
# Exploratory Data Analysis
# 
# Step 1 : head, shape, info, describe
# 
# 
# 

# In[4]:


countries = wb.get_countries()


# In[5]:


countries.head()


# In[7]:


countries.shape


# In[8]:


countries_df.info()


# In[9]:


countries.describe()


# Visualising Maps with Bokeh : https://colab.research.google.com/drive/1G2QGZO78CRMRNTXqcct48pBaSLLLhpK_?usp=sharing#scrollTo=yBR2ompMxjbk

# In[10]:


import pandas as pd
import numpy as np

from bokeh.models import *
from bokeh.plotting import *
from bokeh.io import *
from bokeh.tile_providers import *
from bokeh.palettes import *
from bokeh.transform import *
from bokeh.layouts import *


# #example of importing and cleaning the data
# 
# conflict_df=pd.read_csv('https://raw.githubusercontent.com/ConnerBrew/Iraq-Conflict-Data/master/conflict_data_irq.csv')
# 
# conflict_df=conflict_df.loc[conflict_df['year'] == '2019']
# 
# conflict_df['latitude']=conflict_df['latitude'].astype('float')
# 
# conflict_df['longitude']=conflict_df['longitude'].astype('float')
# 
# conflict_df['fatalities']=conflict_df['fatalities'].astype('int64')
# 
# conflict_df=conflict_df.reset_index()
# 
# conflict_df=conflict_df.drop('index',axis=1)
# 
# 

# In[ ]:


countries = wb.get_countries()

#creating a dataframe 

countries_df= pd.DataFrame(data=countries)

countries_df=countries_df.reset_index() #--> drops original index

countries_df.head()


# In[50]:


#removing null values from longitude and latitude

countries_df = countries_df.dropna(subset=['longitude', 'latitude'])
countries_df.head()


# In[44]:


countries_df.info()


# In[45]:


#checking different categories from "incomeLevel"
countries_df['incomeLevel'].value_counts()


# In[57]:


#Bokeh maps are in mercator. Convert lat lon fields to mercator units for plotting

def convert_to_web_mercator(df, lon, lat):
    """Converts decimal longitude/latitude to Web Mercator format"""
    k = 6378137
    df["x"] = df[lon] * (k * np.pi/180.0)
    df["y"] = np.log(np.tan((90 + df[lat]) * np.pi/360.0)) * k
    return df

df=convert_to_web_mercator(countries_df,'longitude','latitude')

#Establishing a zoom scale for the map. The scale variable will also determine proportions for hexbins and bubble maps so that everything looks visually appealing. 

scale=2000
x=df['x']
y=df['y']

#The range for the map extents is derived from the lat/lon fields. This way the map is automatically centered on the plot elements.

x_min=int(x.mean() - (scale * 350))
x_max=int(x.mean() + (scale * 350))
y_min=int(y.mean() - (scale * 350))
y_max=int(y.mean() + (scale * 350))


#Defining the map tiles to use. I use OSM, but you can also use ESRI images or google street maps.

tile_provider=get_provider(OSM)

output_notebook()


# In[58]:


#Creating a map that will display events categorically by type

p=figure(
    title='World Bank:Countries',
    match_aspect=True,
    tools='wheel_zoom,pan,reset,save',
    x_range=(x_min, x_max),
    y_range=(y_min, y_max),
    x_axis_type='mercator',
    y_axis_type='mercator',
    width=500)

p.grid.visible=True

m=p.add_tile(tile_provider)
m.level='underlay'

p.xaxis.visible = False
p.yaxis.visible=False
p.title.text_font_size="20px"

output_notebook()


# In[52]:


countries_df.head()


# In[68]:


#Initializing empty lists to create temporary dataframes for each category

High_income=[]
Upper_middle_income=[]
Lower_middle_income=[]
Low_income=[]

list_list=[High_income,Upper_middle_income,Lower_middle_income,Low_income]


#Extracting event information for each category. I opted not to use nested iterators here to enhance code readability - a more efficient method woudld be to use a nested for loop with 'for iterate1,iterate2 in zip (event_type_name,list_name)

for i in range(len(countries_df['incomeLevel'])):
  if countries_df.loc[i,'incomeLevel']=='High income':
    High_income.append([countries_df.loc[i,'incomeLevel'],
                        countries_df.loc[i,'name'],
                        countries_df.loc[i,'x'],
                        countries_df.loc[i,'y'],
                        countries_df.loc[i,'lendingType'],
                        countries_df.loc[i,'latitude'],
                        countries_df.loc[i,'longitude']])

for i in range(len(countries_df['incomeLevel'])):
  if countries_df.loc[i,'incomeLevel']=='Upper middle income':
    Upper_middle_income.append([countries_df.loc[i,'incomeLevel'],
                        countries_df.loc[i,'name'],
                        countries_df.loc[i,'x'],
                        countries_df.loc[i,'y'],
                        countries_df.loc[i,'lendingType'],
                        countries_df.loc[i,'latitude'],
                        countries_df.loc[i,'longitude']])

for i in range(len(countries_df['incomeLevel'])):
  if countries_df.loc[i,'incomeLevel']=='Lower middle income':
    Lower_middle_income.append([countries_df.loc[i,'incomeLevel'],
                        countries_df.loc[i,'name'],
                        countries_df.loc[i,'x'],
                        countries_df.loc[i,'y'],
                        countries_df.loc[i,'lendingType'],
                        countries_df.loc[i,'latitude'],
                        countries_df.loc[i,'longitude']])

for i in range(len(countries_df['incomeLevel'])):
  if countries_df.loc[i,'incomeLevel']=='Low income':
    Low_income.append([countries_df.loc[i,'incomeLevel'],
                        countries_df.loc[i,'name'],
                        countries_df.loc[i,'x'],
                        countries_df.loc[i,'y'],
                        countries_df.loc[i,'lendingType'],
                        countries_df.loc[i,'latitude'],
                        countries_df.loc[i,'longitude']])
    
    
 #using the list of lists, create temporary dataframes for each event category and plot them to our second map.

for i in range(len(list_list)):
  temp_df=pd.DataFrame(list_list[i],columns=['incomeLevel','name','x','y','lendingType','latitude','longitude'])
  source=ColumnDataSource(temp_df)

  circle=p.circle(x='x',y='y',source=source,color=Spectral6[i],line_color=Spectral6[i],legend_label=events[i],hover_color='white',radius=15000,fill_alpha=0.4)

  event_hover = HoverTool(tooltips=[('Country','@name'),
                                    ('Income_Level','incomeLevel'),
                                    ('Lending_Type','@lendingType'),
                                    ('(Lat,Lon)','(@latitude,@longitude)')],
                          mode='mouse',
                          point_policy='follow_mouse',
                          renderers=[circle])
  
  event_hover.renderers.append(circle)
  p.tools.append(event_hover)

#View our maps

p.legend.location = "top_right"
p.legend.click_policy="hide"

show(p)   
    


# In[ ]:





# In[ ]:




