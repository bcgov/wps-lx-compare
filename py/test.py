import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import geopandas as gpd
from shapely.geometry import Point, shape
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import math 
import os
import pickle as pickle


file1 = pd.read_csv('../data/lx_data/WFPRD_Lightning_20240401-20240630.csv')
file2 = pd.read_csv('../data/lx_data/WFPRD_Lightning_20240701-20240731.csv')
file3 = pd.read_csv('../data/lx_data/WFPRD_Lightning_20240801-20240831.csv')




# Concatenate the DataFrames
combined_df = pd.concat([file1, file2, file3], ignore_index=True)

# Save the combined DataFrame to a new CSV file
#combined_df.to_csv('../data/lx_data/WFPRD_Lightning_20240401-20240831.csv', index=False)
combined_df.to_csv('combine.csv', index = False)