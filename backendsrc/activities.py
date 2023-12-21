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
import random


def create_tables(df):

    totals = {}
    maxdist = 0
    totals = {'TotalDistance': 0, 'TotalTime': 0, 'latlng': {}, 'number_act': 0, 'kudos_count': 0, 'maxdist': 0}
    for index, row in df.iterrows():
        
        distance = row['distance']
        time = row['moving_time']
        kudos_count = row['kudos_count']
        if distance>maxdist:
            maxdist=distance

        
        

        totals['TotalDistance'] += distance
        totals['TotalTime'] += time
        totals['kudos_count'] += kudos_count
        totals['number_act'] += 1
    totals['TotalDistance'] = totals['TotalDistance']//1609
    totals['TotalTime'] = totals['TotalTime']//3600
    totals['maxdist'] = maxdist//1609
    df = df[df['summary_polyline'].apply(lambda x: bool(x))]
    coordinates = df['summary_polyline'].tolist()
    totals['latlng'] = coordinates
       
    

    return totals

def generate_accent_color():
    """Generate a random accent color."""
    accent_colors = [
        (0.8, 0.2, 0.2),  # Red
        (0.2, 0.8, 0.2),  # Green
        (0.2, 0.2, 0.8),  # Blue
        (0.8, 0.8, 0.2),  # Yellow
        (0.8, 0.2, 0.8),  # Magenta
        (0.2, 0.8, 0.8),  # Cyan
    ]
    return (1, 1, 1)
    #return random.choice(accent_colors)

def calculate_complement_color(color):
    """Calculate the complement color for an RGB color."""
    r, g, b = color
    #return (256,236, 226)
    
    return (0.06666666666666667, 0.31, 0.67)
    #return (1.0 - r, 1.0 - g, 1.0 - b)

def create_plot(polylines):
    polylines = polylines
    num_polylines = len(polylines)
    num_cols = int(num_polylines**0.5)
    num_rows = (num_polylines + num_cols - 1) // num_cols

    # Create a grid of subplots
    fig, axs = plt.subplots(num_rows, num_cols, figsize=(15, 17), facecolor='none')
    axs = axs.flatten()  # Flatten the 2D array of subplots

    # Plot each polyline in a subplot
    for i, polyline_str in enumerate(polylines):
        try:
            decoded_polyline = polyline.decode(polyline_str)
            lats, lons = zip(*decoded_polyline)

            # Generate a random accent color
            accent_color = generate_accent_color()
            complement_color = calculate_complement_color(accent_color)

            axs[i].plot(lons, lats, color=accent_color, linewidth=2)
            axs[i].set_facecolor((*complement_color, 1.0))  # Set alpha to 1.0 for full opacity
            axs[i].set_xticks([])
            axs[i].set_yticks([])
            axs[i].grid(False)
            #axs[i].set_aspect('equal')
            axs[i].axis('on')
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