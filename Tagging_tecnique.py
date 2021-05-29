from netCDF4 import Dataset, date2num
import numpy as np
import find_file as find
from datetime import datetime


date_address = 'H:/PAHs/v2019-01/'
suffix = '.nc'
degree = 1
namelist = find.find_file(date_address, suffix)
print('Found', len(namelist), 'files in ', date_address)
matrix = np.zeros([1, int(180/degree), int(360/degree)])
dat = np.zeros([1, int(180/degree), int(360/degree)])
ca_dat = np.zeros([1, int(180/degree), int(360/degree)])
eu_dat = np.zeros([1, int(180/degree), int(360/degree)])
ru_dat = np.zeros([1, int(180/degree), int(360/degree)])
for file in namelist:
    f = Dataset(file, 'r', format='NETCDF4')
    matrix = matrix + f.variables['PG_SRCE__POPG'][:]
matrix = matrix/len(namelist)

# output three boreal forest fire emission inventory
North = 90
South = 40
Ca_left = -167
Ca_right = -50
Eu_left = -10
Eu_right = 33
Ru_left = 33
Ru_right = 180
up = int((90 + South)/degree)
down = int((90 + North)/degree)
ca_dat[0, up:down, int((180 + Ca_left)/degree):int((180 + Ca_right)/degree)] = matrix[0, up:down,
                                                            int((180 + Ca_left)/degree):int((180 + Ca_right)/degree)]
eu_dat[0, up:down, int((180 + Eu_left)/degree):int((180 + Eu_right)/degree)] = matrix[0, up:down,
                                                            int((180 + Eu_left)/degree):int((180 + Eu_right)/degree)]
ru_dat[0, up:down, int((180 + Ru_left)/degree):int((180 + Ru_right)/degree)] = matrix[0, up:down,
                                                             int((180 + Ru_left)/degree):int((180 + Ru_right)/degree)]

new_area = np.zeros([int(180/degree), int(360/degree)])
new_area[:, :] = 111.31 * degree * 111.31 * degree
for i in range(new_area.shape[0]):
    new_area[i, :] = new_area[i, :] * np.cos((90 - degree/2 - degree*i)*np.pi/180)

name = 'BaP_fire_european_1x1' + namelist[1][-3:]
print('Build the file:', name)
new_f = Dataset(name, 'w', format='NETCDF4')
new_f.description = 'Canadian boreal forest BaP fire emission in unit: kg/m2/s, average over 2002 - 2014'
new_f.Title = 'COARDS/netCDF file containing BaP fire emission data set.'
new_f.Contact = 'myjinmuluo@pku.edu.cn, Peking University college of Urban and Environmental Science'
new_f.Conventions = 'COARDS'
new_f.createDimension('lon', int(360/degree))
new_f.createDimension('lat', int(180/degree))
new_f.createDimension('time', 1)
lat = new_f.createVariable('lat', np.float32, ('lat',), chunksizes=[int(180/degree)])
lon = new_f.createVariable('lon', np.float32, ('lon',), chunksizes=[int(360/degree)] )
grid_area = new_f.createVariable('grid_area', np.float32, ('lat', 'lon',), chunksizes=[int(180/degree), int(360/degree)])
PG_SRCE__POPG = new_f.createVariable('PG_SRCE__POPG', np.float64, ('time', 'lat', 'lon',),
                                         chunksizes=[1, int(180/degree), int(360/degree)])
time = new_f.createVariable('time', np.int, ('time',), chunksizes=[1])
lat.units = 'degrees_north'
lat.axis = 'Y'
lat.long_name = 'Latitude'
lon.units = 'degrees_east'
lon.axis = 'X'
lon.long_name = 'Longitude'
grid_area.unit = ' grid area in unit:km2'
PG_SRCE__POPG.units = 'kg/m2/s'
PG_SRCE__POPG.long_name = 'POPG tracer'
time.long_name = 'Time'
time.axis = 'T'
time.calendar = 'standard'
time.units = 'hours since 1985-01-01 00:00:00'
new_f.variables['lat'][:] = np.arange(-90+degree/2, 90+degree/2, degree)
new_f.variables['lon'][:] = np.arange(-180+degree/2, 180+degree/2, degree)
new_f.variables['PG_SRCE__POPG'][:] = eu_dat
new_f.variables['grid_area'][:] = new_area
new_f.variables['time'][:] = date2num(datetime(2010, 1, 1, 0), units=time.units, calendar=time.calendar)
print(date2num(datetime(2010, 1, 1, 0), units=time.units, calendar=time.calendar))
new_f.close()
print('Year', 2010, 'Finished!')




