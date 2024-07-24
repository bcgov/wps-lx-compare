'''
Plots accepted lightning data (within space time threshold of LCF) for all fire centers and BC. Also plots a point map of LCFs colored by which sensor detected it
'''

from lightning import comp #compare two types of lighting data for one fire center
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
import geopandas as gpd

max_radius = 2000 #define a max radius
#loads data for all fire centers and combines them for all of BC
data_se = comp('../lx_data/data/EarthNetworks_BCWS_LX_2023.csv','../lx_data/data/cldn.csv','SE', max_radius)
data_nw = comp('../lx_data/data/EarthNetworks_BCWS_LX_2023.csv','../lx_data/data/cldn.csv','NW', max_radius)
data_car = comp('../lx_data/data/EarthNetworks_BCWS_LX_2023.csv','../lx_data/data/cldn.csv','CARIBOO', max_radius)
data_coast = comp('../lx_data/data/EarthNetworks_BCWS_LX_2023.csv','../lx_data/data/cldn.csv','COAST', max_radius)
data_kam = comp('../lx_data/data/EarthNetworks_BCWS_LX_2023.csv','../lx_data/data/cldn.csv','KAM', max_radius)
data_pg = comp('../lx_data/data/EarthNetworks_BCWS_LX_2023.csv','../lx_data/data/cldn.csv','PG', max_radius)
data_bc = comp('../lx_data/data/EarthNetworks_BCWS_LX_2023.csv','../lx_data/data/cldn.csv','BC', max_radius)
data_both = data_se[0] + data_nw[0] + data_car[0] + data_coast[0] + data_kam[0] + data_pg[0]
data_aem = data_se[1] + data_nw[1] + data_car[1] + data_coast[1] + data_kam[1] + data_pg[1]
data_cldn = data_se[2] + data_nw[2] + data_car[2] + data_coast[2] + data_kam[2] + data_pg[2]
data_miss = data_se[3] + data_nw[3] + data_car[3] + data_coast[3] + data_kam[3] + data_pg[3]

#plotting LCFs colored by detection catagory
fig, ax = plt.subplots(figsize=(15, 15), subplot_kw={'projection': ccrs.PlateCarree()})
ax.set_extent([-136, -114, 48.3, 60.5], crs=ccrs.PlateCarree())

#plots BC boundary
bc_gdf = gpd.read_file('../shape_files/bc_boundary_terrestrial_multipart.shp')
bc_gdf = bc_gdf.to_crs(epsg=4326)
bc_gdf.boundary.plot(ax=ax,edgecolor='black')

both = 0
aem = 0
cldn = 0
miss = 0

#Sorts LCFs by detection category 
for long, lat in data_both:
    both +=1
    ax.plot(long,lat, color='green', marker='o',markersize=6, transform=ccrs.PlateCarree())

for long, lat in data_aem:
    aem += 1
    ax.plot(long,lat, color='orange',marker='o',markersize=6,transform=ccrs.PlateCarree())
    
for long, lat in data_cldn:
    cldn += 1
    ax.plot(long,lat, color='red',marker='o',markersize=6,transform=ccrs.PlateCarree())
    
for long, lat in data_miss:
    miss += 1
    ax.plot(long,lat, color='black',marker='o',markersize=6,transform=ccrs.PlateCarree())

#How to plot a single legend entry for each detection type instead of one legend entry for each LCF
ax.scatter(np.nan,np.nan, marker='o', color='green', label=f'Both sensors detected: {both}')
ax.scatter(np.nan,np.nan, marker='o', color='orange', label=f'Just AEM detected: {aem}')
ax.scatter(np.nan,np.nan, marker='o', color='red', label=f'Just CLDN detected: {cldn}')
ax.scatter(np.nan,np.nan, marker='o', color='black', label=f'Both sensors missed: {miss}')
plt.title('LCFs ignition points colored by sensor detection combinations',fontsize=14)
plt.legend(fontsize=14)
plt.tight_layout()
plt.savefig(f'plots/{max_radius}_strike_detection.png')    