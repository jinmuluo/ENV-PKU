from netCDF4 import Dataset
import numpy as np


address = 'G:/PAHs/0.25 deg/PAHs_emission_2002.nc'
file = Dataset(address, 'r', format='NETCDF4')
matrix = file.variables['BaP'][:]
area = file.variables['grid_area'][:]
latt = file.variables['lat'][:]
lont = file.variables['lon'][:]
new_matrix = np.multiply(matrix, area*1000)*365*24*3600

new_f = Dataset('exam.nc', 'w', format='NETCDF4')
new_f.description = 'BaP emission in unit: Tons'
new_f.createDimension('lon', new_matrix.shape[1])
new_f.createDimension('lat', new_matrix.shape[0])
latitude = new_f.createVariable('latitude', np.float32, ('lat',))
longitude = new_f.createVariable('longitude', np.float32, ('lon',))
BaP = new_f.createVariable('BaP', np.float32, ('lat', 'lon',))
latitude.unit = 'degree_North in WGS84'
longitude.unit = 'degree_South in WGS84'
BaP.unit = 'B[a]P emission in unit: Tons'
new_f.variables['latitude'][:] = latt
new_f.variables['longitude'][:] = lont
new_f.variables['BaP'][:] = new_matrix
new_f.close()
data = np.zeros([len(latt)*len(lont), 3])
count = 0
for i in range(len(latt)):
    for j in range(len(lont)):
        data[count, 0] = latt[i]
        data[count, 1] = lont[j]
        data[count, 2] = new_matrix[i, j]
        count = count + 1
np.savetxt('example.txt', data)
