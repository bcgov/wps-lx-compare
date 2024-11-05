# wps-lx-compare
BCWS Predictive Services Unit: python based comparison of lightning data from two providers

2024 Data:
https://bcgov.sharepoint.com/:u:/t/01324/ER6BVzoLIqRCgSG3m0hQjBwBBniSxrFW4viVKRFF0SR_uw?e=dKfU0d


2023 Data:
https://bcgov.sharepoint.com/:u:/t/01324/ETRzSrO9PEBDjkzU6R8ogfgB9h2-HkoVUO8SAprpYfHQuA?e=46eAsJ




Background:
The BC Wildfire service currently uses lightning strike data from a national sensor network in order to determine fire start points and make forecasts. Another vendor proposed their strike detction network service as an alternative. This project was created to evaluate the accuracy and extent of the data from these two sources, to determine which is better. This involves looking at the spatial distribution of lightning strikes themselves, as well as their proximity to known lightning-caused fire start points.


Dependencies:
Matplotlib
Cartopy
numpy
scipy
shapely
pandas 
geopandas
pickle

These can be imported as follows:
pip3 install <package_name>

Scripts:

**Plot_lx.py** is a program for plotting the spatial extent of lightning strikes detected by the two networks over a specified time period. The command line call to this script should look like:

python3 plot_lx.py n_grids 'date_start 'date_end' --optional_flag

n_grids specifies the number of grids on which the initial data is plotted. Note that the outputs are smooth kernel density estimates. 'date_start' and 'date_end' are dates over which we wat to look at the strikes. The 2023 dataset contains strike data from April 2023- September 2023 and the 2024 dataset from April 2024-Spetember 2024. If there are no values in the dataset within the selected timeframe, an error of 'incorrect array length' will be seen. If one of the endpoint dates is outside the range, the program will run, but may give the incorrect impression that there is data outside the real range (e.g. August 2023-November 2023 will output plots, but the shown data does not run past the end of August).

Sample script call for most recent data:
python3 plot_lx.py 100 '2024-06-02' '2024-08-03'

The 2023 data are in a slightly different format than the 2024 data, so a flag is required to get a correct parsing.
 Sample function call for using 2023 data:
python3 plot_lx.py 100 '2023-06-02' '2023-08-03' --use_old_data

Both of these versions will initially involve a pickling process. The first run may take some time to process the data, but subsequent rereads of the pickle files will be fast.

**lx_all.py** is a script which calculates the distances between detected lightning strikes and lightning-caused fires and produces plots. The mechanics of the distances calculation and spatial joins are in **lightning.py**, which also contains the files paths. This file is currently written to process 2024 data, but modifications required to process 2023 data are in comments in both files. lx_all also has a variable at the top called max_radius, which determines the limit for classifying a fire as 'matched' to a given lightning strike. Increasing the radius variable will increase the number of fires calssified as 'matched'. 

This script requires fire perimeter shapefiles in order to run. All required files for the 2024 season may be found at the link above, in the necessary format. Future runs will require new shapefiles, which can be acquired by running the get_perimeters.py script. Like the other script, the inital run requires reading and pickling data and may take a few hours. 

Sample script call:
python3 lx_all.py



