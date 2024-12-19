'''
Produces density plots to compare lightning strike detection from AEM and CLDN sources
Example call: 
python3 plot_lx.py 100 '2024-06-02' '2024-08-03'
python3 plot_lx.py 100 '2023-06-02' '2023-08-03' --use_old_data
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
from fig_tools import LinkZoom




def data_parser_aem(file):
    '''
    Parses the data from the AEM CSV
    '''
    df = pd.read_csv(file)
    if use_new_data:
        df['time']= pd.to_datetime(df.iloc[:,1]) 
        df['type'] = df.iloc[:,0] 
        df['latitude'] = df.iloc[:, 2]
        df['longitude'] = df.iloc[:, 3]
        df['pc'] = df.iloc[:, 4]
        df['ic'] = df.iloc[:, 5]
        
    else:

        df['time']=  pd.to_datetime(df.iloc[:, 0])
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
    if use_new_data:
        df['time'] = pd.to_datetime(df.iloc[:, 14].str.split('.', expand=True)[0], format='%y-%m-%d %H:%M:%S') #pd.to_datetime(df.iloc[:, 7])
        df['polarity'] = df.iloc[:, 2] #df.iloc[:, 4]
        df['latitude'] = df.iloc[:, 5] #df.iloc[:, 2]
        df['longitude'] = df.iloc[:, 6] #df.iloc[:, 3]
        df['charge'] = df.iloc[:,4] #df.iloc[:,6]
    else:
        df['time'] = pd.to_datetime(df.iloc[:, 7])
        df['polarity'] = df.iloc[:, 4]
        df['latitude'] = df.iloc[:, 2]
        df['longitude'] = df.iloc[:, 3]
        df['charge'] = df.iloc[:,6]
    geometry = [Point(xy) for xy in zip(df['longitude'],df['latitude'])]
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs='EPSG:4326')  
    
    return df, gdf


def plot_map(ax):
    bc_gdf.boundary.plot(ax=ax, color='black', linewidth= 0.5)
    car_gdf.boundary.plot(ax=ax, color='black', linewidth= 0.2)
    coast_gdf.boundary.plot(ax=ax, color='black', linewidth= 0.2)
    kam_gdf.boundary.plot(ax=ax, color='black', linewidth= 0.2)
    nw_gdf.boundary.plot(ax=ax, color='black', linewidth= 0.2)
    pg_gdf.boundary.plot(ax=ax, color='black', linewidth= 0.2)
    se_gdf.boundary.plot(ax=ax, color='black', linewidth= 0.2)


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

    #count strikes by region
    strikes_aem = aem_df['fire_center'].value_counts().reindex(fire_centers.keys(), fill_value=0)
    strikes_cldn = cldn_df['fire_center'].value_counts().reindex(fire_centers.keys(), fill_value=0)

    #reshape and apply kde onto discrete data
    aem_positions = np.vstack([aem_df['longitude'], aem_df['latitude']])
    factor = 0.15
    aem_kde = gaussian_kde(aem_positions, factor)
    scott_factor = aem_kde.scotts_factor()
    aem_density = aem_kde(np.vstack([lon_mesh.ravel(), lat_mesh.ravel()])).reshape(lon_mesh.shape)
    aem_density_prob = aem_density/np.sum(aem_density)*np.prod(np.diff(lon_mesh[0,:2]))
    aem_density_strikes = aem_density*len(aem_df)/np.sum(aem_density)

    cldn_positions = np.vstack([cldn_df['longitude'], cldn_df['latitude']])
    #import copy
    #cldn_positions = copy.deepcopy(aem_positions)
    #bw_cldn = gaussian_kde(cldn_positions, bw)
    cldn_kde = gaussian_kde(cldn_positions, factor)
    scott_factor_copy = cldn_kde.scotts_factor()
    cldn_density = cldn_kde(np.vstack([lon_mesh.ravel(), lat_mesh.ravel()])).reshape(lon_mesh.shape)
    cldn_density_prob = cldn_density/np.sum(cldn_density)*np.prod(np.diff(lon_mesh[0,:2]))
    cldn_density_strikes = cldn_density*len(cldn_df)/np.sum(cldn_density)

    #print(f'Scott factor:{scott_factor}')
    #print(f'Scott factor copy:{scott_factor_copy}')

    #calculate maximum density for plotting
    max_density = np.max(aem_density_prob)
    if np.max(cldn_density_prob) > max_density:
        max_density = np.max(cldn_density_prob)


    fig1, axs1 = plt.subplots(1, 2, figsize = (15,6))
    #plot aem data
    contour_aem = axs1[0].contourf(lon_mesh, lat_mesh, aem_density_prob, levels=30, cmap='Blues', vmin = 0, vmax = max_density)
    #axs1[0].set_title(f'AEM Density ({len(aem_df)} strikes)\n CAR: {strikes_aem.iloc[0]}, COAST: {strikes_aem.iloc[1]}, KAM: {strikes_aem.iloc[2]}, NW: {strikes_aem.iloc[3]}, PG: {strikes_aem.iloc[4]}, SE: {strikes_aem.iloc[5]}')
    axs1[0].set_title(f'AEM Density ({len(aem_df)} strokes)')
    plot_map(axs1[0])
    

    #plot cldn data
    contour_cldn = axs1[1].contourf(lon_mesh, lat_mesh, cldn_density_prob, levels=30, cmap='Blues', vmin = 0, vmax = max_density)
    #axs1[1].set_title(f'CLDN Density ({len(cldn_df)} strikes)\n CAR: {strikes_cldn.iloc[0]}, COAST: {strikes_cldn.iloc[1]}, KAM: {strikes_cldn.iloc[2]}, NW: {strikes_cldn.iloc[3]}, PG: {strikes_cldn.iloc[4]}, SE: {strikes_cldn.iloc[5]}')
    axs1[1].set_title(f'CLDN Density ({len(cldn_df)} strokes)')
    plot_map(axs1[1])

    #add a colorbar
    cbar = fig1.colorbar(contour_aem, ax=axs1, orientation='horizontal', fraction=0.05, pad=0.1)
    cbar.ax.tick_params(labelrotation=45)
    cbar.set_label('Density')

    fig1.suptitle(f'Lightning stroke density between {start_date} and {end_date}')
    # Adjust layout to prevent overlap
    plt.subplots_adjust(bottom=0.2)  
    
    if not os.path.exists('plots'):
            os.mkdir('plots')
    if not os.path.exists('plots/lx_density_plots/'):
        os.mkdir('plots/lx_density_plots')
    plt.savefig(f'plots/lx_density_plots/{start_date}_to_{end_date}_comp.png')
    #synchronize subplot zoom
    zoomsync = LinkZoom(fig1, axs1)


    #Generate flux plot
    #difference in probabilities
    density_dif_prob = np.subtract(aem_density_prob, cldn_density_prob)
    #colorbar limits calculation
    colorbar_max_prob = np.max(density_dif_prob)
    if abs(np.min(density_dif_prob)) > colorbar_max_prob:
        colorbar_max_prob = abs(np.min(density_dif_prob))
    levels_prob = np.linspace(-colorbar_max_prob, colorbar_max_prob, 31)
    #difference in strikes
    density_dif_strikes = np.subtract(aem_density_strikes, cldn_density_strikes)
    #colorbar limits calculation
    colorbar_max_strikes = np.max(density_dif_strikes)
    if abs(np.min(density_dif_strikes)) > colorbar_max_strikes:
        colorbar_max_strikes = abs(np.min(density_dif_strikes))
    levels_strikes = np.linspace(-colorbar_max_strikes, colorbar_max_strikes, 31)

    

    #create figure for plotting
    fig2, axs2 = plt.subplots(1,2, figsize = (15,6))

    #Plot differences
    contour_dif_prob = axs2[0].contourf(lon_mesh, lat_mesh, density_dif_prob, levels=levels_prob, cmap='seismic', vmin = -colorbar_max_prob, vmax = colorbar_max_prob)
    plot_map(axs2[0])
    axs2[0].set_title(f'Difference in probability density')

    cbar_prob = fig2.colorbar(contour_dif_prob, ax=axs2[0], orientation='horizontal', fraction=0.05, pad=0.1)
    cbar_prob.set_label('Probability Density')

    cbar_prob.ax.text(0, 1.05, 'CLDN dominant', ha='center', va='bottom', transform=cbar_prob.ax.transAxes)
    cbar_prob.ax.text(1, 1.05, 'AEM dominant', ha='center', va='bottom', transform=cbar_prob.ax.transAxes)
    cbar_prob.ax.tick_params(labelrotation = 45)


    contour_dif_strikes = axs2[1].contourf(lon_mesh, lat_mesh, density_dif_strikes, levels=levels_strikes, cmap='seismic', vmin = -colorbar_max_strikes, vmax = colorbar_max_strikes)
    plot_map(axs2[1])
    axs2[1].set_title(f'Difference in strokes')

    cbar_strikes = fig2.colorbar(contour_dif_strikes, ax=axs2[1], orientation='horizontal', fraction=0.05, pad=0.1)
    cbar_strikes.set_label('Strokes')

    cbar_strikes.ax.text(0, 1.05, 'CLDN dominant', ha='center', va='bottom', transform=cbar_strikes.ax.transAxes)
    cbar_strikes.ax.text(1, 1.05, 'AEM dominant', ha='center', va='bottom', transform=cbar_strikes.ax.transAxes)
    cbar_strikes.ax.tick_params(labelrotation=45)
    fig2.suptitle(f'Lightning stroke density difference between {start_date} and {end_date}')
    plt.savefig(f'plots/lx_density_plots/{start_date}_to_{end_date}_dif.png')
 
    #Produce table
    absolute_difference = abs(strikes_aem - strikes_cldn)
    average_values = (strikes_aem + strikes_cldn) / 2

    # Calculate the percent difference
    percent_difference = round((absolute_difference / average_values).fillna(0) * 100, 3)

    # Add the percent difference to the DataFrame
    all_strikes = pd.concat([strikes_aem, strikes_cldn, percent_difference], axis=1)
    all_strikes.columns = ['AEM', 'CLDN', 'Percent Difference']

    # Create the table
    fig3, axs3 = plt.subplots(figsize=(10, 4))
    axs3.axis('tight')
    axs3.axis('off')
    table = axs3.table(cellText=all_strikes.values, colLabels=all_strikes.columns, rowLabels=list(fire_centers.keys()), loc='center')
    axs3.set_title(f'Lightning stroke counts between {start_date} and {end_date}')
    plt.savefig(f'plots/lx_density_plots/{start_date}_to_{end_date}_table.png')
    plt.show()

    





if __name__ == "__main__":
    # Check if --use_old_data flag is in the command line arguments
    use_old_data = "--use_old_data" in sys.argv
    use_new_data = not use_old_data

    # Filter out unwanted arguments 
    args_2 = [arg for arg in sys.argv if arg != '..']
    
    # Check for missing inputs
    if len(args_2) < 4:
        print("Usage: script.py <n_grids> <start_date> <end_date> [--use_old_data]")
        sys.exit(1)

    # Parse the arguments
    n_grids = int(args_2[1])
    start_date = args_2[2]
    end_date = args_2[3]
    


    #LIGHTNING FILE PATHS
    aem_path = '../data/lx_data/BCwildfire_2024_April-Sept_pulse.csv' 
    cldn_path = '../data/lx_data/WFPRD_Lightning_20240401-20240831.csv'  
    if use_old_data:
        aem_path = '../data/lx_data/old_data/EarthNetworks_BCWS_LX_2023.csv'
        cldn_path = '../data/lx_data/old_data/cldn.csv'


    #SHAPEFILE PATHS
    bc_boundary = '../data/shape_files/bc_boundary_terrestrial_multipart.shp'
    cariboo = '../data/shape_files/cariboo_fc.shp'
    coast = '../data/shape_files/coast_fc.shp'
    kamloops = '../data/shape_files/kam_fc.shp'
    northwest = '../data/shape_files/nw_fc.shp'
    princegeorge = '../data/shape_files/pg_fc.shp'
    southeast = '../data/shape_files/se_fc.shp'

    

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


    # Pickle AEM dat
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
   