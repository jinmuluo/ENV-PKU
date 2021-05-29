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
Organization: Urban and Environmental Science, Peking University, China

"""

# ----------------------------------------------------------------------------------------------------------------------
# Define the data address.
# ----------------------------------------------------------------------------------------------------------------------
tol_address = 'E:/OMI/pku-improve/SO2_2005_total.nc'
ind_address = 'E:/OMI/pku-improve/SO2_2005_industry.nc'
omi_address = 'E:/OMI/pku-improve/Sources.txt'
degree = 0.1
sources = pd.read_table(omi_address)
emi_point = np.array(sources.target)
lat = np.array(sources.lat)
lon = np.array(sources.lon)
print(emi_point.shape[0], 'point sources prepared.')
f = Dataset(tol_address, 'r', format='NETCDF4')
f_ind = Dataset(ind_address, 'r', format='NETCDF4')
emi_term = f.variables['emission'][:]
emi_ind_term = f_ind.variables['emission'][:]
area = f.variables['grid_cell_area'][:]
emi_inventory = np.zeros([emi_term.shape[1], emi_term.shape[2]])
emi_ind = np.zeros([emi_term.shape[1], emi_term.shape[2]])
for i in range(emi_term.shape[0]):
    emi_inventory = emi_inventory + np.multiply(emi_term[i, :, :], area)
    emi_ind = emi_ind + np.multiply(emi_ind_term[i, :, :], area)

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
        emi_ind[(y-4):(y+4), (x-4):(x+4)] = emi_point[i]*1000*1000*1000/64
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
        if emi_km/(emi_point[i]+1)>= 10 or emi_km/(emi_point[i]+1) <= 0.1:
            emi_ind[(y - 4):(y + 4), (x - 4):(x + 4)] = emi_point[i] * 1000 * 1000 * 1000 / 64
            if emi_km/(emi_point[i]+1)<= 0.1:
                small_count = small_count + 1
            elif emi_km/(emi_point[i]+1)>= 10:
                big_count = big_count + 1
print('North American have', small_count, 'too smaller')
print('North American have', big_count, 'too bigger')
emi_ind = np.divide(emi_ind/1000, area*1000*1000*365*24*3600)

# ----------------------------------------------------------------------------------------------------------------------
# Output the new emission inventory.
# ----------------------------------------------------------------------------------------------------------------------
nc_name = 'SO2_2005_omi_total.nc'
new_f = Dataset(nc_name, 'w', format='NETCDF4')
new_f.description = 'Improve PKU SO2 industry emission inventory in 2005'
new_f.Title = 'COARDS/netCDF file containing SO2 emission data set.'
new_f.Contact = 'myjinmuluo@pku.edu.cn, Peking University, college of Urban and Environmental Science'
new_f.Conventions = 'COARDS'
new_f.createDimension('lon', int(360/degree))
new_f.createDimension('lat', int(180/degree))
new_f.createDimension('time', 1)
lat = new_f.createVariable('lat', np.float32, ('lat',), chunksizes=[int(180/degree)])
lon = new_f.createVariable('lon', np.float32, ('lon',), chunksizes=[int(360/degree)])
grid_area = new_f.createVariable('grid_area', np.float32, ('lat', 'lon',), chunksizes=[int(180/degree),int(360/degree)])
SO2_ind = new_f.createVariable('SO2_ind', np.float64, ('time', 'lat', 'lon',),
                                     chunksizes=[1, int(180/degree), int(360/degree)])
time = new_f.createVariable('time', np.int, ('time',), chunksizes=[1])
lat.units = 'degrees_north'
lat.axis = 'Y'
lat.long_name = 'Latitude'
lon.units = 'degrees_east'
lon.axis = 'X'
lon.long_name = 'Longitude'
grid_area.unit = 'km2'
SO2_ind.units = 'kg/m2/s'
SO2_ind.long_name = 'SO2 industrial emission'
time.long_name = 'Time'
time.axis = 'T'
time.calendar = 'standard'
time.units = 'hours since 1985-01-01 00:00:00'
new_f.variables['lat'][:] = np.arange(-90 + degree / 2, 90 + degree / 2, degree)
new_f.variables['lon'][:] = np.arange(0 + degree / 2, 360 + degree / 2, degree)
new_f.variables['SO2_ind'][:] = emi_ind
new_f.variables['grid_area'][:] = area
new_f.variables['time'][:] = date2num(datetime(2014, 1, 1, 0), units=time.units, calendar=time.calendar)
print(date2num(datetime(2014, 1, 1, 0), units=time.units, calendar=time.calendar))
f.close()
new_f.close()









