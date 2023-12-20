import pandas as pd
import base64
from io import BytesIO
import mplleaflet
import folium
from matplotlib.ticker import MaxNLocator
import polyline
from polyline import decode
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec


def create_tables(df):

    totals = {}
    totals = {'TotalDistance': 0, 'TotalTime': 0, 'latlng': {}}
    for index, row in df.iterrows():
        
        distance = row['distance']
        time = row['moving_time']
        

        
        

        totals['TotalDistance'] += distance
        totals['TotalTime'] += time
    totals['TotalDistance'] = totals['TotalDistance']//1609
    df = df[df['summary_polyline'].apply(lambda x: bool(x))]
    coordinates = df['summary_polyline'].tolist()
    totals['latlng'] = coordinates
       
    

    return totals

def create_plot(polylines):
    polylines = polylines
    num_polylines = len(polylines)
    num_cols = int(num_polylines**0.5)
    num_rows = (num_polylines + num_cols - 1) // num_cols

    # Create a grid of subplots
    fig, axs = plt.subplots(num_rows, num_cols, figsize=(10, 15), facecolor='none')
    axs = axs.flatten()  # Flatten the 2D array of subplots

    # Plot each polyline in a subplot

    for i, polyline_str in enumerate(polylines):
        try:
  
            decoded_polyline = polyline.decode(polyline_str)
            lats, lons = zip(*decoded_polyline)

            axs[i].plot(lons, lats, color='blue', linewidth=2)
            #axs[i].set_title(f'Polyline {i+1}')
            axs[i].set_xticks([])
            axs[i].set_yticks([])
            axs[i].grid(False)
            axs[i].set_aspect('equal')
            axs[i].axis('off')
        except Exception as e:
            print(f"Error decoding polyline {i+1}: {str(e)}")
            continue
    plt.subplots_adjust(wspace=.05, hspace=.05)
    

    # Remove empty subplots (if any)
    for j in range(i+1, len(axs)):
        fig.delaxes(axs[j])

    buffer = BytesIO()
    # Adjust layout
    plt.tight_layout()

    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Convert the plot to a base64-encoded string
    plot_data = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()
    return plot_data





