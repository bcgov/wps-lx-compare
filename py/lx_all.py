'''
Plots accepted lightning data (within space time threshold of LCF) for all fire centers and BC. Also plots a point map of LCFs colored by which sensor detected it
'''

from lightning import comp #compare two types of lighting data for one fire center
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
import geopandas as gpd

#loads data for all fire centers and combines them for all of BC
data_se = comp('../data/EarthNetworks_BCWS_LX_2023.csv','../data/cldn.csv','SE')
data_nw = comp('../data/EarthNetworks_BCWS_LX_2023.csv','../data/cldn.csv','NW')
data_car = comp('../data/EarthNetworks_BCWS_LX_2023.csv','../data/cldn.csv','CARIBOO')
data_coast = comp('../data/EarthNetworks_BCWS_LX_2023.csv','../data/cldn.csv','COAST')
data_kam = comp('../data/EarthNetworks_BCWS_LX_2023.csv','../data/cldn.csv','KAM')
data_pg = comp('../data/EarthNetworks_BCWS_LX_2023.csv','../data/cldn.csv','PG')
data_both = data_se[0] + data_nw[0] + data_car[0] + data_coast[0] + data_kam[0] + data_pg[0]
data_aem = data_se[1] + data_nw[1] + data_car[1] + data_coast[1] + data_kam[1] + data_pg[1]
data_cldn = data_se[2] + data_nw[2] + data_car[2] + data_coast[2] + data_kam[2] + data_pg[2]
data_miss = data_se[3] + data_nw[3] + data_car[3] + data_coast[3] + data_kam[3] + data_pg[3]
aem_dist = data_se[4] + data_nw[4] + data_car[4] + data_coast[4] + data_kam[4] + data_pg[4]
cldn_dist = data_se[5] + data_nw[5] + data_car[5] + data_coast[5] + data_kam[5] + data_pg[5]
aem_miss = data_se[6] + data_nw[6] + data_car[6] + data_coast[6] + data_kam[6] + data_pg[6]
cldn_miss = data_se[7] + data_nw[7] + data_car[7] + data_coast[7] + data_kam[7] + data_pg[7]

#plotting stike distance from LCF for all of BC
plt.figure(figsize=(15,15))
plt.hist(aem_dist, alpha=0.5, bins=np.linspace(0, 5000, 51), edgecolor='black', label=f'AEM, average dist: {round(np.mean(aem_dist),1)} +/- {round(np.std(aem_dist),1)} m, missed: {aem_miss}')
plt.hist(cldn_dist, alpha=0.3,bins=np.linspace(0, 5000, 51), edgecolor='black', label=f'CLDN, average dist: {round(np.mean(cldn_dist),1)} +/- {round(np.std(cldn_dist),1)} m, missed: {cldn_miss}')
plt.xlabel('Distance from LCF (m)', fontsize=14)
plt.ylabel('# of strikes', fontsize=14)
plt.title(f'Strike counts within 5km and 3 weeks of LCF ignition, AEM vs CLDN, BC',fontsize=18)
plt.legend(fontsize=14)
plt.tight_layout()
plt.savefig(f'BC_strike_data.png')
plt.clf()

#plotting LCFs colored by detection catagory
fig, ax = plt.subplots(figsize=(15, 15), subplot_kw={'projection': ccrs.PlateCarree()})
ax.set_extent([-136, -114, 48.3, 60.5], crs=ccrs.PlateCarree())

#plots BC boundary
bc_gdf = gpd.read_file('~/Documents/wps-lx-compare/shape_files/bc_boundary_terrestrial_multipart.shp')
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
plt.savefig('strike_detection.png')    