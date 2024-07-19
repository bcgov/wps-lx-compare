import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import geopandas as gpd
from shapely.geometry import Point, shape
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from zipfile import ZipFile
from bs4 import BeautifulSoup
import math 
from misc import err
from osgeo import ogr
import os



def data_parser_aem(file):
    df = pd.read_csv(file)
    time_list = df.iloc[:, 0].tolist()
    type_list = df.iloc[:, 1].tolist()
    lat_list = df.iloc[:, 2].tolist()
    long_list = df.iloc[:, 3].tolist()
    pc_list = df.iloc[:, 4].tolist()
    ic_list = df.iloc[:, 5].tolist()
    station_list = df.iloc[:, 6].tolist()
    
    return [time_list,type_list,lat_list,long_list,pc_list,ic_list,station_list]

def data_parser_cldn(file):
    df = pd.read_csv(file)
    time_list = df.iloc[:, 7].tolist()
    polarity_list = df.iloc[:, 4].tolist()
    lat_list = df.iloc[:, 2].tolist()
    long_list = df.iloc[:, 3].tolist()
    charge_list = df.iloc[:,6].tolist()
    
    return [time_list,charge_list,lat_list,long_list,polarity_list]

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
    
    data = data_parser_aem(file)
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
    distance = 6371 * c * 1000  # Radius of Earth in meters
    
    return distance

def filter_points_by_shapefile_and_date(shapefile_path, points_with_dates):
    """
    Filter a list of points with dates to keep only those that lie within a given shapefile.

    Parameters:
    - shapefile_path (str): Path to the shapefile.
    - points_with_dates (list of tuples): List of (longitude, latitude, date) tuples representing points.

    Returns:
    - filtered_points (list of tuples): List of points that lie within the shapefile.
    """
    # Open the shapefile
    driver = ogr.GetDriverByName('ESRI Shapefile')
    dataset = driver.Open(shapefile_path)
    if dataset is None:
        raise IOError(f"Unable to open shapefile at {shapefile_path}")
    
    # Get the layer from the dataset
    layer = dataset.GetLayer()
    
    # Prepare a list to store filtered points
    filtered_points = []

    # Iterate over each point with date
    for lon, lat, date in points_with_dates:
        point_geom = Point(lon, lat)

        # Flag to check if point is within any feature
        is_within = False
        
        # Iterate over each feature in the layer
        for feature in layer:
            geom = feature.GetGeometryRef()
            if geom:
                shp_geom = shape(geom)
                if point_geom.within(shp_geom):
                    is_within = True
                    break
        
        # If point is within any feature, add it to filtered points
        if is_within:
            filtered_points.append((lon, lat, date))

        # Reset the feature reading to start from the beginning
        layer.ResetReading()

    # Close the dataset
    dataset = None

    return filtered_points


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
    aem = data_parser_aem(data1_file) #extracting data from csv files
    cldn = data_parser_cldn(data2_file)
    fire_point_path = '~/Documents/wps-lx-compare/shape_files/prot_current_fire_points.shp' #extracting LCFs from shape file
    fires_gdf = gpd.read_file(fire_point_path)
    fires_gdf = fires_gdf.to_crs(epsg=4326)
    filtered_fires_gdf = fires_gdf[fires_gdf['FIRE_CAUSE'] == 'Lightning'] #extracting lighting caused fires
    
    nw_zone_path = '~/Documents/wps-lx-compare/shape_files/nw_fc.shp'
    coast_zone_path = '~/Documents/wps-lx-compare/shape_files/coast_fc.shp'
    cari_zone_path = '~/Documents/wps-lx-compare/shape_files/cariboo_fc.shp'
    kam_zone_path = '~/Documents/wps-lx-compare/shape_files/kam_fc.shp'
    pg_zone_path = '~/Documents/wps-lx-compare/shape_files/pg_fc.shp'
    se_zone_path = '~/Documents/wps-lx-compare/shape_files/se_fc.shp'
    
    #choosing a fire centers shape file
    if zone == 'NW': 
        zone_path = nw_zone_path
    elif zone == 'COAST':
        zone_path = coast_zone_path
    elif zone == 'CARIBOO':
        zone_path = cari_zone_path
    elif zone == 'KAM':
        zone_path = kam_zone_path
    elif zone == 'PG':
        zone_path = pg_zone_path
    elif zone == 'SE':
        zone_path = se_zone_path
    else:
        err('Invalid zone')
    
    #trimming fires outside selected fire center perimeter 
    zone_gdf = gpd.read_file(zone_path)
    zone_gdf = zone_gdf.to_crs(epsg=4326)
    zone_gdf.sindex
    zone_fires_gdf = gpd.sjoin(filtered_fires_gdf, zone_gdf, how='inner',predicate='intersects')
    filtered_fires = [(point.x, point.y) for point in zone_fires_gdf.geometry] #writing fire locations to a list
    fire_dates = [datetime.strptime(date, '%Y-%m-%d').date() for date in zone_fires_gdf.IGNITN_DT] #writing ignition time to a list
    
    #making strike lists with dates    
    aem_points = [(aem[3][i],aem[2][i],aem[0][i]) for i in range(len(aem[0]))]
    cldn_points = [(cldn[3][i],cldn[2][i],cldn[0][i]) for i in range(len(cldn[0]))]
    
    #trimming AEM and CLDN data to the fire center perimeter
    print('start AEM trim')
    aem_points = []
    aem_dates = []
    
    #remove cloud-to-cloud strikes
    for i in range(len(aem[0])):
        if aem[1][i] == 0:
            aem_points.append(Point(aem[3][i],aem[2][i]))
            aem_dates.append(aem[0][i])
        else:
            continue;
    aem_gdf = gpd.GeoDataFrame({'geometry': aem_points, 'date': aem_dates}, crs='EPSG:4326')
    aem_filtered = gpd.sjoin(aem_gdf, zone_gdf,how='inner',predicate='intersects')
    aem_filtered_points = [(point.x, point.y) for point in aem_filtered.geometry]
    aem_filtered_dates = [datetime.strptime(date[0:-3], "%Y-%m-%dT%H:%M:%S.%f").date() for date in aem_filtered.date]
    print('done AEM trim')
    
    print('start CLDN trim')
    cldn_points = [Point(cldn[3][i],cldn[2][i]) for i in range(len(cldn[0]))]
    cldn_gdf = gpd.GeoDataFrame({'geometry': cldn_points, 'date': cldn[0]}, crs='EPSG:4326')
    cldn_filtered = gpd.sjoin(cldn_gdf, zone_gdf,how='inner',predicate='intersects')
    cldn_filtered_points = [(point.x, point.y) for point in cldn_filtered.geometry]
    cldn_filtered_dates = [datetime.strptime(date.split('+')[0], "%Y/%m/%d %H:%M:%S").date() for date in cldn_filtered.date]
    print('done CLDN trim')
    
    #calculating strike distance from fire start if strike distance < 5000 meters
    aem_strikes = []
    cldn_strikes = []
    aem_dist = []
    cldn_dist = []
    aem_miss = 0
    cldn_miss = 0
    max_radius = 5000
    both_det = []
    aem_det = []
    cldn_det = []
    cldn_det = []
    both_miss = []
    for fire in range(len(filtered_fires)): #searching through fire points in fire center perimeter
        end_date = fire_dates[fire] #fire start date, end date fore lightning search
        start_date = end_date - timedelta(weeks=3) #only taking strikes that took place within 3 weeks prior to ignition date
        lat = filtered_fires[fire][1]
        long = filtered_fires[fire][0]
        smallest_dist_aem = max_radius
        small_dist_cldn = max_radius

        #Checks strike distance from lightning caused fire (LCF) for AEM data and keeps smallest distance
        for strike in range(len(aem_filtered_points)): 
            dist = haversine(lat, long, aem_filtered_points[strike][1], aem_filtered_points[strike][0])
            date =  aem_filtered_dates[strike]
            if dist < smallest_dist_aem and start_date <= date <= end_date:
                smallest_dist_aem = dist
            elif date > end_date: #breaks if the strike date goes past ignition date
                break;
            
        #Only takes stikes within 5000 meters      
        if smallest_dist_aem != max_radius:
            aem_dist.append(smallest_dist_aem)
        else:
            aem_miss += 1
            
        #Checks strike distance from lightning caused fire (LCF) for CLDN data and keeps smallest distance
        for strike in range(len(cldn_filtered_points)): 
            dist = haversine(lat, long, cldn_filtered_points[strike][1], cldn_filtered_points[strike][0])
            date =  cldn_filtered_dates[strike]
            if dist < small_dist_cldn and start_date <= date <= end_date:
                small_dist_cldn = dist
            elif date > end_date:
                break;
                 
        if small_dist_cldn != max_radius:
            cldn_dist.append(small_dist_cldn)
        else:
            cldn_miss += 1
            
        #Sorts LCFs into 4 catagories: both sensors detected a strike, only AEM detected, only CLDN detected, both sensors did not detect
        if smallest_dist_aem != max_radius and small_dist_cldn != max_radius:
            both_det.append((long,lat)) #lat and long of the LCF
            
        elif smallest_dist_aem != max_radius and small_dist_cldn == max_radius:
            aem_det.append((long,lat))
        
        elif smallest_dist_aem == max_radius and small_dist_cldn != max_radius:
            cldn_det.append((long,lat))
        
        else:
            both_miss.append((long,lat))
        
        #progress meter
        percent = round((fire/len(filtered_fires))*100,0)
        if int(percent) % 5 == 0:
            print(f'{int(percent)}%' )

    #plotting histograms of distances of accepted stikes for all fire in given fire center
    plt.figure(figsize=(15,15))
    plt.hist(aem_dist, alpha=0.5, bins=np.linspace(0, 5000, 51), edgecolor='black', label=f'AEM, strikes detected: {len(aem_filtered_points)}, average dist: {round(np.mean(aem_dist),1)} +/- {round(np.std(aem_dist),1)} m, missed: {aem_miss} LCFs')
    plt.hist(cldn_dist, alpha=0.3,bins=np.linspace(0, 5000, 51), edgecolor='black', label=f'CLDN, strikes detected: {len(cldn_filtered_points)}, average dist: {round(np.mean(cldn_dist),1)} +/- {round(np.std(cldn_dist),1)} m, missed: {cldn_miss} LCFs')
    plt.xlabel('Distance from LCF (m)', fontsize=14)
    plt.ylabel('# of strikes', fontsize=14)
    plt.title(f'Strike counts within 5km and 3 weeks of LCF ignition, AEM vs CLDN, fire center: {zone}, # of LCFs: {len(filtered_fires)}',fontsize=18)
    plt.legend(fontsize=14)
    plt.tight_layout()
    plt.savefig(f'{zone}_strike_data.png')
    plt.clf()
    return [both_det, aem_det, cldn_det, both_miss, aem_dist, cldn_dist, aem_miss, cldn_miss]
    