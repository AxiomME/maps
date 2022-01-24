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
def load_data():
	
	data=pd.read_csv('datacountries.csv',sep='\t',index_col=0)
	import geojson
	with open("countries.geojson") as f:
		gj = geojson.load(f)
	
	return data,gj
	
	
def main():	
	
	data,gj=load_data()
	
	fig = px.choropleth(data,                            # Input Dataframe
                     geojson=gj,           # identify country code column
                     color="value",                     # identify representing column
                     #hover_name="country",              # identify hover name
                     animation_frame="variable",# identify date column
                     locations="country",
                     projection="mercator",        # select projection
                     color_continuous_scale = 'Reds',# select prefer color scale
                     featureidkey="properties.ADM0_EN",
                     range_color=[0,300]              # select range of dataset
                     )        
	fig.update_geos(fitbounds="locations", visible=False)
	fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
	st.plotly_chart(fig,use_container_width=True)    
 
if __name__== '__main__':
    main()


