'''
Plots accepted lightning data (within space time threshold of LCF) for all fire centers and BC. Also plots a point map of LCFs colored by which sensor detected it
'''

from lightning import comp #compare two types of lighting data for one fire center
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
import geopandas as gpd
import matplotlib.gridspec as gridspec

max_radius = 500 #define a max radius
#loads data for all fire centers and combines them for all of BC
data_se = comp('../data/lx_data/EarthNetworks_BCWS_LX_2023.csv','../data/lx_data/cldn.csv','SE', max_radius)
data_nw = comp('../data/lx_data/EarthNetworks_BCWS_LX_2023.csv','../data/lx_data/cldn.csv','NW', max_radius)
data_car = comp('../data/lx_data/EarthNetworks_BCWS_LX_2023.csv','../data/lx_data/cldn.csv','CARIBOO', max_radius)
data_coast = comp('../data/lx_data/EarthNetworks_BCWS_LX_2023.csv','../data/lx_data/cldn.csv','COAST', max_radius)
data_kam = comp('../data/lx_data/EarthNetworks_BCWS_LX_2023.csv','../data/lx_data/cldn.csv','KAM', max_radius)
data_pg = comp('../data/lx_data/EarthNetworks_BCWS_LX_2023.csv','../data/lx_data/cldn.csv','PG', max_radius)
data_bc = comp('../data/lx_data/EarthNetworks_BCWS_LX_2023.csv','../data/lx_data/cldn.csv','BC', max_radius)
data_both = data_se[0] + data_nw[0] + data_car[0] + data_coast[0] + data_kam[0] + data_pg[0]
data_aem = data_se[1] + data_nw[1] + data_car[1] + data_coast[1] + data_kam[1] + data_pg[1]
data_cldn = data_se[2] + data_nw[2] + data_car[2] + data_coast[2] + data_kam[2] + data_pg[2]
data_miss = data_se[3] + data_nw[3] + data_car[3] + data_coast[3] + data_kam[3] + data_pg[3]

#plotting LCFs colored by detection catagory
fig, ax = plt.subplots(figsize=(15, 15), subplot_kw={'projection': ccrs.PlateCarree()})
ax.set_extent([-136, -114, 48.3, 60.5], crs=ccrs.PlateCarree())

#plots BC boundary
bc_gdf = gpd.read_file('../data/shape_files/bc_boundary_terrestrial_multipart.shp')
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
plt.savefig(f'plots/{max_radius}data/LCFs/{max_radius}m-strike-detection.png')
plt.clf()

# #plotting bar graphs for each detection stat 
# zones = ['BC','PG', 'NW', 'Cariboo', 'Coast', 'Kam', 'SE']
# #defining data
# zone_vals_both = [len(data_bc[0]),len(data_pg[0]),len(data_nw[0]),len(data_car[0]), len(data_coast[0]), len(data_kam[0]), len(data_se[0])]
# zone_vals_aem = [len(data_bc[1]),len(data_pg[1]),len(data_nw[1]),len(data_car[1]), len(data_coast[1]), len(data_kam[1]), len(data_se[1])]
# zone_vals_cldn = [len(data_bc[2]),len(data_pg[2]),len(data_nw[2]),len(data_car[2]), len(data_coast[2]), len(data_kam[2]), len(data_se[2])]
# zone_vals_none = [len(data_bc[3]),len(data_pg[3]),len(data_nw[3]),len(data_car[3]), len(data_coast[3]), len(data_kam[3]), len(data_se[3])]
# colors = ['red', 'blue', 'green', 'purple', 'orange', 'cyan', 'magenta']

# #plotting
# fig, axs = plt.subplots(2,2,figsize=(15, 15))
# axs[0,0].set_title('Both sensors detected')
# axs[0,0].set_ylabel('# of fires')
# axs[0,0].bar(zones,zone_vals_both,color=colors)
# axs[0,1].set_title('Just AEM detected')
# axs[0,1].set_ylabel('# of fires')
# axs[0,1].bar(zones,zone_vals_aem,color=colors)
# axs[1,0].set_title('Just CLDN detected')
# axs[1,0].set_ylabel('# of fires')
# axs[1,0].bar(zones,zone_vals_cldn,color=colors)
# axs[1,1].set_title('Both sensors missed')
# axs[1,1].set_ylabel('# of fires')
# axs[1,1].bar(zones,zone_vals_none,color=colors)
# plt.tight_layout()
# plt.savefig(f'plots/{max_radius}data/LCFs/{max_radius}m-zone_hist.png')

#plotting bar graphs for each fire centers detection stats
fig = plt.figure(figsize=(12, 16))

#defining subplots
gs = gridspec.GridSpec(4, 2, height_ratios=[1, 1, 1, 1], width_ratios=[1, 1], hspace=0.4, wspace=0.3)
ax1 = plt.subplot(gs[0, 0])
ax2 = plt.subplot(gs[0, 1])
ax3 = plt.subplot(gs[1, 0])
ax4 = plt.subplot(gs[1, 1])
ax5 = plt.subplot(gs[2, 0])
ax6 = plt.subplot(gs[2, 1])
ax7 = plt.subplot(gs[3, 0:2])

#calculating bars
names = ['Hit', 'Only AEM', 'Only CLDN', 'Miss']
bc = [len(data_bc[0]), len(data_bc[1]), len(data_bc[2]), len(data_bc[3])]
pg = [len(data_pg[0]), len(data_pg[1]), len(data_pg[2]), len(data_pg[3])]
nw = [len(data_nw[0]), len(data_nw[1]), len(data_nw[2]), len(data_nw[3])]
car = [len(data_car[0]), len(data_car[1]), len(data_car[2]), len(data_car[3])]
coast = [len(data_coast[0]), len(data_coast[1]), len(data_coast[2]), len(data_coast[3])]
kam = [len(data_kam[0]), len(data_kam[1]), len(data_kam[2]), len(data_kam[3])]
se = [len(data_se[0]), len(data_se[1]), len(data_se[2]), len(data_se[3])]
colors = ['green', 'orange', 'red', 'black']

#plotting
ax1.set_title('South East')
ax1.set_ylabel('# of fires')
ax1.bar(names,se,color=colors)
ax2.set_title('Prince George')
ax2.set_ylabel('# of fires')
ax2.bar(names,pg,color=colors)
ax3.set_title('North West')
ax3.set_ylabel('# of fires')
ax3.bar(names,nw,color=colors)
ax4.set_title('Cariboo')
ax4.set_ylabel('# of fires')
ax4.bar(names,car,color=colors)
ax5.set_title('Coast')
ax5.set_ylabel('# of fires')
ax5.bar(names,coast,color=colors)
ax6.set_title('Kamloops')
ax6.set_ylabel('# of fires')
ax6.bar(names,kam,color=colors)
ax7.set_title('BC')
ax7.set_ylabel('# of fires')
ax7.bar(names,bc,color=colors)

plt.tight_layout()
plt.savefig(f'plots/{max_radius}data/LCFs/{max_radius}m-hist.png')