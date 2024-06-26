import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import geopandas as gpd
from shapely.geometry import Point
import numpy as np
import pandas as pd
from datetime import datetime, timedelta



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
    
    data = data_parser(file)
    time = data[0]
    lat = data[2]
    long = data[3]
    charge = data[4]
    i = 0
    n = 0
    
    while n <= len(long):
        end_date = datetime.strptime(time[i][:-3], "%Y-%m-%dT%H:%M:%S.%f") + timedelta(weeks=2)
        points = []
        while datetime.strptime(time[n][:-3], "%Y-%m-%dT%H:%M:%S.%f") <= end_date:
            points.append((lat[n],long[n]))
            n += 1
        
        # Create a GeoDataFrame from the points
        points_gdf = gpd.GeoDataFrame(geometry=[Point(longs, latas) for longs, latas in points])
        print(points_gdf)
        # Ensure both GeoDataFrames use the same coordinate reference system (CRS)
        points_gdf.set_crs(bc_gdf.crs, inplace=True)
        
        # Perform a spatial join to find points within the BC polygon
        points_within_bc = gpd.sjoin(points_gdf, bc_gdf, op='within')
        print(points_within_bc)
        filtered_points = [(point.x, point.y) for point in points_within_bc.geometry]

        print(filtered_points)
        for lon, lata in filtered_points:
            print('blah')
            ax.plot(lon, lata, 'ro', markersize=5, transform=ccrs.PlateCarree())

        # Add a title
        plt.title(f'Lighting strikes and LCFs {end_date.date()}')
        plt.legend()

        # Show the plot
        plt.savefig(f'Lighting strikes and LCFs {end_date.date()}.png')
        i += n

def comp(file1,file2, strike_fires):
    data1 = data_parser(file1)
    data2 = data_parser(file2)
