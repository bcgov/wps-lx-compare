'''
Produces density plots to compare lightning strike detection from AEM and CLDN sources
Example call: 
python3 plot_lx.py 100 '2023-08-02' '2023-08-03'

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


# Create subplots
fig, axs = plt.subplots(1, 2, figsize = (15,6))

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


syncing =False #flag to prevent infinite recursion of zoom

def link_zoom(event):
    # Get the current limits of the first axis
    global syncing
    global fig
    global axs
    if syncing:
         return
    syncing = True
    xlim = axs[0].get_xlim()
    ylim = axs[0].get_ylim()
    
    # Set the limits for the second axis
    axs[1].set_xlim(xlim)
    axs[1].set_ylim(ylim)
    
    # Redraw the figure
    fig.canvas.draw_idle()
    syncing = False

def link_zoom2(event):
    # Get the current limits of the first axis
    global syncing
    global fig
    global axs
    if syncing:
         return
    syncing = True
    xlim = axs[1].get_xlim()
    ylim = axs[1].get_ylim()
    
    # Set the limits for the second axis
    axs[0].set_xlim(xlim)
    axs[0].set_ylim(ylim)
    
    # Redraw the figure
    fig.canvas.draw_idle()
    syncing = False

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



    #count strikes
    strikes_aem = np.zeros(6)
    '''
    for name in fire_centers:
        print(name)
        strikes_aem.append(aem_df['fire_center'].value_counts()[name])

    strikes_cldn = []
    for name in fire_centers:
        strikes_cldn.append(cldn_df['fire_center'].value_counts()[name])
        '''


    strikes_aem[0] = aem_df['fire_center'].value_counts()['Cariboo']
    strikes_aem[1] = aem_df['fire_center'].value_counts()['Coast']
    strikes_aem[2] = aem_df['fire_center'].value_counts()['Kamloops']
    strikes_aem[3] = aem_df['fire_center'].value_counts()['Northwest']
    strikes_aem[4] = aem_df['fire_center'].value_counts()['Prince George']
    astrikes_aem[5] = aem_df['fire_center'].value_counts()['Southeast']
    

    #reshape and apply kde onto discrete data
    aem_positions = np.vstack([aem_df['longitude'], aem_df['latitude']])
    factor = 0.15
    aem_kde = gaussian_kde(aem_positions, factor)
    scott_factor = aem_kde.scotts_factor()
    aem_density = aem_kde(np.vstack([lon_mesh.ravel(), lat_mesh.ravel()])).reshape(lon_mesh.shape)

    cldn_positions = np.vstack([cldn_df['longitude'], cldn_df['latitude']])
    #import copy
    #cldn_positions = copy.deepcopy(aem_positions)
    #bw_cldn = gaussian_kde(cldn_positions, bw)
    cldn_kde = gaussian_kde(cldn_positions, factor)
    scott_factor_copy = cldn_kde.scotts_factor()
    cldn_density = cldn_kde(np.vstack([lon_mesh.ravel(), lat_mesh.ravel()])).reshape(lon_mesh.shape)

    print(f'Scott factor:{scott_factor}')
    print(f'Scott factor copy:{scott_factor_copy}')

    
    
    #Max color values for plotting currently set to 0.07 by inspection
    #Could update this to automatically use highest value on both plots if desired

    #plot aem data
    contour_aem = axs[0].contourf(lon_mesh, lat_mesh, aem_density, levels=30, cmap='Blues', vmin = 0, vmax = 0.07)
    axs[0].set_title(f'AEM Density ({len(aem_df)} strikes)\n CAR: {aem_strikes[0]}')
    bc_gdf.boundary.plot(ax=axs[0], color='black', linewidth= 0.5)
    car_gdf.boundary.plot(ax=axs[0], color='black', linewidth= 0.2)
    coast_gdf.boundary.plot(ax=axs[0], color='black', linewidth= 0.2)
    kam_gdf.boundary.plot(ax=axs[0], color='black', linewidth= 0.2)
    nw_gdf.boundary.plot(ax=axs[0], color='black', linewidth= 0.2)
    pg_gdf.boundary.plot(ax=axs[0], color='black', linewidth= 0.2)
    se_gdf.boundary.plot(ax=axs[0], color='black', linewidth= 0.2)

    #plot cldn data
    contour_cldn = axs[1].contourf(lon_mesh, lat_mesh, cldn_density, levels=30, cmap='Blues', vmin = 0, vmax = 0.07)
    axs[1].set_title(f'CLDN Density ({len(cldn_df)} strikes)')
    bc_gdf.boundary.plot(ax=axs[1], color='black', linewidth = 0.5)
    car_gdf.boundary.plot(ax=axs[1], color='black', linewidth= 0.2)
    coast_gdf.boundary.plot(ax=axs[1], color='black', linewidth= 0.2)
    kam_gdf.boundary.plot(ax=axs[1], color='black', linewidth= 0.2)
    nw_gdf.boundary.plot(ax=axs[1], color='black', linewidth= 0.2)
    pg_gdf.boundary.plot(ax=axs[1], color='black', linewidth= 0.2)
    se_gdf.boundary.plot(ax=axs[1], color='black', linewidth= 0.2)

    #add a colorbar
    cbar = fig.colorbar(contour_aem, ax=axs, orientation='horizontal', fraction=0.05, pad=0.1)
    cbar.set_label('Density')

    fig.suptitle(f'Lightning strike density between {start_date} and {end_date}')
    # Adjust layout to prevent overlap
    plt.subplots_adjust(bottom=0.2)  
    
    if not os.path.exists('plots'):
            os.mkdir('plots')
    if not os.path.exists('plots/lx_density_plots/'):
        os.mkdir('plots/lx_density_plots')
    plt.savefig(f'plots/lx_density_plots/{start_date}_to_{end_date}.png')

    axs[0].callbacks.connect('xlim_changed', link_zoom)
    axs[0].callbacks.connect('ylim_changed', link_zoom)
    axs[1].callbacks.connect('xlim_changed', link_zoom)
    axs[1].callbacks.connect('ylim_changed', link_zoom2)
    plt.show()
    






###FILE PATHS

aem_path = '../data/lx_data/EarthNetworks_BCWS_LX_2023.csv'
cldn_path = '../data/lx_data/cldn.csv'
bc_boundary = '../data/shape_files/bc_boundary_terrestrial_multipart.shp'
cariboo = '../data/shape_files/cariboo_fc.shp'
coast = '../data/shape_files/coast_fc.shp'
kamloops = '../data/shape_files/kam_fc.shp'
northwest = '../data/shape_files/nw_fc.shp'
princegeorge = '../data/shape_files/pg_fc.shp'
southeast = '../data/shape_files/se_fc.shp'





if __name__ == "__main__":
    n_grids = int(sys.argv[1])
    start_date = sys.argv[2]
    end_date = sys.argv[3]
    #bandwidth = float(sys.argv[4])
    bc_gdf = gpd.read_file(bc_boundary).to_crs('EPSG:4326')
    car_gdf = gpd.read_file(cariboo).to_crs('EPSG:4326')
    coast_gdf = gpd.read_file(coast).to_crs('EPSG:4326')
    kam_gdf = gpd.read_file(kamloops).to_crs('EPSG:4326')
    nw_gdf = gpd.read_file(northwest).to_crs('EPSG:4326')
    pg_gdf = gpd.read_file(princegeorge).to_crs('EPSG:4326')
    se_gdf = gpd.read_file(southeast).to_crs('EPSG:4326')

    fire_centers = {'Cariboo': car_gdf,'Coast': coast_gdf,'Kamloops': kam_gdf,'Northwest': nw_gdf,
    'Prince George': pg_gdf,'Southeast': se_gdf,}

    

    #pickle file generation 
    if not os.path.exists('pickles'):
            os.mkdir('pickles')


    # Pickle AEM data
    if not os.path.exists('pickles/aem_in_range.pkl'):
        aem_df, aem_gdf = data_parser_aem(aem_path)
        
        # Add fire center classification
        aem_df['fire_center'] = None
        print('Filtering AEM data')

        print(f"Initial aem_gdf size: {len(aem_gdf)}")

        for name, fc in fire_centers.items():
            joined = gpd.sjoin(aem_gdf, fc, how="inner", predicate="intersects")
            print(f"Joined {name}: {len(joined)} points")
            
            # Only update fire center classification
            aem_gdf.loc[joined.index, 'fire_center'] = name

        # After processing all fire centers, filter for those with fire center classifications
        filtered_aem_gdf = aem_gdf[aem_gdf['fire_center'].notna()]
        print(f"Filtered aem_gdf size: {len(filtered_aem_gdf)}")
        filtered_aem_gdf.reset_index(drop=True, inplace=True)

        # Filtered AEM DataFrame
        filtered_aem_df = filtered_aem_gdf.drop(columns='geometry')
        # Filter out intracloud strikes
        filtered_aem_df = filtered_aem_df[filtered_aem_df.type != 1]
        filtered_aem_df.to_csv('Test.csv')
        filtered_aem_df.to_pickle('pickles/aem_in_range.pkl')
        print('Filtered')


    else:
        with open(f'pickles/aem_in_range.pkl', 'rb') as f:
                filtered_aem_df = pickle.load(f)
    
 
    #pickle CLDN data
    if not os.path.exists('pickles/cldn_in_range.pkl'):
        cldn_df, cldn_gdf = data_parser_cldn(cldn_path)

        
        # Add fire center classification
        cldn_df['fire_center'] = None
        print('Filtering CLDN data')

        print(f"Initial cldn_gdf size: {len(cldn_gdf)}")

        for name, fc in fire_centers.items():
            joined = gpd.sjoin(cldn_gdf, fc, how="inner", predicate="intersects")
            print(f"Joined {name}: {len(joined)} points")
            
            # Only update fire center classification
            cldn_gdf.loc[joined.index, 'fire_center'] = name

        # After processing all fire centers, filter for those with fire center classifications
        filtered_cldn_gdf = cldn_gdf[cldn_gdf['fire_center'].notna()]
        print(f"Filtered cldn_gdf size: {len(filtered_cldn_gdf)}")
        filtered_cldn_gdf.reset_index(drop=True, inplace=True)

        # Filtered CLDNDataFrame
        filtered_cldn_df = filtered_cldn_gdf.drop(columns='geometry')
 
        filtered_cldn_df.to_csv('Test2.csv')
        filtered_cldn_df.to_pickle('pickles/cldn_in_range.pkl')
        print('Filtered')

    else:
        with open(f'pickles/cldn_in_range.pkl', 'rb') as f:
                    filtered_cldn_df = pickle.load(f)
    

    plot_density(filtered_aem_df, filtered_cldn_df, n_grids, start_date, end_date)
   