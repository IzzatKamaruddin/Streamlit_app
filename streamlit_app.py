# Data Source: https://public.tableau.com/app/profile/federal.trade.commission/viz/FraudandIDTheftMaps/AllReportsbyState
# US State Boundaries: https://public.opendatasoft.com/explore/dataset/us-state-boundaries/export/

import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

APP_TITLE = 'Mobile Broadband Quarter 4 Report'
APP_SUB_TITLE = 'Source: Ookla Q4'


def display_speed(df):
    year_list = list(df["NAME_1"].unique())
    year_list.sort()
    state = st.sidebar.selectbox("STATE", year_list)
    st.header(f'{state}')
    return state

#def display_state_filter(df, state_name):
 #   state_list = [''] + list(df['NAME_1'].unique())
  #  state_list.sort()
   # state_index = state_list.index(state_name) if state_name and state_name in state_list else 0
    #return st.sidebar.selectbox('State', state_list, state_index)

def display_map(df, state):
    df = df[(df['NAME_1'] == state)]

    m = folium.Map(location=[4.1093195,109.45547499999998], zoom_start=6.5, zoom_to_layer = True, tiles='CartoDB positron')
    
    d = df[df.avg_d_mbps <= 25].set_index("quadkey")
    
    choropleth = folium.Choropleth(
        geo_data=d,
        name='choropleth',
        data=d.avg_d_mbps,
        key_on='feature.id',
        fill_color='YlGn',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Legend',
        highlight=True
    )
    choropleth.geojson.add_to(m)    
    
    df_indexed = df.set_index('NAME_1')
    for feature in choropleth.geojson.data['features']:
            state_name = feature['properties']
            feature['properties']['population'] = 'Average Mbps: ' + '{:,}'.format(df_indexed.loc[state_name, 'avg_d_mbps'][0]) if state_name in list(df_indexed.index) else ''
            feature['properties']['per_100k'] = 'Average u Mbps: ' + str(round(df_indexed.loc[state_name, 'avg_u_mbps'][0])) if state_name in list(df_indexed.index) else ''

    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip([ 'population', 'per_100k'], labels=False)
    )
    
    
    
    st_map = st_folium(m, width=700, height=450)

def main():
    st.set_page_config(APP_TITLE)
    st.title(APP_TITLE)
    st.caption(APP_SUB_TITLE)

    #Load Data
    df_MBB = gp.read_file('data/Malaysia_MBB_Q4_2022.geojson')
    
    
    #Display Filters and Map
    state = display_speed(df_MBB)
    state_name = display_map(df_MBB, state)
    #state_name = display_state_filter(df_MBB, state_name)

    #Display Metrics


if __name__ == "__main__":
    main()