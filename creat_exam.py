from netCDF4 import Dataset
import numpy as np


address = 'H:/PAHs/BaP_soil_conc.merra2.4x5.nc '
file = Dataset(address, 'r', format='NETCDF4')
matrix = file.variables['IJ_AVG_S__POPG'][:]
latt = file.variables['lat'][:]
lont = file.variables['lon'][:]
time2 = file.variables['time'][:]
empty = np.zeros(matrix.shape)

new_f = Dataset('BaP_soil_conc.empty.4x5.nc', 'w', format='NETCDF4')
new_f.description = 'zeros emission inventory used to replace surface pops emission'
new_f.createDimension('lon', 72)
new_f.createDimension('lat', 46)
new_f.createDimension('time', 1)
lat = new_f.createVariable('lat', np.float32, ('lat',), chunksizes=[46])
lon = new_f.createVariable('lon', np.float32, ('lon',), chunksizes=[72])
time = new_f.createVariable('time', np.float32, ('time',), chunksizes=[1])
IJ_AVG_S__POPG = new_f.createVariable('IJ_AVG_S__POPG', np.float32, ('time', 'lat', 'lon',),
                                      chunksizes=[1, 46, 72])
lat.units = 'degrees_north'
lat.long_name = 'Latitude'
lat.axis = 'Y'
lon.units = 'degrees_east'
lon.long_name = 'Longitude'
lon.axis = 'X'
time.axis = 'T'
time.units = 'hours since 1985-1-1 00:00:0.0'
time.calendar = 'gregorian'
IJ_AVG_S__POPG.units = 'kg/m2/s'
new_f.variables['lat'][:] = latt
new_f.variables['lon'][:] = lont
new_f.variables['time'][:] = time2[:]
new_f.variables['IJ_AVG_S__POPG'][:] = empty
new_f.close()

