import pandas as pd
import mplleaflet
import folium
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


def create_tables(df):

    totals = {}
    totals = {'TotalDistance': 0, 'TotalTime': 0, 'latlng': {}}
    for index, row in df.iterrows():
        
        distance = row['distance']
        time = row['moving_time']
        

        
        

        totals['TotalDistance'] += distance
        totals['TotalTime'] += time
    df = df[df['summary_polyline'].apply(lambda x: bool(x))]
    coordinates = df['summary_polyline'].tolist()
    totals['latlng'] = coordinates
       
    

    return totals





