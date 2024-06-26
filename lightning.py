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

def plotter(file):
    '''
    fig, ax = plt.subplots(figsize=(15, 15), subplot_kw={'projection': ccrs.PlateCarree()})
    
    ax.set_extent([-135, -114, 48.3, 60], crs=ccrs.PlateCarree())
    ax.plot(np.nan,np.nan, 'ro', markersize=3, color='blue', label='negative strike')
    ax.plot(np.nan,np.nan, 'ro', markersize=3, color='red', label='positive strike')
    
    bc_gdf = gpd.read_file('~/Downloads/bc_boundary_terrestrial_multipart.shp')
    bc_gdf = bc_gdf.to_crs(epsg=4326)
    bc_gdf.boundary.plot(ax=ax,edgecolor='black')
    
    shapefile_path = '~/Downloads/prot_current_fire_points_202310241608/prot_current_fire_points.shp'
    gdf = gpd.read_file(shapefile_path)
    gdf = gdf.to_crs(epsg=4326)
    filtered_gdf = gdf[gdf['FIRE_CAUSE'] == 'Lightning']
    
    # Plot the shapefile
    filtered_gdf.plot(ax=ax,marker='s', color='orange', markersize=5,label='LCFs')

    # Add gridlines
    ax.gridlines(draw_labels=True)
    '''
    data = data_parser(file)
    time = data[0]
    lat = data[2]
    long = data[3]
    charge = data[4]
    n = 0
    
    while n <= len(long):
        end_date = datetime.strptime(time[n][:-3], "%Y-%m-%dT%H:%M:%S.%f") + timedelta(weeks=2)
        points = []
        while datetime.strptime(time[n][:-3], "%Y-%m-%dT%H:%M:%S.%f") <= end_date:
            points.append(Point(long[n],lat[n]))
            n += 1
        
        fig, ax = plt.subplots(figsize=(15, 15), subplot_kw={'projection': ccrs.PlateCarree()})
    
        ax.set_extent([-135, -114, 48.3, 60], crs=ccrs.PlateCarree())
        #ax.plot(np.nan,np.nan, 'ro', markersize=3, color='blue', label='negative strike')
        ax.plot(np.nan,np.nan, 'ro', markersize=3, color='red', label='positive strike')
    
        bc_gdf = gpd.read_file('~/Downloads/bc_boundary_terrestrial_multipart.shp')
        bc_gdf = bc_gdf.to_crs(epsg=4326)
        bc_gdf.boundary.plot(ax=ax,edgecolor='black')
    
        shapefile_path = '~/Downloads/prot_current_fire_points_202310241608/prot_current_fire_points.shp'
        gdf = gpd.read_file(shapefile_path)
        gdf = gdf.to_crs(epsg=4326)
        filtered_gdf = gdf[gdf['FIRE_CAUSE'] == 'Lightning']
    
        # Plot the shapefile
        filtered_gdf.plot(ax=ax,marker='s', color='orange', markersize=5,label='LCFs')

        # Add gridlines
        ax.gridlines(draw_labels=True)
        
        # Create a GeoDataFrame from the points
        points_gdf = gpd.GeoDataFrame(geometry=points, crs='EPSG:4326')

        # Ensure both GeoDataFrames use the same coordinate reference system (CRS)
        points_gdf.set_crs('EPSG:4326', inplace=True)
 
        # Perform a spatial join to find points within the BC polygon
        points_within_bc = gpd.sjoin(points_gdf, bc_gdf, how='inner',predicate='intersects')

        filtered_points = [(point.x, point.y) for point in points_within_bc.geometry]
 
    
        for lon, lata in filtered_points:
            ax.plot(lon, lata, 'ro', markersize=5, transform=ccrs.PlateCarree())

        # Add a title
        plt.title(f'Lighting strikes and LCFs {end_date.date()}')
        plt.legend()

        # Show the plot
        plt.savefig(f'Lighting strikes and LCFs {end_date.date()}.png')
        plt.clf()
    

def comp(file1,file2, strike_fires):
    data1 = data_parser(file1)
    data2 = data_parser(file2)


def read_kmz_file(kmz_file):
    # Open the KMZ file
    with ZipFile(kmz_file, 'r') as kmz:
        # Look for the KML file inside the KMZ (there might be multiple, so we take the first)
        kml_file = [name for name in kmz.namelist() if name.lower().endswith('.kml')][0]
        
        # Extract the KML content
        kml_content = kmz.read(kml_file)
        
        # Parse the KML content using BeautifulSoup
        soup = BeautifulSoup(kml_content, 'html.parser')  # Use 'xml' parser for KML
        
        # Print the KML content (or process it further)
        print(soup.prettify())

