import numpy as np
from netCDF4 import Dataset, date2num
from datetime import datetime


"""
This python files is writen for change the PKU-FUEL SO2 emission inventory format:
(1) Add the missing points
(2) ......

Author: Luo Jinmu
Email:myjinmuluo@pku.edu.cn
Organization: Urban and Environmental Science, Peking University, China

"""

old_address = 'E:/OMI/pku-improve/SO2_2014_transportation.nc'                                        # 1
new_address = 'SO2_2014_TRO.nc'                                                                                     # 2
degree = 0.1
f = Dataset(old_address, 'r', format='NETCDF4')
emi = f.variables['emission'][:]
new_emi = np.zeros([emi.shape[1], emi.shape[2]])
for i in range(emi.shape[0]):
    new_emi = new_emi + emi[i, :, :]/1000/1000/1000/30/24/3600
new_emi = new_emi/12

new_f = Dataset(new_address, 'w', format='NETCDF4')
new_f.description = 'Improve PKU SO2 transportation emission inventory in 2014'                   # 3
new_f.Title = 'COARDS/netCDF file containing SO2 emission data set.'
new_f.Contact = 'myjinmuluo@pku.edu.cn, Peking University, college of Urban and Environmental Science'
new_f.Conventions = 'COARDS'
new_f.createDimension('lon', int(360/degree))
new_f.createDimension('lat', int(180/degree))
new_f.createDimension('time', 1)
lat = new_f.createVariable('lat', np.float32, ('lat',), chunksizes=[int(180/degree)])
lon = new_f.createVariable('lon', np.float32, ('lon',), chunksizes=[int(360/degree)])
SO2_tro = new_f.createVariable('SO2_tro', np.float64, ('time', 'lat', 'lon',),                              # 4
                                     chunksizes=[1, int(180/degree), int(360/degree)])
time = new_f.createVariable('time', np.int, ('time',), chunksizes=[1])
lat.units = 'degrees_north'
lat.axis = 'Y'
lat.long_name = 'Latitude'
lon.units = 'degrees_east'
lon.axis = 'X'
lon.long_name = 'Longitude'
SO2_tro.units = 'kg/m2/s'                                                                                # 5
SO2_tro.long_name = 'so2 from transportation emission'                                     # 6
time.long_name = 'Time'
time.axis = 'T'
time.calendar = 'standard'
time.units = 'hours since 1985-01-01 00:00:00'
new_f.variables['lat'][:] = np.arange(-90 + degree / 2, 90 + degree / 2, degree)
new_f.variables['lon'][:] = np.arange(0 + degree / 2, 360 + degree / 2, degree)
new_f.variables['SO2_tro'][:] = new_emi                                                                   # 7
new_f.variables['time'][:] = date2num(datetime(2014, 1, 1, 0), units=time.units, calendar=time.calendar)
print(date2num(datetime(2014, 1, 1, 0), units=time.units, calendar=time.calendar))


