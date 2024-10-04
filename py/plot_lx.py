'''
Produces density plots to compare lightning strike detection from AEM and CLDN sources
Example call: 
python3 plot_lx.py 100 '2023-02-01' '2024-03-01'

'''
import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point
import pandas as pd
from datetime import datetime, timedelta
from scipy.stats import gaussian_kde
import pickle as pickle
import os
import sys

def data_parser_aem(file):
    '''
    Parses the data from the AEM CSV
    '''
    df = pd.read_csv(file)
    df['time']= pd.to_datetime(df.iloc[:, 0])
    df['type'] = df.iloc[:, 1]
    df['latitude'] = df.iloc[:, 2]
    df['longitude'] = df.iloc[:, 3]
    df['pc'] = df.iloc[:, 4]
    df['ic'] = df.iloc[:, 5]
    df['station'] = df.iloc[:, 6]
    # Convert the DataFrame to a GeoDataFrame
    geometry = [Point(xy) for xy in zip(df['longitude'],df['latitude'])]
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs='EPSG:4326')  
    return df, gdf

def data_parser_cldn(file):
    '''
    Parses the data for the CLDN CSV
    '''
    df = pd.read_csv(file)
    df['time'] = pd.to_datetime(df.iloc[:, 7])
    df['polarity'] = df.iloc[:, 4]
    df['latitude'] = df.iloc[:, 2]
    df['longitude'] = df.iloc[:, 3]
    df['charge'] = df.iloc[:,6]
    geometry = [Point(xy) for xy in zip(df['longitude'],df['latitude'])]
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs='EPSG:4326')  
    
    return df, gdf



def plot_density(aem_df, cldn_df, n_grid_points, start_date, end_date):
    '''
    Produces strike density plot to comapre two data sources
    '''
     # Define grid for density estimation
     # Both datasets have same grid edges as bc shaapefile, so all equivalent
    lon_grid = np.linspace(aem_df['longitude'].min(), aem_df['longitude'].max(), n_grid_points)
    lat_grid = np.linspace(aem_df['latitude'].min(), aem_df['latitude'].max(), n_grid_points)
    lon_mesh, lat_mesh = np.meshgrid(lon_grid, lat_grid)


    #sort dates
    mask_aem = (aem_df['time'] >= start_date) & (aem_df['time'] <= end_date)
    aem_df = aem_df[mask_aem]
    mask_cldn = (cldn_df['time'] >= start_date) & (cldn_df['time'] <= end_date)
    cldn_df = cldn_df[mask_cldn]

    #reshape and apply kde onto discrete data
    aem_positions = np.vstack([aem_df['longitude'], aem_df['latitude']])
    aem_kde = gaussian_kde(aem_positions)
    aem_density = aem_kde(np.vstack([lon_mesh.ravel(), lat_mesh.ravel()])).reshape(lon_mesh.shape)
    cldn_positions = np.vstack([cldn_df['longitude'], cldn_df['latitude']])
    cldn_kde = gaussian_kde(cldn_positions)
    cldn_density = cldn_kde(np.vstack([lon_mesh.ravel(), lat_mesh.ravel()])).reshape(lon_mesh.shape)

    # Create subplots
    fig, axs = plt.subplots(1, 2, figsize = (15,6))
    
    #Max color values for plotting currently set to 0.07 by inspection
    #Could update this to automatically use highest value on both plots if desired

    #plot aem data
    contour_aem = axs[0].contourf(lon_mesh, lat_mesh, aem_density, levels=30, cmap='Blues', vmin = 0, vmax = 0.07)
    axs[0].set_title('AEM Density')
    bc_gdf.boundary.plot(ax=axs[0], color='black', linewidth= 0.5)

    #plot cldn data
    contour_cldn = axs[1].contourf(lon_mesh, lat_mesh, cldn_density, levels=30, cmap='Blues', vmin = 0, vmax = 0.07)
    axs[1].set_title('CLDN Density')
    bc_gdf.boundary.plot(ax=axs[1], color='black', linewidth = 0.5)

    #add a colorbar
    cbar = fig.colorbar(contour_aem, ax=axs, orientation='horizontal', fraction=0.05, pad=0.1)
    cbar.set_label('Density')

    fig.suptitle(f'Lightning strike density between {start_date} and {end_date}')
    # Adjust layout to prevent overlap
    plt.subplots_adjust(bottom=0.2)  
    

    if not os.path.exists('plots/lx_density_plots/'):
        os.mkdir('plots/lx_density_plots')
    plt.savefig(f'plots/lx_density_plots/{start_date}_to_{end_date}.png')
    plt.show()



###FILE PATHS

aem_path = '../data/lx_data/EarthNetworks_BCWS_LX_2023.csv'
cldn_path = '../data/lx_data/cldn.csv'
bc_boundary = '../data/shape_files/bc_boundary_terrestrial_multipart.shp'







if __name__ == "__main__":
    n_grids = int(sys.argv[1])
    start_date = sys.argv[2]
    end_date = sys.argv[3]
    bc_gdf = gpd.read_file(bc_boundary).to_crs('EPSG:4326')

    #pickle file generation 
    if not os.path.exists('pickles'):
            os.mkdir('pickles')

    #pickle AEM data
    if not os.path.exists('pickles/aem_in_range.pkl'):
        aem_df, aem_gdf, = data_parser_aem(aem_path)
        print('Filtering AEM data')
        filtered_aem_gdf = gpd.sjoin(aem_gdf, bc_gdf, how = 'inner', predicate = 'intersects')
        filtered_aem_df = filtered_aem_gdf.drop(columns = 'geometry')
        filtered_aem_df.to_pickle('pickles/aem_in_range.pkl')
        print('Filtered')

    else:
        with open(f'pickles/aem_in_range.pkl', 'rb') as f:
                filtered_aem_df = pickle.load(f)


    #pickle CLDN data
    if not os.path.exists('pickles/cldn_in_range.pkl'):
        cldn_df, cldn_gdf = data_parser_cldn(cldn_path)
        print('Filtering CLDN data')
        filtered_cldn_gdf = gpd.sjoin(cldn_gdf, bc_gdf, how = 'inner', predicate = 'intersects')
        filtered_cldn_df = filtered_cldn_gdf.drop(columns = 'geometry')
        filtered_cldn_df.to_pickle('pickles/cldn_in_range.pkl')
        print('Filtered')

    else:
        with open(f'pickles/cldn_in_range.pkl', 'rb') as f:
                filtered_cldn_df = pickle.load(f)

    #Filter out intracloud lightning
    #This will be incorporated into pickle data asap
    test_aem_df = filtered_aem_df[filtered_aem_df.type != 1]

    plot_density(test_aem_df, filtered_cldn_df, n_grids, start_date, end_date)