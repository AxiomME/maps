import pandas as pd
import json
import geopandas as geo
import geojson
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import datetime
import plotly.express as px


st.set_page_config(layout="wide")

#import des données
def load_data(level,event_list):
	
	data=pd.read_csv('data_incidents.csv',sep='\t',index_col=0)
	
	
	if len(event_list)>0:
		#st.write('coucou')
		data=data[data['event_type'].isin(event_list)]
	
	#st.write(data)
	data=data[['event_date',level,'iso3']]
	
	a=data.groupby(by=[level,'iso3','event_date']).aggregate({'iso3':'count'}).unstack()
	a.reset_index(inplace=True)
	a.columns=[a.columns.tolist()[0][0],a.columns.tolist()[1][0]]+[i[1] for i in a.columns.tolist()[2:]]
	df_long = pd.melt(a, id_vars=[level,'iso3'], value_vars=a.columns.tolist()[2:])
	df_long.fillna(0,inplace=True)
	
	if level=='admin2':
		with open("districts_som.geojson") as f:
			gj = geojson.load(f)
		df_long=df_long[df_long['iso3']=='SOM']
	elif level=='admin1':
		with open("regions_som.geojson") as f:
			gj = geojson.load(f)
		df_long=df_long[df_long['iso3']=='SOM']
	else:
		with open("countries.geojson") as f:
			gj = geojson.load(f)
		
	return df_long,gj
	
	
def main():	
	
	event_list = st.multiselect('The type of events you want to visualize: (For all do not select any)', ['Battles', 'Protests', 'Strategic developments',\
       'Violence against civilians', 'Explosions/Remote violence','Riots'])
	details = st.radio('Select the level of details (Region and District only for Somalia):', ['Country', 'Region', 'District'])
	dico={'Country':'country', 'Region':'admin1', 'District':'admin2'}
	level=dico[details]
	feature_id_dico={'Country':'properties.ADM0_EN', 'Region':'properties.ADM1_EN', 'District':'properties.ADM2_EN'}
	
	#st.write(event_list)
	st.title('Number of security incident per month over the last 3 years')
	data,gj=load_data(level,event_list)
	#st.write(data)
	#st.write(data['value'].max())
	
	
	
	
	fig = px.choropleth(data,                            # Input Dataframe
                     geojson=gj,           # identify country code column
                     color="value",                     # identify representing column
                     #hover_name="country",              # identify hover name
                     animation_frame="variable",# identify date column
                     locations=level,
                     projection="mercator",        # select projection
                     color_continuous_scale = 'Reds',# select prefer color scale
                     featureidkey=feature_id_dico[details],
                     range_color=[0,data['value'].max()/2]              # select range of dataset
                     )        
	fig.update_geos(fitbounds="locations", visible=False)
	fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
	st.plotly_chart(fig,use_container_width=True)    
 
if __name__== '__main__':
    main()


