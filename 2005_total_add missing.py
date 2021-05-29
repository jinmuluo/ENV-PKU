import numpy as np
from netCDF4 import Dataset, date2num
from datetime import datetime
import pandas as pd


"""
This python files is writen for import the PKU-FUEL SO2 emission inventory:
(1) Add the missing points.
(2) Adjust the outlier Point sources.
(3) ...................................

Author: Luo Jinmu
Email:myjinmuluo@pku.edu.cn
Organization: College of Urban and Environmental Sciences, Peking University, Beijing, China

"""

# ----------------------------------------------------------------------------------------------------------------------
# Define the data address.
# ----------------------------------------------------------------------------------------------------------------------
tol_address = 'E:/OMI/pku-improve/SO2_2005_total.nc'
omi_address = 'E:/OMI/pku-improve/Sources.txt'
us_epa_address = 'E:/OMI/GRAPH_data/USEPA DATA.txt'
degree = 0.1
sources = pd.read_table(omi_address)
emi_point = np.array(sources.target)
lat = np.array(sources.lat)
lon = np.array(sources.lon)
print(emi_point.shape[0], 'point sources prepared.')
f = Dataset(tol_address, 'r', format='NETCDF4')
emi_total = f.variables['emission'][:]
area = f.variables['grid_cell_area'][:]
emi_inventory = np.zeros([emi_total.shape[1], emi_total.shape[2]])
for i in range(emi_total.shape[0]):
    emi_inventory = emi_inventory + np.multiply(emi_total[i, :, :], area)

# ----------------------------------------------------------------------------------------------------------------------
# Search the missing point in emission inventory.
# Remember the pku emission inventory ha different map projection with satellite emission inventory.
# ----------------------------------------------------------------------------------------------------------------------
mis_count = 0
count = 0
for i in range(lat.shape[0]):
    if lon[i] < 0:
        lon[i] = lon[i] + 360
    y = int((90 + lat[i])/degree)
    x = int(lon[i]/degree)
    # print(lat[i], y)
    # print(lon[i], x)
    emi_km = sum(sum(emi_inventory[(y-4):(y+4), (x-4):(x+4)]))/1000/1000/1000
    if emi_point[i] > 30 and emi_km < 5:
        mis_count = mis_count + 1
        emi_inventory[(y-4):(y+4), (x-4):(x+4)] = emi_point[i]*1000*1000*1000/64
    else:
        count = count + 1
print('missing:', mis_count)
print('found:', count)

# ----------------------------------------------------------------------------------------------------------------------
# OMI perform pretty well in US or North American.
# So this section is aiming to  adjust the point sources quality in US and Canada.
# ----------------------------------------------------------------------------------------------------------------------
lat_north = 80
lat_south = -80
lon_west = 10
lon_east = 350
small_count = 0
big_count = 0
for i in range(lat.shape[0]):
    y = int((90 + lat[i])/degree)
    x = int(lon[i]/degree)
    emi_km = sum(sum(emi_inventory[(y - 4):(y + 4), (x - 4):(x + 4)])) / 1000 / 1000 / 1000
    if lat_south <= lat[i] <= lat_north and lon_west <= lon[i] <= lon_east:
        if emi_km/(emi_point[i]+1)>= 2 or emi_km/(emi_point[i]+1) <= 0.5:
            emi_inventory[(y - 4):(y + 4), (x - 4):(x + 4)] = emi_point[i] * 1000 * 1000 * 1000 / 64
            if emi_km/(emi_point[i]+1)<= 0.5:
                small_count = small_count + 1
            elif emi_km/(emi_point[i]+1)>= 10:
                big_count = big_count + 1
print('North American have', small_count, 'too smaller')
print('North American have', big_count, 'too bigger')

# ----------------------------------------------------------------------------------------------------------------------
# extract the USEPA point sources in 2005 emission inventory.
# ----------------------------------------------------------------------------------------------------------------------
f = pd.read_table(us_epa_address)
emi = np.array(f.emission)
lat = np.array(f.lat)
lon = np.array(f.lon)
print('We found ', len(lat), 'Point sources in USEPA')

for i in range(len(lat)):
    y = int((90 + lat[i])/degree)
    x = int(lon[i]/degree)
    emi_km = sum(sum(emi_inventory[(y - 4):(y + 4), (x - 4):(x + 4)])) / 1000 / 1000 / 1000
    print(emi_km, emi[i])
