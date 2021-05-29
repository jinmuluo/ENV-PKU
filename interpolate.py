import numpy as np
import find_file as find
from datetime import datetime, timedelta
from netCDF4 import Dataset, num2date, date2num


Address = 'H:/PAHs/0.25 deg/'
name_list = find.find_file(Address, '.nc')
old_degree = 0.25
new_degree = 1
time_slice = 1
new_row = int(180/new_degree)
new_col = int(360/new_degree)
new_area = np.zeros([new_row, new_col])
new_area[:, :] = 111.31 * new_degree * 111.31 * new_degree
for i in range(new_area.shape[0]):
    new_area[i, :] = new_area[i, :] * np.cos((90 - new_degree/2 - new_degree*i)*np.pi/180)

for i in range(len(name_list)):
    f = Dataset(name_list[i], 'r', format='NETCDF4')
    year = name_list[i][-7:-3]
    BaP = f.variables['BaP'][:]
    area = f.variables['grid_area'][:]
    BaP_term = np.multiply(BaP, area)
    BaP_new = np.zeros([new_row, new_col])
    for j in range(new_row):
        for k in range(new_col):
            BaP_new[j, k] = np.sum(np.sum(BaP_term[j*4:(j*4)+4, k*4:(k*4)+4]))

    BaP_new = np.divide(BaP_new, new_area)
    name = 'BaP_fire'+ name_list[i][-17:-3] + '.1x1' + name_list[i][-3:]
    new_f = Dataset(name, 'w', format='NETCDF4')
    new_f.description = 'BaP  year fire emission in unit: kg/m2/s'
    new_f.Title = 'COARDS/netCDF file containing BaP fire emission data set.'
    new_f.Contact = 'myjinmuluo@pku.edu.cn, Peking University college of Urban and Environmental Science'
    new_f.Conventions = 'COARDS'
    new_f.createDimension('lon', new_col)
    new_f.createDimension('lat', new_row)
    new_f.createDimension('time', time_slice)
    lat = new_f.createVariable('lat', np.float32, ('lat',), chunksizes=[new_row])
    lon = new_f.createVariable('lon', np.float32, ('lon',), chunksizes=[new_col] )
    grid_area = new_f.createVariable('grid_area', np.float32, ('lat', 'lon',), chunksizes=[new_row, new_col])
    PG_SRCE__POPG = new_f.createVariable('PG_SRCE__POPG', np.float64, ('time', 'lat', 'lon',),
                                         chunksizes=[1, new_row, new_col])
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
    new_f.variables['lat'][:] = np.arange(-90+new_degree/2, 90+new_degree/2, new_degree)
    new_f.variables['lon'][:] = np.arange(-180+new_degree/2, 180+new_degree/2, new_degree)
    new_f.variables['PG_SRCE__POPG'][:] = BaP_new
    new_f.variables['grid_area'][:] = new_area
    new_f.variables['time'][:] = date2num(datetime(int(year), 1, 1, 0), units=time.units, calendar=time.calendar)
    print(date2num(datetime(int(year), 1, 1, 0), units=time.units, calendar=time.calendar))
    new_f.close()
    print('Year', str(i + 2001), 'Finished!')
