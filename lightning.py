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
from misc import err



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
        
    bc_gdf = gpd.read_file('~/wxps-lx-compare/shape_files/bc_boundary_terrestrial_multipart.shp')
    bc_gdf = bc_gdf.to_crs(epsg=4326)
    bc_gdf.boundary.plot(ax=ax,edgecolor='black')
    
    shapefile_path = '~/wxps-lx-compare/shape_files/prot_current_fire_points.shp'
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
    distance = 6371 * c * 1000  # Radius of Earth in kilometers
    
    return distance

def comp(data1_file,data2_file,zone):
    '''
    Compares two lighting strike data sets based on their fire zone, can chose one of the 6 fire centers in BC
    NW == Northwest Fire Center
    COAST == Costal Fire Center
    CARIBOO == Cariboo Fire Center
    KAM == Kamloops Fire Center
    PG == Prince George Fire Center
    SE == Southeast Fire Center
    '''
    aem = data_parser(data1_file) #extracting data from csv files
    cldn = data_parser(data2_file)
    
    fire_point_path = '~/wxps-lx-compare/shape_files/prot_current_fire_points.shp' #extracting LCFs from shape file
    fires_gdf = gpd.read_file(fire_point_path)
    fires_gdf = fires_gdf.to_crs(epsg=4326)
    filtered_fires_gdf = fires_gdf[fires_gdf['FIRE_CAUSE'] == 'Lightning']
    
    nw_zone_path = ''
    coast_zone_path = ''
    cari_zone_path = ''
    kam_zone_path = ''
    pg_zone_path = ''
    se_zone_path = ''

    #chosing fire zone
    if zone == 'NW': 
        zone_gdf = gpd.read_file(nw_zone_path)
    elif zone == 'COAST':
        zone_gdf = gpd.read_file(coast_zone_path)
    elif zone == 'CARIBOO':
        zone_gdf = gpd.read_file(cari_zone_path)
    elif zone == 'KAM':
        zone_gdf = gpd.read_file(kam_zone_path)
    elif zone == 'PG':
        zone_gdf = gpd.read_file(pg_zone_path)
    elif zone == 'SE':
        zone_gdf = gpd.read_file(se_zone_path)
    else:
        err('Invalid zone')
    
    #filtering fires in zone    
    zone_gdf = zone_gdf.to_crs(epsg=4326)
    zone_fires_gdf = gpd.sjoin(filtered_fires_gdf, zone_gdf, how='inner',predicate='intersects')
    #filtered_fires = [(point.x, point.y) for point in zone_fires_gdf.geometry]
    
    #calculating strike distance from fire start if strike distance < 5000 meters
    aem_strikes = []
    cldn_strikes = []
    aem_dist = []
    cldn_dist = []
    aem_miss = 0
    cldn_miss = 0
    max_radius = 5000
    for fire in range(len(zone_fires_gdf)):
        end_date = zone_fires_gdf.IGNITN_DT.to_list()[fire]
        start_date = end_date - timedelta(weeks=3)
        coord = zone_fires_gdf.geometry.to_list()[fire]
        lat = coord.x
        long = coord.y
        small_dist_aem = max_radius
        small_dist_cldn = max_radius
        
        date_objects_aem = [datetime.strptime(date[0:-3], "%Y-%m-%dT%H:%M:%S.%f") for date in aem[0]]
        date_objects_cldn = [datetime.strptime(date[0:-3], "%Y-%m-%dT%H:%M:%S.%f") for date in cldn[0]]
        start_index1 = next(i for i, date in enumerate(date_objects_aem) if date >= start_date)
        end_index1 = next(i for i, date in enumerate(date_objects_aem) if date > end_date)
        start_index2 = next(i for i, date in enumerate(date_objects_cldn) if date >= start_date)
        end_index2 = next(i for i, date in enumerate(date_objects_cldn) if date > end_date)
        
        aem_strikes_gdf = gpd.GeoDataFrame(geometry=((Point(aem[2][i],aem[3][i])) for i in range(start_index1,end_index1)), crs='EPSG:4326')
        cldn_strikes_gdf = gpd.GeoDataFrame(geometry=((Point(cldn[2][i],cldn[3][i])) for i in range(start_index2,end_index2)), crs='EPSG:4326')
        zone_aem =  gpd.sjoin(aem_strikes_gdf, zone_gdf, how='inner',predicate='intersects')
        zone_cldn =  gpd.sjoin(cldn_strikes_gdf, zone_gdf, how='inner',predicate='intersects')
        zone_aem_list = [(point.x, point.y) for point in zone_aem.geometry]
        zone_cldn_list = [(point.x, point.y) for point in zone_cldn.geometry]
        
        for strike in zone_aem_list:
            dist = haversine(lat, long, strike[0], strike[1])
            if dist < small_dist_aem:
                strike_loc = strike
                small_dist_aem = dist
        if small_dist_aem != max_radius:
            aem_strikes.append(strike_loc)
            aem_dist.append(small_dist_aem)
        else:
            aem_miss += 1
            
        for strike in zone_cldn_list:
            dist = haversine(lat, long, strike[0], strike[1])
            if dist < small_dist_cldn:
                strike_loc = strike
                small_dist_cldn = dist
        if small_dist_cldn != max_radius:
            cldn_strikes.append(strike_loc)
            cldn_dist.append(small_dist_cldn)
        else:
            cldn_miss += 1