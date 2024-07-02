import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import geopandas as gpd
from shapely.geometry import Point
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from zipfile import ZipFile
from bs4 import BeautifulSoup
import math 




def data_parser(file):
    df = pd.read_csv(file)
    time_list = df.iloc[:, 0].tolist()
    type_list = df.iloc[:, 1].tolist()
    lat_list = df.iloc[:, 2].tolist()
    long_list = df.iloc[:, 3].tolist()
    pc_list = df.iloc[:, 4].tolist()
    ic_list = df.iloc[:, 5].tolist()
    station_list = df.iloc[:, 6].tolist()
    
    return [time_list,type_list,lat_list,long_list,pc_list,ic_list,station_list]

def plotter(file,start_date,end_date):
    
    fig, ax = plt.subplots(figsize=(15, 15), subplot_kw={'projection': ccrs.PlateCarree()})
    
    ax.set_extent([-136, -114, 48.3, 60.5], crs=ccrs.PlateCarree())
        
    bc_gdf = gpd.read_file('~/Downloads/bc_boundary_terrestrial_multipart.shp')
    bc_gdf = bc_gdf.to_crs(epsg=4326)
    bc_gdf.boundary.plot(ax=ax,edgecolor='black')
    
    shapefile_path = '~/Downloads/prot_current_fire_points_202310241608/prot_current_fire_points.shp'
    fires_gdf = gpd.read_file(shapefile_path)
    fires_gdf = fires_gdf.to_crs(epsg=4326)
    filtered_fires_gdf = fires_gdf[(fires_gdf['FIRE_CAUSE'] == 'Lightning') &
                        (fires_gdf['IGNITN_DT'] <= end_date) &
                        (fires_gdf['IGNITN_DT'] >= start_date)]
    
    # Plot the shapefile
    filtered_fires_gdf.plot(ax=ax,marker='s', color='orange', markersize=5,label=f'LCFs: {len(filtered_fires_gdf)}')

    # Add gridlines
    ax.gridlines(draw_labels=False)
    
    data = data_parser(file)
    time = data[0]
    lat = data[2]
    long = data[3]
    charge = data[4]
    strikes = []
    charges = []
    for i in range(len(time)):
        if datetime.strptime(start_date, '%Y-%m-%d') <  datetime.strptime(time[i][0:-3], "%Y-%m-%dT%H:%M:%S.%f") < datetime.strptime(end_date, '%Y-%m-%d'):
            strikes.append(Point(long[i],lat[i]))
            charges.append((long[i],lat[i],charge[i]))
            
        elif datetime.strptime(time[i][0:-3], "%Y-%m-%dT%H:%M:%S.%f") > datetime.strptime(end_date, '%Y-%m-%d'):
            break;
        
    
    # Create a GeoDataFrame from the points
    
    strikes_gdf = gpd.GeoDataFrame(geometry=strikes, crs='EPSG:4326')

    # Ensure both GeoDataFrames use the same coordinate reference system (CRS)
    strikes_gdf.set_crs('EPSG:4326', inplace=True)
 
    # Perform a spatial join to find points within the BC polygon
    strikes_within_bc = gpd.sjoin(strikes_gdf, bc_gdf, how='inner',predicate='intersects')

    filtered_strikes = [(point.x, point.y) for point in strikes_within_bc.geometry]
    
    positive = 0
    negative = 0
    for i in range(len(filtered_strikes)):
        for charge in charges:
            if charge[0:2] == filtered_strikes[i]:
                charge = charge[2]
                break;
        size = int(abs(charge/10000))
        if charge < 0:
            negative += 1
            ax.plot(filtered_strikes[i][0], filtered_strikes[i][1], marker='o', markersize=size, color='blue', transform=ccrs.PlateCarree())
        else:
            positive += 1
            ax.plot(filtered_strikes[i][0], filtered_strikes[i][1], marker='o', markersize=size, color='red', transform=ccrs.PlateCarree())
        
        percent = i/len(filtered_strikes)
        if int(percent) // 10 == 0:
            print(f'{percent}%')

    ax.scatter(np.nan,np.nan, marker='o', s=10, color='blue', label=f'negative strikes: {negative}')
    ax.scatter(np.nan,np.nan, marker='o', s=10, color='red', label=f'positive strike: {positive}')
    
    # Add a title
    plt.title(f'Lighting strikes and LCFs in range: {start_date} - {end_date}')
    plt.legend()

    # Show the plot
    plt.savefig(f'strikes_LCFs_{start_date}_{end_date}.png')
    plt.clf()

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the Earth's surface given their latitude and longitude 
    in degrees.
    """
    # Convert latitude and longitude from degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    # Haversine formula
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = 6371 * c  # Radius of Earth in kilometers
    
    return distance

