import numpy as np
import find_file as find
from datetime import datetime, timedelta
from netCDF4 import Dataset, num2date, date2num


# change the unit g/km2/month  into kg/m2/s and 0.1 degree to 1 degree
address = 'H:/PKU-FUEL/BaP/'
new_address = 'H:/PKU-FUEL/Test2/'
namelist = find.find_file(address, '.nc')
time_slice = 1
new_degree = 1
row = int(180/0.1)
col = int(360/0.1)
new_row = int(180/new_degree)
new_col = int(360/new_degree)
step = int(1/0.1)
new_area = np.zeros([new_row, new_col])
new_area[:, :] = 111.31 * new_degree * 111.31 * new_degree
for i in range(new_area.shape[0]):
    new_area[i, :] = new_area[i, :] * np.cos((90 - new_degree/2 - new_degree*i)*np.pi/180)

for name in namelist:
    file = Dataset(name, 'r', format='NETCDF4')
    year = name[-13:-9]
    date = (datetime(int(year), 1, 1))
    new_name = new_address + 'BaP_COARDS_' + name[-13:-9] + '_1x1.nc'
    emission = file.variables['emission'][:]
    grid_area = file.variables['grid_cell_area'][:]
    emission = np.multiply(emission, grid_area)
    term_emission = np.zeros([row, col])
    for i in range(emission.shape[0]):
        term_emission[:, 0:int(col/2)] = term_emission[:, 0:int(col/2)] + emission[i, :, int(col/2):]
        term_emission[:, int(col / 2):] = term_emission[:, int(col / 2):] + emission[i, :, 0:int(col/2)]
    term_emission = term_emission /1000/(365 * 24 * 3600)
    final_dat = np.zeros([int(180/new_degree), int(360/new_degree)])
    for j in range(final_dat.shape[0]):
        for k in range(final_dat.shape[1]):
            final_dat[j, k] = sum(sum(term_emission[j*step:(j+1)*step, k*step:(k+1)*step]))
    final_dat = np.divide(final_dat, new_area*1000*1000)

    new_file = Dataset(new_name, 'w', format='NETCDF4_CLASSIC')
    new_file.description = 'PKU-FUEL BaP monthly emission inventory'
    new_file.Title = 'COARDS/netCDF file containing BaP deforestation and wildfire emission data set.'
    new_file.Contact = 'taos@pku.edu.cn, Peking University college of Urban and Environmental Science'
    new_file.Conventions = 'COARDS'

    new_file.createDimension('lon', int(360/new_degree))
    new_file.createDimension('lat', int(180/new_degree))
    new_file.createDimension('time', time_slice)
    lat = new_file.createVariable('lat', np.float32, ('lat',), chunksizes=[int(180/new_degree)])
    lon = new_file.createVariable('lon', np.float32, ('lon',), chunksizes=[int(360/new_degree)])
    PG_SRCE__POPG = new_file.createVariable('PG_SRCE__POPG', np.float32, ('time', 'lat', 'lon',),
                                            chunksizes=[time_slice, int(180/new_degree), int(360/new_degree)])
    time = new_file.createVariable('time', np.int, ('time',), chunksizes=[time_slice])
    lat.units = 'degrees_north'
    lat.axis = 'Y'
    lon.units = 'degrees_east'
    lon.axis = 'X'
    PG_SRCE__POPG.units = 'kg/m2/s'
    PG_SRCE__POPG.long_name = 'POPG tracer'
    time.long_name = 'Time'
    time.axis = 'T'
    time.calendar = 'standard'
    time.units = 'hours since 1985-01-01 00:00:00'
    new_file.variables['PG_SRCE__POPG'][:] = final_dat
    new_file.variables['lat'][:] = np.arange(-90+new_degree/2, 90+new_degree/2, new_degree)
    new_file.variables['lon'][:] = np.arange(-180+new_degree/2, 180+new_degree/2, new_degree)
    new_file.variables['time'][:] = date2num(date, units=time.units, calendar=time.calendar)
    print(date2num(date, units=time.units, calendar=time.calendar))
    file.close()
    print(new_name, 'is done!')